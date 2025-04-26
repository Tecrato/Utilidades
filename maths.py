import math
from typing import Union, Tuple, List, Literal, Callable, Self, Iterable
from typing import overload

def Hipotenuza(vector1, vector2) -> int:
    """
    Calcula la distancia euclídea entre dos vectores numéricos de igual dimensión.

    Args:
        vector1 (Iterable[float]): Primer vector (ej. [1.2, 3.5, 4.0])
        vector2 (Iterable[float]): Segundo vector de la misma dimensión

    Returns:
        float: Distancia entre los vectores

    Raises:
        ValueError: Si los vectores tienen dimensiones diferentes

    Ejemplo:
        >>> Hipotenuza([0, 0], [3, 4])
        5.0
        >>> Hipotenuza((1, 2, 3), (4, 5, 6))
        5.196152422706632
    """
    if len(vector1) != len(vector2):
        raise ValueError(f"Vectores de dimensiones diferentes: {len(vector1)} vs {len(vector2)}")
    return math.dist(vector1,vector2)

def Angulo(
    punto_origen: Union[Tuple[float, float], list[float]],
    punto_destino: Union[Tuple[float, float], list[float]]
) -> float:
    """
    Calcula el ángulo polar (en grados) entre dos puntos en un plano 2D.
    El ángulo se mide desde el eje X positivo en sentido antihorario.

    Args:
        punto_origen (Union[Tuple[float, float], list[float]]): Coordenadas (x, y) del punto de origen
        punto_destino (Union[Tuple[float, float], list[float]]): Coordenadas (x, y) del punto destino

    Returns:
        float: Ángulo en grados en el rango [0, 360)

    Raises:
        ValueError: Si los puntos no son 2D

    Ejemplos:
        >>> Angulo((0, 0), (3, 4))
        53.13010235415599
        >>> Angulo((2, 2), (2, 5))
        90.0
        >>> Angulo((0, 0), (-5, 0))
        180.0
    """
    
    # Validación de inputs
    if len(punto_origen) != 2 or len(punto_destino) != 2:
        raise ValueError("Ambos puntos deben ser coordenadas 2D numéricas")
    # Cálculo del vector diferencia
    dx = punto_destino[0] - punto_origen[0]
    dy = punto_destino[1] - punto_origen[1]
    angulo_grados = math.degrees(math.atan2(dy, dx)) % 360.0

    return angulo_grados

def format_size_bits_to_bytes_str(size: int | float) -> str:
    """
    Convierte bits a cadena legible usando unidades binarias (IEC).
    Args:
        size (int/float): Tamaño en bits (ej. 10_000_000)
        
    Ejemplos:
        >>> format_size_bytes(2_380_800)
        '2.27 MB'
        >>> format_size_bytes(1_048_576)
        '1.00 MB'
    """
    UNIDADES = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    BASE = 1024  # Sistema binario

    # Validación
    if size < 0:
        raise ValueError("El tamaño no puede ser negativo")
    unit_index = 0
    while size >= BASE and unit_index < len(UNIDADES) - 1:
        size /= BASE
        unit_index += 1
    
    return f"{size:.2f} {UNIDADES[unit_index]}"


def notacion_cientifica(n: int) -> str:
    """
    Convierte un número entero a notación científica **sin usar floats**, 
    evitando OverflowError y manteniendo el formato original pero mejorado.
    
    Args:
        n (int): Número entero (positivo, negativo o cero)
    
    Returns:
        str: Notación científica estilo "2.38x10^6"
    
    Ejemplos:
        >>> notacion_cientifica(2380800)
        '2.38x10^6'
        >>> notacion_cientifica(-9999)
        '-9.99x10^3'
        >>> notacion_cientifica(1000)
        '1x10^3'
    """
    if n == 0:
        return "0x10^0"
    
    sign = "-" if n < 0 else ""
    s = str(abs(n))
    exponent = len(s) - 1
    
    # Parte decimal truncada (sin redondeo)
    decimal_part = s[1:4].ljust(3, '0')  # Rellena con ceros si es necesario
    decimal_part = decimal_part.rstrip('0')  # Elimina ceros finales
    
    # Formatea la parte decimal
    formatted_decimal = f".{decimal_part}" if decimal_part else ""
    
    return f"{sign}{s[0]}{formatted_decimal}x10^{exponent}"


