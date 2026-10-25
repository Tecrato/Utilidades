"""Tests de la parte de `Utilidades` que no depende de pygame.

Se ejecutan desde `site-packages` con:

    python -m pytest Utilidades/test
"""
import sys
from pathlib import Path

# site-packages (este archivo vive en Utilidades/test/)
SITE_PACKAGES = Path(__file__).resolve().parents[2]
if str(SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(SITE_PACKAGES))
