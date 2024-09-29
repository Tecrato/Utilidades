from .maths import Angulo, Hipotenuza, format_size_bits_to_bytes, UNIDADES_BYTES
from .mytime import Deltatime, tener_el_tiempo, format_date
from .optimize import memosize
from .multithread import Funcs_pool, Semaforo
from .web_tools import check_update, get_mediafire_url, Download
from .Animaciones import Simple_acceleration, Curva_de_Bezier, Second_Order_Dinamics
# from .tinify_API import Compress_img
# from .image import Image

from . import win32_tools


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