def fibonacci(n: int) -> int:
    def _fast_doubling(n):
        if n == 0:
            return (0, 1)
        a, b = _fast_doubling(n >> 1)
        c = a * (b * 2 - a)
        d = a * a + b * b
        if n & 1:
            return (d, d + c)
        else:
            return (c, d)
    return _fast_doubling(n)[0]

def recta_entre_puntos(
    p1: Tuple[Union[int, float], Union[int, float]],
    p2: Tuple[Union[int, float], Union[int, float]]
) -> Union[str, Tuple[float, float]]:
    """
    Calcula la ecuación de la recta y = mx + b entre dos puntos.
    
    Args:
        p1: Tupla (x1, y1)
        p2: Tupla (x2, y2)
    
    Returns:
        - Si los puntos son idénticos: "Los puntos son iguales"
        - Si la recta es vertical: "Recta vertical x = {x}"
        - En otros casos: (m, b) donde y = mx + b
    
    Ejemplos:
        >>> calcular_recta_entre_puntos((2, 3), (5, 7))
        (1.3333333333333333, 0.3333333333333335)
        
        >>> calcular_recta_entre_puntos((3, 4), (3, 8))
        'Recta vertical x = 3'
        
        >>> calcular_recta_entre_puntos((2, 5), (2, 5))
        'Los puntos son iguales'
    """
    # Validación de puntos iguales
    if p1 == p2:
        return "Los puntos son iguales"
    
    if p1[0] == p2[0]:
        return f"Recta vertical x = {p1[0]}"
    
    x1, y1 = p1
    x2, y2 = p2
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    
    return (round(m, 10), round(b, 10))

def lineal_interception_func(
    m1: float, 
    b1: float, 
    m2: float, 
    b2: float
) -> Union[Tuple[float, float], str, None]:
    """
    Calcula el punto de intersección entre dos rectas y = m1x + b1 e y = m2x + b2.
    
    Args:
        m1 (float): Pendiente de la primera recta
        b1 (float): Ordenada al origen de la primera recta
        m2 (float): Pendiente de la segunda recta
        b2 (float): Ordenada al origen de la segunda recta
    
    Returns:
        - Tuple[float, float]: (x, y) si hay una intersección única
        - "Rectas coincidentes": Si son la misma recta
        - None: Si son paralelas pero distintas
    
    Ejemplos:
        >>> lineal_interception_func(2, 1, -1, 3)
        (0.6666666666666666, 2.3333333333333335)
        
        >>> lineal_interception_func(2, 1, 2, 3)
        None
        
        >>> lineal_interception_func(2, 1, 2, 1)
        'Rectas coincidentes'
    """
    # Manejo de precisión decimal (opcional)
    TOLERANCIA = 1e-10
    
    # Caso 1: Rectas coincidentes
    if abs(m1 - m2) < TOLERANCIA and abs(b1 - b2) < TOLERANCIA:
        return "Rectas coincidentes"
    
    # Caso 2: Rectas paralelas
    if abs(m1 - m2) < TOLERANCIA:
        return None
    
    # Cálculo de intersección
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1  # También válido: y = m2 * x + b2
    
    return (round(x, 10), round(y, 10))  # Redondeo para evitar errores de precisión
