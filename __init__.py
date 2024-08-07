from .Animaciones import Curva_de_Bezier, Second_Order_Dinamics
from .Barras_progreso import Barra_de_progreso
from .maths import Angulo, Hipotenuza
from .mytime import Deltatime, tener_el_tiempo, format_date
from .particles import Particles
from .sparks import Spark
from .optimize import memosize
from .multithread import Funcs_pool, Semaforo
from .web_tools import check_update, get_mediafire_url
# from .tinify_API import Compress_img
# from .image import Image

from . import win32_tools
from . import GUI
from . import mini_GUI

from .texts import Text
from .texts import Button
from .texts import Input
from .texts import List
from .texts import Multi_list


from .figuras.poligono_regular import Poligono_regular
from .figuras.poligono_irregular import Poligono_irregular
from .figuras.engranajes import Engranaje


print(
    "\n"
    "Bienvenido a las utilidades para pygame, Hecho por Edouard Sandoval\n"
    "\n"
    "Para Empezar puedes copiar el codigo del archivo inicio aplicacion dentro de la libreria\n"
    "te facilitara el codigo necesario para iniciar la aplicacion por primera vez"
)