"""Tests de `Utilidades.Animaciones` y `Utilidades.Animator`.

Todo se mide con `dt` explícito, así que no depende de la velocidad de la máquina.
"""
import pytest

from Utilidades.Animaciones import (
    Curva_de_Bezier,
    Second_Order_Dynamics,
    Simple_acceleration,
)
from Utilidades.Animator import Animator


# ==================== Curva_de_Bezier ====================

def test_bezier_de_un_segundo_termina_en_un_segundo():
    curva = Curva_de_Bezier(timer=1, points=[(0, 0), (100, 0)])
    for _ in range(61):                 # 61 y no 60: 60 * (1/60) deja error de float
        curva.update(1 / 60)
    assert curva.is_finished()
    assert curva.get_pos().x == pytest.approx(100)
    assert curva.get_pos().y == pytest.approx(0)


def test_bezier_necesita_dos_puntos():
    with pytest.raises(ValueError):
        Curva_de_Bezier(1, [(0, 0)])


def test_bezier_set_sitúa_el_progreso():
    curva = Curva_de_Bezier(timer=1, points=[(0, 0), (100, 0)])
    curva.set(0.5)
    assert curva.update(0).x == pytest.approx(50)
    assert not curva.is_finished()


def test_bezier_no_pasa_del_final():
    curva = Curva_de_Bezier(timer=1, points=[(0, 0), (100, 0)], extra_time=1)
    curva.update(10)                    # un frame gigante
    assert curva.is_finished()
    assert curva.get_pos().x == pytest.approx(100)


# ==================== Simple_acceleration ====================

def test_simple_acceleration_es_independiente_del_framerate():
    """Regresión de UNITS-01: `update` tenía que reenviar el `dt`."""
    a_60 = Simple_acceleration(60, (1, 0), (0, 0))
    for _ in range(60):
        a_60.update(1 / 60)

    a_144 = Simple_acceleration(60, (1, 0), (0, 0))
    for _ in range(144):
        a_144.update(1 / 144)

    assert a_60.pos.x == pytest.approx(60, abs=1e-9)
    assert a_144.pos.x == pytest.approx(60, abs=1e-9)


def test_simple_acceleration_sin_dt_equivale_a_un_frame():
    a = Simple_acceleration(5, (1, 0), (0, 0))
    a.update()
    assert a.pos.x == pytest.approx(5)


# ==================== Second_Order_Dynamics ====================

def test_second_order_dynamics_llega_al_objetivo():
    sistema = Second_Order_Dynamics(1, 1, 0, (0, 0))
    for _ in range(120):
        sistema.update((100, 0), 1 / 60)
    assert sistema.position[0] == pytest.approx(100, abs=0.1)
    assert sistema.position[1] == pytest.approx(0, abs=1e-9)


def test_second_order_dynamics_arranca_con_r_cero():
    """Con r=0 no hay salto inicial: el primer frame solo carga velocidad."""
    sistema = Second_Order_Dynamics(1, 1, 0, (0, 0))
    assert sistema.position == (0.0, 0.0)
    sistema.update((100, 0), 1 / 60)
    assert sistema.position == (0.0, 0.0)
    sistema.update((100, 0), 1 / 60)
    assert 0 < sistema.position[0] < 100


def test_second_order_dynamics_acota_el_dt():
    """Un dt enorme (> 0.05 s) se recorta para no explotar."""
    lento = Second_Order_Dynamics(1, 1, 0, (0, 0))
    lento.update((100, 0), 10)
    normal = Second_Order_Dynamics(1, 1, 0, (0, 0))
    normal.update((100, 0), 0.05)
    assert lento.position == pytest.approx(normal.position)


# ==================== Animator ====================

def test_animator_ejecuta_y_retira_la_animacion():
    animator = Animator()
    hechos = []
    animator.add_animation(lambda: hechos.append(1), delay=0.1)

    animator.update(0.05)
    assert hechos == []

    animator.update(0.05)
    assert hechos == [1]
    assert animator.list_funcs == []


def test_animator_repite():
    animator = Animator()
    hechos = []
    animator.add_animation(lambda: hechos.append(1), delay=0.1, repetitions=3)
    for _ in range(4):
        animator.update(0.1)
    assert len(hechos) == 3
    assert animator.list_funcs == []


def test_animator_clear():
    animator = Animator()
    animator.add_animation(lambda: None, delay=10)
    animator.clear()
    assert animator.list_funcs == []


def test_animator_conserva_lo_que_aun_no_dispara():
    """Regresión: las animaciones que aún no han disparado no se borran."""
    animator = Animator()
    pendiente = []
    dispara = []
    animator.add_animation(lambda: pendiente.append(1), delay=10)
    animator.add_animation(lambda: dispara.append(1), delay=0.1)
    animator.add_animation(lambda: dispara.append(2), delay=0.1)

    animator.update(0.6)

    assert len(animator.list_funcs) == 1
    assert animator.list_funcs[0]["delay"] == 10