def lineal_interception(
    p1: Tuple[float, float], 
    p2: Tuple[float, float], 
    p3: Tuple[float, float], 
    p4: Tuple[float, float]
) -> Union[Tuple[float, float], str, None]:
    """
    Calcula la intersección de dos líneas definidas por pares de puntos.
    
    Args:
        p1, p2: Puntos de la primera línea (x1, y1), (x2, y2)
        p3, p4: Puntos de la segunda línea (x3, y3), (x4, y4)
    
    Returns:
        - Tuple[float, float]: Coordenadas (x, y) de la intersección
        - "Rectas coincidentes": Si las líneas son idénticas
        - None: Si son paralelas y no se intersectan
    
    Ejemplos:
        >>> lineal_interception((0, 0), (2, 2), (0, 2), (2, 0))
        (1.0, 1.0)
        
        >>> lineal_interception((0, 0), (1, 1), (2, 2), (3, 3))
        "Rectas coincidentes"
        
        >>> lineal_interception((0, 0), (1, 0), (0, 1), (1, 1))
        None
    """
    # Tolerancia para errores de precisión
    TOL = 1e-10
    
    # Calcular coeficientes para la primera línea: A1x + B1y = C1
    A1 = p2[1] - p1[1]  # Δy
    B1 = p1[0] - p2[0]  # Δx inverso
    C1 = A1 * p1[0] + B1 * p1[1]
    
    # Calcular coeficientes para la segunda línea: A2x + B2y = C2
    A2 = p4[1] - p3[1]
    B2 = p3[0] - p4[0]
    C2 = A2 * p3[0] + B2 * p3[1]
    
    # Calcular determinantes
    det = A1 * B2 - A2 * B1
    det_x = C1 * B2 - C2 * B1
    det_y = A1 * C2 - A2 * C1
    
    # Caso 1: Líneas paralelas o coincidentes
    if abs(det) < TOL:
        # Verificar si son coincidentes
        if abs(det_x) < TOL and abs(det_y) < TOL:
            return "Rectas coincidentes"
        return None
    
    # Calcular punto de intersección
    x = det_x / det
    y = det_y / det
    
    # Verificar si el punto pertenece a ambos segmentos (opcional)
    # (Si solo te interesan las líneas infinitas, omite esta parte)
    """
    if not (min(p1[0], p2[0]) - TOL <= x <= max(p1[0], p2[0]) + TOL and
            min(p1[1], p2[1]) - TOL <= y <= max(p1[1], p2[1]) + TOL and
            min(p3[0], p4[0]) - TOL <= x <= max(p3[0], p4[0]) + TOL and
            min(p3[1], p4[1]) - TOL <= y <= max(p3[1], p4[1]) + TOL):
        return None
    """
    
    return (round(x, 10), round(y, 10))

