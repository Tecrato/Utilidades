"""Tests de `Utilidades.maths`: puros, sin pygame y sin tocar el disco."""
import math

import pytest

from Utilidades.constants import Rect
from Utilidades.maths import (
    Angulo,
    Angulo_radians,
    Angulo_solo,
    Hipotenusa,
    LinearRegressionSimple,
    Vector2,
    calcular_pendiente,
    fibonacci,
    format_size_bits_to_bytes_str,
    line_to_polygon_intersection,
    lineal_interception_func,
    notacion_cientifica,
    recta_entre_puntos,
    rect_collision,
    rect_get_center,
)


# ==================== rect_collision ====================

def test_rect_collision():
    assert rect_collision((0, 50, 50, 50), (51, 50, 50, 50)) == False
    assert rect_collision((100, 105, 50, 50), (0, 50, 50, 50)) == False
    assert rect_collision((51, 50, 50, 50), (0, 50, 50, 50)) == False
    assert rect_collision((0, 0, 50, 50), (0, 150, 50, 50)) == False
    assert rect_collision((0, 0, 50, 50), (0, 100, 50, 50)) == False
    assert rect_collision((0, 0, 50, 50), (0, 75, 50, 50)) == False

    assert rect_collision((0, 50, 50, 50), (45, 50, 50, 50)) == True
    assert rect_collision((0, 50, 50, 50), (49, 50, 50, 50)) == True
    assert rect_collision((10, 50, 50, 50), (10, 50, 50, 50)) == True
    assert rect_collision((40, 50, 50, 50), (0, 10, 50, 50)) == True

    assert rect_collision((0, 0, 10, 10), (0, 0, 50, 50)) == True

    assert rect_collision((-47, -50, 50, 800), (0, 0, 100, 100)) == True


def test_rect_collision_acepta_rect():
    """La tupla (L, T, W, H) y el `Rect` del paquete son intercambiables."""
    assert rect_collision(Rect(0, 0, 10, 10), Rect(5, 5, 10, 10))
    assert not rect_collision(Rect(0, 0, 10, 10), (10, 0, 10, 10))
    assert rect_collision(Rect(0, 0, 10, 10), (9, 9, 10, 10))


def test_rect_get_center():
    assert rect_get_center((0, 0, 10, 20)) == (5.0, 10.0)
    assert rect_get_center((10, 10, 40, 40)) == (30.0, 30.0)


# ==================== ángulos y distancias ====================

def test_hipotenusa():
    assert Hipotenusa((0, 0), (3, 4)) == pytest.approx(5.0)
    assert Hipotenusa((1, 2, 3), (4, 5, 6)) == pytest.approx(math.sqrt(27))
    assert Hipotenusa((2, 2), (2, 2)) == 0


def test_hipotenusa_dimensiones_distintas():
    with pytest.raises(ValueError):
        Hipotenusa((0, 0), (1, 2, 3))


def test_angulo_en_grados():
    assert Angulo((0, 0), (3, 4)) == pytest.approx(53.13010235415599)
    assert Angulo((2, 2), (2, 5)) == pytest.approx(90.0)
    assert Angulo((0, 0), (-5, 0)) == pytest.approx(180.0)


def test_angulo_mismo_punto():
    with pytest.raises(ValueError):
        Angulo((1, 1), (1, 1))


def test_angulo_radians():
    assert Angulo_radians((2, 2), (2, 5)) == pytest.approx(math.pi / 2)
    assert Angulo_radians((0, 0), (-5, 0)) == pytest.approx(math.pi)


def test_angulo_solo():
    assert Angulo_solo((1, 0)) == pytest.approx(0.0)
    assert Angulo_solo((0, 1)) == pytest.approx(90.0)
    assert Angulo_solo((0, -1)) == pytest.approx(270.0)


# ==================== formateo de números ====================

def test_format_size():
    assert format_size_bits_to_bytes_str(0) == '0.00 B'
    assert format_size_bits_to_bytes_str(1024) == '1.00 KB'
    assert format_size_bits_to_bytes_str(2_380_800) == '2.27 MB'
    assert format_size_bits_to_bytes_str(4 * 1024 ** 3) == '4.00 GB'


def test_format_size_negativo():
    with pytest.raises(ValueError):
        format_size_bits_to_bytes_str(-1)


def test_notacion_cientifica():
    assert notacion_cientifica(0) == '0x10^0'
    assert notacion_cientifica(1000) == '1x10^3'
    assert notacion_cientifica(2380800) == '2.38x10^6'
    assert notacion_cientifica(-9999) == '-9.99x10^3'


def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    assert fibonacci(50) == 12586269025


# ==================== rectas e intersecciones ====================

def test_recta_entre_puntos():
    m, b = recta_entre_puntos((2, 3), (5, 7))
    assert m == pytest.approx(4 / 3)
    assert b == pytest.approx(1 / 3)


