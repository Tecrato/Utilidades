from typing import Tuple, Union, List
from math import pi, comb
from pygame import Vector2


class Simple_acceleration:
    def __init__(self,vel, dir,pos) -> None:
        self.vel: float = vel
        self.dir: Vector2 = Vector2(dir)
        self.pos = Vector2(pos)
    def update(self,dt=1) -> Vector2:
        self.pos += self.dir*self.vel*dt
        return self.pos
    def follow(self,pos,dt=1):
        self.dir = (Vector2(pos)-self.pos).normalize()
        self.pos += self.dir*self.vel*dt*60
        return self.pos

class Curva_de_Bezier:
    """
    Sistema de curvas Bézier generalizado con interpolación suave y eficiente.
    
    Args:
        points: Lista de puntos de control (mínimo 2)
        duration: Duración total de la animación en segundos
        loop: Si la animación se repite automáticamente
    """
    
    __slots__ = ('_points', '_duration', '_time', '_loop', '_coefficients', '_step')
    
    def __init__(self, points: List[Union[Tuple[float, float], Vector2]], 
                 duration: float = 1.0, loop: bool = False):
        if len(points) < 2:
            raise ValueError("Se requieren al menos 2 puntos de control")
            
        self._points = [Vector2(p) for p in points]
        self._duration = max(duration, 0.001)
        self._time = 0.0
        self._loop = loop
        self._coefficients = self._precalculate_coefficients()
        self._step = 1.0 / self._duration

    def _precalculate_coefficients(self) -> List[float]:
        """Calcula los coeficientes binomiales una sola vez"""
        n = len(self._points) - 1
        return [comb(n, i) for i in range(n + 1)]

    def reset(self) -> None:
        """Reinicia la animación al estado inicial"""
        self._time = 0.0

    @property
    def completed(self) -> bool:
        """Indica si la animación ha finalizado (solo en modo no-loop)"""
        return self._time >= 1.0 and not self._loop

    def update(self, dt: float) -> Vector2:
        """
        Actualiza la posición en la curva.
        
        Args:
            dt: Tiempo transcurrido en segundos
            
        Returns:
            Vector2: Posición actual en la curva
        """
        self._time += dt * self._step
        
        if self._loop:
            self._time %= 1.0
        else:
            self._time = min(self._time, 1.0)

        return self._calculate_position(self._time)

    def _calculate_position(self, t: float) -> Vector2:
        """Cálculo optimizado usando pre-multiplicación de coeficientes"""
        t = max(0.0, min(t, 1.0))
        n = len(self._points) - 1
        result = Vector2(0, 0)
        
        for i in range(n + 1):
            coeff = self._coefficients[i] * (t ** i) * ((1 - t) ** (n - i))
            result += self._points[i] * coeff
            
        return result

    @property
    def position(self) -> Vector2:
        """Posición actual en la curva (interpolación suave)"""
        return self._calculate_position(self._time)

    @property
    def progress(self) -> float:
        """Progreso de la animación en rango [0, 1]"""
        return self._time

    @progress.setter
    def progress(self, value: float):
        """Establece el progreso de la animación manualmente"""
        self._time = max(0.0, min(float(value), 1.0))

class Second_Order_Dinamics:
    """
    Sistema de dinámica de segundo orden para animaciones fluidas y realistas.
    
    Parámetros:
        f: Frecuencia (Hz) - Controla la velocidad de la animación
        z: Factor de amortiguamiento - Evita oscilaciones (0 < z < 1)
        r: Respuesta inicial - 0 para empezar suave, 1 para inicio instantáneo
        coord: Posición inicial (Tuple[float, float] o Vector2)
    """
    __slots__ = ('_pi', '_k1', '_k2', '_k3', 'xp', 'y', 'yd', '_dt_crit', '_last_time')
    
    def __init__(self, f: float, z: float, r: float, coord: Union[Tuple[float, float], Vector2]):
        # Constantes del sistema
        self._pi = pi
        self._k1 = z / (self._pi * f)
        self._k2 = 1 / ((2 * self._pi * f) ** 2)
        self._k3 = r * z / (2 * self._pi * f)

        # Estado inicial
        self.xp = Vector2(coord)
        self.y = Vector2(coord)
        self.yd = Vector2(0.0, 0.0)
        
        # Ajuste para paso de tiempo variable
        self._dt_crit = 0.05  # Paso crítico para estabilidad
        self._last_time = None

    def update(self, target: Union[Tuple[float, float], Vector2], dt: float= None) -> Vector2:
        """
        Actualiza el sistema dinámico usando integración estable de Verlet.
        
        Args:
            target: Posición objetivo actual
            dt: Tiempo delta desde la última actualización (en segundos)
            
        Returns:
            Vector2: Nueva posición suavizada
        """
        if dt is None:
            dt = 1.0 / 60.0  # Asume 60 FPS como caso base
        else:
            dt = min(dt, 0.05)  # Limita a 20 FPS mínimo para estabilidad
        # Manejo automático de dt para aplicaciones en tiempo real
        if dt > self._dt_crit:
            dt = self._dt_crit
        
        target_vec = Vector2(target)
        
        # Cálculo de velocidad objetivo si no se proporciona
        xd = (target_vec - self.xp) / dt
        self.xp = target_vec
        
        # Integración numérica estabilizada
        self.y = self.y + self.yd * dt
        self.yd = self.yd + (target_vec + xd * self._k3 - self.y - self.yd * self._k1) * (dt / self._k2)
        
        return self.y

    @property
    def position(self) -> Tuple[float, float]:
        return (self.y.x, self.y.y)