def line_to_polygon_intersection(
    line: Tuple[Tuple[float, float], Tuple[float, float]],
    polygon: List[Tuple[float, float]],
    center: Tuple[float, float],
    max_radio: float
) -> List[Tuple[float, float]]:
    """
    Encuentra intersecciones entre una línea y un polígono usando:
    - Spatial hashing para descartar bordes lejanos
    - Precálculos de geometría analítica
    - Early exits para bordes no intersectantes
    
    Args:
        line: Tupla con dos puntos ((x1, y1), (x2, y2))
        polygon: Lista de vértices del polígono
        center: Centro de referencia para el radio máximo
        max_radio: Radio máximo desde el centro
    
    Returns:
        Lista de puntos de intersección ordenados por distancia al inicio de la línea
    """
    # 1. Precálculos de la línea
    (x1, y1), (x2, y2) = line
    line_dir = (x2 - x1, y2 - y1)
    line_length = math.hypot(line_dir[0], line_dir[1])
    
    # 2. Spatial hashing para bordes del polígono
    grid_size = max_radio * 0.5  # Tamaño de celda óptimo
    grid = {}
    
    # 3. Construcción de la grid
    cx, cy = center
    for i, (px, py) in enumerate(polygon):
        cell_x = int((px - cx) // grid_size)
        cell_y = int((py - cy) // grid_size)
        if (cell_x, cell_y) not in grid:
            grid[(cell_x, cell_y)] = []
        grid[(cell_x, cell_y)].append(i)
    
    # 4. Parámetros de la línea en forma paramétrica
    t_min, t_max = 0.0, 1.0
    intersections = []
    
    # 5. Búsqueda optimizada en celdas relevantes
    relevant_cells = get_relevant_cells(line, center, max_radio, grid_size)
    for cell in relevant_cells:
        if cell not in grid:
            continue
            
        for edge_idx in grid[cell]:
            p_prev = polygon[edge_idx - 1]
            p_current = polygon[edge_idx]
            
            # 6. Early exit por AABB
            if not aabb_intersect(line, (p_prev, p_current)):
                continue
                
            # 7. Cálculo eficiente de intersección
            intersect = line_segment_intersection(line, (p_prev, p_current))
            if intersect:
                distance_to_center = math.hypot(intersect[0]-center[0], intersect[1]-center[1])
                if distance_to_center <= max_radio:
                    t = ((intersect[0]-x1)*line_dir[0] + (intersect[1]-y1)*line_dir[1]) / (line_length**2)
                    intersections.append((t, intersect))
    
    # 8. Ordenar por posición en la línea
    return [p for t, p in sorted(intersections, key=lambda x: x[0])]

# Funciones auxiliares ---------------------------------------------------------

def get_relevant_cells(line, center, radius, cell_size):
    """Obtiene celdas intersectadas por el área de búsqueda"""
    cells = set()
    steps = int(radius // cell_size) + 2
    
    for dx in range(-steps, steps+1):
        for dy in range(-steps, steps+1):
            cells.add((int(dx), int(dy)))
    
    return cells

def aabb_intersect(line, segment):
    """Comprueba intersección de AABBs"""
    (lx1, ly1), (lx2, ly2) = line
    (sx1, sy1), (sx2, sy2) = segment
    
    return not (max(lx1, lx2) < min(sx1, sx2) or
                min(lx1, lx2) > max(sx1, sx2) or
                max(ly1, ly2) < min(sy1, sy2) or
                min(ly1, ly2) > max(sy1, sy2))

def line_segment_intersection(line, segment):
    """Versión optimizada de intersección línea-segmento"""
    (x1, y1), (x2, y2) = line
    (x3, y3), (x4, y4) = segment

    denom = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)
    if denom == 0:
        return None  # Paralelas

    u = ((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3)) / denom
    t = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)) / denom

    if 0 <= u <= 1 and 0 <= t <= 1:
        return (x1 + u*(x2 - x1), y1 + u*(y2 - y1))
    return None
    

def calcular_centroide(coordenadas: List[Tuple[Union[int, float], ...]]) -> List[float]:
    """
    Calcula el centroide (punto medio promedio) de un conjunto de coordenadas n-dimensionales.
    
    Args:
        coordenadas: Lista de tuplas con coordenadas. Todas deben tener la misma dimensión.
        
    Returns:
        Lista con la media de cada dimensión.
        
    Raises:
        ValueError: Si no hay coordenadas o tienen dimensiones inconsistentes.
        
    Ejemplos:
        >>> calcular_centroide([(1, 2), (3, 4), (5, 6)])
        [3.0, 4.0]
        
        >>> calcular_centroide([(0, 0, 0), (1, 2, 3), (2, 4, 6)])
        [1.0, 2.0, 3.0]
    """
    # Validación de entrada
    if not coordenadas:
        raise ValueError("Se requiere al menos una coordenada")
    
    dimension = len(coordenadas[0])
    if any(len(p) != dimension for p in coordenadas):
        raise ValueError("Todas las coordenadas deben tener la misma dimensión")
    
    # Cálculo vectorizado optimizado
    suma = [sum(dim) for dim in zip(*coordenadas)]
    n = len(coordenadas)
    
    return [round(val / n, 10) for val in suma]  # Redondeo para evitar errores de precisión