def test_recta_entre_puntos_casos_especiales():
    assert recta_entre_puntos((2, 5), (2, 5)) == "Los puntos son iguales"
    assert recta_entre_puntos((3, 4), (3, 8)) == "Recta vertical x = 3"


def test_lineal_interception_func():
    x, y = lineal_interception_func(2, 1, -1, 3)
    assert x == pytest.approx(2 / 3)
    assert y == pytest.approx(7 / 3)


def test_lineal_interception_func_paralelas_y_coincidentes():
    assert lineal_interception_func(2, 1, 2, 3) is None
    assert lineal_interception_func(2, 1, 2, 1) == "Rectas coincidentes"


def test_line_to_polygon_intersection():
    cuadrado = [(0, 0), (10, 0), (10, 10), (0, 10)]
    cortes = line_to_polygon_intersection(((-5, 5), (15, 5)), cuadrado, (5, 5), 20)
    assert cortes == [(0.0, 5.0), (10.0, 5.0)]


def test_line_to_polygon_intersection_sin_corte():
    cuadrado = [(0, 0), (10, 0), (10, 10), (0, 10)]
    assert line_to_polygon_intersection(((-5, 50), (15, 50)), cuadrado, (5, 5), 20) == []


# ==================== regresión lineal ====================

def test_calcular_pendiente():
    assert calcular_pendiente([1, 2, 3], [2, 4, 6]) == pytest.approx((2.0, 0.0))
    assert calcular_pendiente([1, 2, 3], [1, 2, 3]) == pytest.approx((1.0, 0.0))


def test_calcular_pendiente_errores():
    with pytest.raises(ValueError):
        calcular_pendiente([1, 2], [1, 2, 3])
    with pytest.raises(ValueError):
        calcular_pendiente([], [])
    with pytest.raises(ValueError):        # todos los x iguales: pendiente infinita
        calcular_pendiente([5, 5, 5], [1, 2, 3])


def test_linear_regression_simple():
    regresion = LinearRegressionSimple([1, 2, 3], [2, 4, 6])
    assert regresion.predict(4) == pytest.approx(8.0)
    assert regresion.error == pytest.approx(0.0)


def test_linear_regression_simple_valida_las_listas():
    with pytest.raises(ValueError):
        LinearRegressionSimple([1, 2], [1])
    with pytest.raises(ValueError):
        LinearRegressionSimple([], [])


# ==================== Vector2 ====================

def test_vector2_aritmetica():
    assert tuple(Vector2(1, 2) + Vector2(3, 4)) == (4.0, 6.0)
    assert tuple(Vector2(1, 2) - Vector2(3, 4)) == (-2.0, -2.0)
    assert tuple(Vector2(1, 2) * 2) == (2.0, 4.0)
    assert tuple(2 * Vector2(1, 2)) == (2.0, 4.0)
    assert tuple(Vector2(2, 4) / 2) == (1.0, 2.0)
    assert tuple(-Vector2(1, 2)) == (-1.0, -2.0)


def test_vector2_longitud_y_normalizacion():
    v = Vector2(3, 4)
    assert v.length() == pytest.approx(5.0)
    assert v.magnitude() == pytest.approx(5.0)
    assert tuple(v.normalize()) == pytest.approx((0.6, 0.8))
    assert tuple(Vector2(0, 0).normalize()) == (0.0, 0.0)
    assert v.dot(Vector2(1, 0)) == pytest.approx(3.0)
    assert tuple(v.scale_to_length(10)) == pytest.approx((6.0, 8.0))


def test_vector2_rotar():
    assert tuple(Vector2(1, 0).rotate(90)) == pytest.approx((0.0, 1.0), abs=1e-9)
    assert tuple(Vector2(1, 0).rotate(180)) == pytest.approx((-1.0, 0.0), abs=1e-9)


def test_vector2_construccion():
    assert tuple(Vector2()) == (0.0, 0.0)
    assert tuple(Vector2((1, 2))) == (1.0, 2.0)     # desde tupla
    assert tuple(Vector2(Vector2(3, 4))) == (3.0, 4.0)
    assert Vector2.from_tuple((7, 8)).x == 7.0
    assert len(Vector2(1, 2)) == 2
    assert Vector2(1, 2)[1] == 2.0


def test_vector2_desde_un_escalar():
    """Un escalar construye `(n, n)`, como documenta la firma `__init__(x, y)`."""
    assert tuple(Vector2(5)) == (5.0, 5.0)
    assert tuple(Vector2(2.5)) == (2.5, 2.5)


def test_vector2_setters():
    v = Vector2(1, 2)
    v.x = 10
    v.y = 20
    assert (v.x, v.y) == (10.0, 20.0)
    v[0] = 3
    assert v.x == 3.0
