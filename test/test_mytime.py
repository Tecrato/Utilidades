"""Tests de `Utilidades.mytime`: regresión de `Deltatime` y utilidades de tiempo."""
import pytest

from Utilidades.mytime import Deltatime, format_date, func_exec_time, tener_el_tiempo


class Reloj:
    """Sustituto de `time.perf_counter`: devuelve valores fijos y repite el último."""

    def __init__(self, *valores):
        self.valores = list(valores)

    def __call__(self):
        if len(self.valores) > 1:
            return self.valores.pop(0)
        return self.valores[0]


def con_reloj(monkeypatch, *valores):
    monkeypatch.setattr('Utilidades.mytime.time.perf_counter', Reloj(*valores))


# ==================== operaciones aritméticas ====================

def test_deltatime_operaciones():
    d = Deltatime()
    d.dt = 0.5
    assert d.dt == 0.5
    assert 1 - d == pytest.approx(0.5)
    assert d - 1 == pytest.approx(-0.5)
    assert d + 1 == pytest.approx(1.5)
    assert 1 + d == pytest.approx(1.5)
    assert 2 * d == pytest.approx(1.0)
    assert d * 2 == pytest.approx(1.0)
    assert d / 2 == pytest.approx(0.25)
    assert 2 / d == pytest.approx(4.0)


def test_deltatime_str():
    d = Deltatime()
    d.dt = 0.5
    assert str(d) == 'FPS: 60.0 dt: 0.5'


# ==================== medición ====================

def test_update_mide_con_perf_counter(monkeypatch):
    con_reloj(monkeypatch, 100.0, 100.02, 100.02)
    d = Deltatime()
    d.update()
    assert d.dt == pytest.approx(0.02)


def test_smoothfix_limita_los_saltos_largos(monkeypatch):
    """Si un frame se pasa de `smoothfix` frames, el dt se fija en 1/FPS."""
    con_reloj(monkeypatch, 0.0, 1.0, 1.0)
    d = Deltatime()
    d.update()
    assert d.dt == pytest.approx(1 / 60)


def test_multiplier_escala_el_dt(monkeypatch):
    con_reloj(monkeypatch, 0.0, 0.01, 0.01)
    d = Deltatime(multiplier=2.0)
    d.update()
    assert d.dt == pytest.approx(0.02)


def test_reset_reinicia_el_reloj(monkeypatch):
    """Regresión: `reset()` usaba `time.time()` y dejaba un dt gigante."""
    con_reloj(monkeypatch, 1000.0, 2000.0, 2000.02, 2000.02)
    d = Deltatime()
    d.reset()
    assert d.dt == 0
    d.update()
    assert d.dt == pytest.approx(0.02)


# ==================== format_date ====================

def test_format_date_completo():
    assert format_date(3661) == {'seg': 1, 'min': 1, 'hour': 1, 'day': 0, 'year': 0}


def test_format_date_cero():
    assert format_date(0) == {'seg': 0, 'min': 0, 'hour': 0, 'day': 0, 'year': 0}


def test_format_date_escalones():
    assert format_date(90, escalones=1) == {'seg': 30, 'min': 0, 'hour': 0, 'day': 0, 'year': 0}
    assert format_date(90, escalones=2)['min'] == 1
    assert format_date(90 * 60, escalones=3)['hour'] == 1
    assert format_date(86400, escalones=4)['day'] == 1
    assert format_date(86400 * 365, escalones=5)['year'] == 1


def test_format_date_escalones_invalidos():
    with pytest.raises(ValueError):
        format_date(10, escalones=0)
    with pytest.raises(ValueError):
        format_date(10, escalones=6)


# ==================== decoradores ====================

def test_tener_el_tiempo(capsys):
    @tener_el_tiempo
    def suma(a, b):
        return a + b

    assert suma(1, 2) == 3
    assert 'El tiempo fue' in capsys.readouterr().out


def test_func_exec_time(capsys):
    @func_exec_time
    def doble(x):
        return x * 2

    assert doble(4) == 8
    assert '(doble)' in capsys.readouterr().out