def calcular_integral(
    funcion: Callable[[float], float],
    a: float,
    b: float,
    metodo: Literal['simpson', 'trapezoidal', 'adaptive'] = 'simpson',
    tolerancia: float = 1e-6,
    max_profundidad: int = 20
) -> float:
    """
    Integración numérica adaptativa sin dependencias externas.
    
    Args:
        funcion: Función a integrar (debe recibir y retornar float)
        a: Límite inferior
        b: Límite superior
        metodo: 'simpson' (default), 'trapezoidal', o 'adaptive'
        tolerancia: Error relativo máximo permitido
        max_profundidad: Máxima recursión para métodos adaptativos

    Returns:
        float: Valor aproximado de la integral
        
    Ejemplos:
        >>> calcular_integral(lambda x: x**2, 0, 1)
        0.33333333333333337
    """
    def _simpson(f, a, b):
        """Regla de Simpson compuesta con 2 intervalos"""
        c = (a + b) / 2
        h = (b - a) / 6  # h = (b-a)/2 / 3
        return h * (f(a) + 4*f(c) + f(b))

    def _adaptativa(f, a, b, tol, prof, metodo):
        """Algoritmo adaptativo recursivo"""
        if prof <= 0:
            return metodo(f, a, b)
        
        # Calcula integral en intervalo completo y dividido
        c = (a + b) / 2
        integral_total = metodo(f, a, b)
        integral_mitad = metodo(f, a, c) + metodo(f, c, b)
        
        # Estimación de error
        error = abs(integral_total - integral_mitad)
        
        if error < 15 * tol:  # Factor de seguridad 15 para Simpson
            return integral_mitad + (integral_mitad - integral_total)/15
        else:
            tol_mitad = tol / 2
            return (_adaptativa(f, a, c, tol_mitad, prof-1, metodo) +
                    _adaptativa(f, c, b, tol_mitad, prof-1, metodo))

    # Selección de método
    metodo_calculo = {
        'simpson': _simpson,
        'trapezoidal': lambda f, a, b: (b - a) * (f(a) + f(b)) / 2,
        'adaptive': lambda f, a, b: _adaptativa(f, a, b, tolerancia, max_profundidad, _simpson)
    }.get(metodo.lower(), _simpson)

    # Llamada inicial
    return metodo_calculo(funcion, a, b)

class LinearRegressionSimple:
    def __init__(self, x, y):
        # Validación de las listas de entrada
        if len(x) != len(y):
            raise ValueError("Las listas de 'x' e 'y' deben tener la misma longitud.")
        if len(x) == 0:
            raise ValueError("Las listas no pueden estar vacías.")
        
        self.x = x
        self.y = y
        self.a, self.b = self.calcular_pendiente()  # Calcular pendiente e intersección
        self.error = self.calcular_error()  # Calcular error cuadrático medio
    
    def set_data(self, x, y):
        self.x = x
        self.y = y
        self.a, self.b = self.calcular_pendiente()  # Calcular pendiente e intersección
        self.error = self.calcular_error()  # Calcular error cuadrático medio

    def calcular_pendiente(self):
        x_sum = sum(self.x)
        y_sum = sum(self.y)
        xy_sum = sum(xi * yi for xi, yi in zip(self.x, self.y))
        xx_sum = sum(xi ** 2 for xi in self.x)
        n = len(self.x)
        
        # Cálculo de la pendiente (a) y la intersección (b)
        a = (n * xy_sum - x_sum * y_sum) / (n * xx_sum - x_sum ** 2)
        b = (y_sum - a * x_sum) / n
        
        return a, b

    def calcular_error(self):
        error = 0
        n = len(self.x)
        
        # Cálculo del error cuadrático medio (MSE)
        for i in range(n):
            y_pred = self.a * self.x[i] + self.b
            error += (self.y[i] - y_pred) ** 2
        
        return error / n

    def predict(self, x):
        # Predicción de valores de y basado en un valor de x dado
        return (self.a * x) + self.b
    
