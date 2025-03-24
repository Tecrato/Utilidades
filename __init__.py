from .maths import (
    Angulo, 
    Hipotenuza, 
    format_size_bits_to_bytes_str,
    lineal_interception, 
    lineal_interception_func, 
    line_to_polygon_intersection, 
    recta_entre_puntos,
    Vector2,
    LinearRegressionSimple
)
from .mytime import Deltatime, tener_el_tiempo, format_date
from .multithread import Funcs_pool, Semaforo
from .web_tools import *
from .Animaciones import DynamicMovement, Curva_de_Bezier, Second_Order_Dinamics
from .logger import Logger, debug_print

import sys

if sys.platform == 'win32':
    from . import win32_tools
else:
    from . import linux_tools as win32_tools


from .figuras.poligono_regular import PoligonoRegular
from .figuras.poligono_irregular import PoligonoIrregular
from .figuras.engranajes import Engranaje


print(
    "Bienvenido a las Utilidades Variadas, Hecho por Edouard Sandoval\n"
)