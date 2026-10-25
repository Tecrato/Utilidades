"""Tests de `Utilidades.multithread`.

Los dos que importan son regresiones: el semáforo que se colgaba y el registro de
hilos que dejaba ids fantasma. Los tiempos son cortos a propósito, pero los
timeouts son holgados para que no fallen en una máquina cargada.
"""
import time

import pytest

from Utilidades.multithread import Funcs_pool, Interval_funcs, Semaforo


# ==================== Semaforo ====================

def test_semaforo_no_se_cuelga():
    s = Semaforo(1, 1)
    assert s.acquire(timeout=0.1)
    assert not s.acquire(timeout=0.1)     # el segundo espera, no entra
    s.release()
    assert s.acquire(timeout=0.1)


def test_semaforo_sin_bloqueo():
    s = Semaforo(1, 1)
    assert s.acquire(blocking=False)
    assert not s.acquire(blocking=False)


def test_semaforo_no_permite_liberar_de_mas():
    s = Semaforo(1, 1)
    with pytest.raises(ValueError):
        s.release()


def test_semaforo_de_conteo():
    s = Semaforo(3, 3)
    for _ in range(3):
        assert s.acquire(timeout=0.1)
    assert not s.acquire(timeout=0.05)
    s.release()
    assert s.acquire(timeout=0.1)


def test_semaforo_libera_desde_otro_hilo():
    s = Semaforo(1, 1)
    assert s.acquire(timeout=0.1)

    def liberar():
        time.sleep(0.02)
        s.release()

    import threading
    hilo = threading.Thread(target=liberar)
    hilo.start()
    assert s.acquire(timeout=1)          # espera de verdad hasta el release
    hilo.join()


# ==================== Funcs_pool ====================

def test_funcs_pool_limpia_el_registro():
    pool = Funcs_pool()
    contador = []

    def tarea():
        time.sleep(0.01)
        contador.append(1)

    pool.add('tarea', tarea, tarea)
    pool.start('tarea')
    pool.join('tarea', timeout=5)

    assert contador == [1, 1]
    assert pool.running['tarea'] == {}
    assert pool.running_ids['tarea'] == []


def test_funcs_pool_se_puede_reusar():
    pool = Funcs_pool()
    contador = []

    def tarea():
        contador.append(1)

    pool.add('tarea', tarea)
    for _ in range(3):
        pool.start('tarea')
        pool.join('tarea', timeout=5)

    assert len(contador) == 3
    assert pool.running_ids['tarea'] == []


@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_funcs_pool_libera_el_id_aunque_la_funcion_falle():
    pool = Funcs_pool()

    def revienta():
        raise RuntimeError('fallo esperado')

    pool.add('tarea', revienta)
    pool.start('tarea')
    pool.join('tarea', timeout=5)

    assert pool.running['tarea'] == {}
    assert pool.running_ids['tarea'] == []


def test_funcs_pool_alias_repetido():
    pool = Funcs_pool()
    pool.add('tarea', lambda: None)
    with pytest.raises(Exception):
        pool.add('tarea', lambda: None)


def test_funcs_pool_alias_desconocido():
    pool = Funcs_pool()
    with pytest.raises(Exception):
        pool.start('no-existe')


# ==================== Interval_funcs ====================

def test_interval_funcs_arranca_y_para():
    ticks = []
    intervalos = Interval_funcs()
    intervalos.add('tic', lambda: ticks.append(1), time=0.01, start=True)
    time.sleep(0.05)

    assert intervalos.join('tic', timeout=5)
    ejecutados = len(ticks)
    assert ejecutados >= 1

    time.sleep(0.05)                      # ya parado: no debe crecer
    assert len(ticks) == ejecutados


def test_interval_funcs_no_duplica_hilos():
    intervalos = Interval_funcs()
    intervalos.add('tic', lambda: None, time=0.01)
    assert intervalos.start_task('tic') is True
    assert intervalos.start_task('tic') is False     # ya hay uno vivo
    assert intervalos.join('tic', timeout=5) is True


def test_interval_funcs_join_desconocido():
    intervalos = Interval_funcs()
    assert intervalos.join('no-existe', timeout=0.1) is False
    assert intervalos.stop_task('no-existe') is False


def test_interval_funcs_alias_repetido():
    intervalos = Interval_funcs()
    intervalos.add('tic', lambda: None)
    with pytest.raises(AttributeError):
        intervalos.add('tic', lambda: None)


def test_interval_funcs_start_desconocido():
    intervalos = Interval_funcs()
    with pytest.raises(KeyError):
        intervalos.start_task('no-existe')


def test_timer_ejecuta_una_sola_vez():
    hechos = []
    intervalos = Interval_funcs()
    intervalos.timer('uno', lambda: hechos.append(1), time=0.01)
    time.sleep(0.1)
    assert hechos == [1]