def calcular_pendiente(datos_x, datos_y):
    x,y,xy,xx,a,b = 0,0,0,0,0,0
    for l_x,l_y in zip(datos_x,datos_y):
        for x,y in zip(l_x,l_y):
            x += x
            y += y
            xy += x * y
            xx += x ** 2
    
    a = ((len(datos_x) * xy) - (x * y)) / ((len(datos_x) * xx) - (x ** 2))
    b = ((y - b * x) / len(datos_x))
    return a,b

class LinearRegressionMultiple:
    def __init__(self, learning_rate=0.01, iterations=5_000):
        self.learning_rate = learning_rate
        self.n_iter = iterations
        self.coef = None
        self.mean = None
        self.std = None
        self.is_fitted = False
    
    def _normalize(self, X, is_training=False):
        if not self.is_fitted or is_training:
            self.mean = [sum(col)/len(col) for col in zip(*X)]
            self.std = [
                (sum((x - mean)**2 for x in col)/len(col))**0.5 
                for col, mean in zip(zip(*X), self.mean)
            ]
        
        X_normalized = []
        for row in X:
            normalized_row = [
                (row[i] - self.mean[i])/self.std[i] if self.std[i] != 0 else 0 
                for i in range(len(row))
            ]
            X_normalized.append([1] + normalized_row)
        return X_normalized
    
    def fit(self, X, y, epochs=None):
        if not self.is_fitted:
            X_normalized = self._normalize(X, is_training=True)
            y = [float(val) for val in y]
            n_features = len(X_normalized[0])
            self.coef = [0.1] * n_features
            self.is_fitted = True
        else:
            X_normalized = self._normalize(X)
            y = [float(val) for val in y]
        
        for _ in range(epochs or self.n_iter):
            gradients = [0.0] * len(self.coef)
            for i in range(len(X_normalized)):
                prediction = sum(X_normalized[i][j] * self.coef[j] for j in range(len(self.coef)))
                error = prediction - y[i]
                for j in range(len(self.coef)):
                    gradients[j] += error * X_normalized[i][j]
            
            self.coef = [
                self.coef[j] - (self.learning_rate * gradients[j]/len(X_normalized)) 
                for j in range(len(self.coef))
            ]
    
    def predict(self, X_new):
        if not self.is_fitted:
            raise Exception("Modelo no entrenado")
        X_normalized = [
            (X_new[i] - self.mean[i])/self.std[i] 
            if self.std[i] != 0 else 0 
            for i in range(len(X_new))
        ]
        return sum(x * coef for x, coef in zip([1] + X_normalized, self.coef))

class Vector2:
    """Clase vectorial minimalista para operaciones 2D"""
    __slots__ = ('x', 'y')
    
    @overload
    def __init__(self, vector: Self): ...
    @overload
    def __init__(self, x: float = 0.0, y: float = 0.0): ...
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (Iterable)):
            self.x = args[0][0]
            self.y = args[0][1]
        elif len(args) == 1 and isinstance(args[0], (int,float)):
            self.x = args[0]
            self.y = args[0]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 0:
            self.x = 0
            self.y = 0
        else:
            raise ValueError('Invalid arguments')
    
    @classmethod
    def from_tuple(cls, data: Tuple[float, float]):
        return cls(data[0], data[1])
    
    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other[0], self.y + other[1])
    
    def __radd__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other[0], self.y + other[1])
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other[0], self.y - other[1])
    
    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __repr__(self):
        return f"Vector2({self.x:.2f}, {self.y:.2f})"

    def __getitem__(self, index):
        return (self.x,self.y)[index]
    
    def __len__(self):
        return 2
    