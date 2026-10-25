"""Tests de `Utilidades.collision_handler`.

La invariante es la misma en todos: `objects[id]["zones"]` tiene que coincidir
exactamente con las celdas de `zone_matrix` que contienen ese id.
"""
from Utilidades.collision_handler import Collision_handler
from Utilidades.constants import Rect

TAM = 50


def zonas_esperadas(rect, tam=TAM):
    return {
        (x, y)
        for y in range(int(rect.top) // tam, (int(rect.top + rect.height) - 1) // tam + 1)
        for x in range(int(rect.left) // tam, (int(rect.left + rect.width) - 1) // tam + 1)
    }


def test_move_obj_mantiene_el_indice_consistente():
    h = Collision_handler((400, 400), TAM)      # la rejilla debe cubrir todos los rects del test
    for i in range(20):
        h.add_element(i, (i * 9, i * 7, 30, 30))

    h.move_obj(3, (120, 120, 30, 30))
    h.move_obj(7, (5, 190, 40, 9))              # cruza el borde inferior

    for id_obj, info in h.objects.items():
        r = info["rect"]
        esperadas = zonas_esperadas(r)
        assert info["zones"] == esperadas
        for (x, y) in esperadas:
            assert id_obj in h.zone_matrix[y][x].objs


def test_add_element_guarda_rect_y_zonas():
    h = Collision_handler((200, 200), TAM)
    h.add_element('a', (10, 10, 30, 30))

    assert h.objects['a']['rect'] == Rect(10, 10, 30, 30)
    assert h.objects['a']['zones'] == {(0, 0)}
    assert h.objects['a']['additional_info'] == {}
    assert 'a' in h.zone_matrix[0][0].objs


def test_add_element_acepta_rect():
    h = Collision_handler((200, 200), TAM)
    h.add_element('a', Rect(60, 60, 30, 30))
    assert h.objects['a']['rect'] == Rect(60, 60, 30, 30)


def test_get_collides():
    h = Collision_handler((200, 200), TAM)
    h.add_element('a', (0, 0, 40, 40))
    h.add_element('b', (100, 100, 40, 40))

    assert h.get_collides('a') == set()
    assert h.get_collides_of_external_rect((30, 30, 20, 20)) == {'a'}

    h.move_obj('b', (20, 20, 40, 40))
    assert h.get_collides('a') == {'b'}


def test_del_element_limpia_las_zonas():
    h = Collision_handler((100, 100), TAM)
    h.add_element(1, (0, 0, 40, 40), {"vida": 10})

    info = h.del_element(1)
    assert info['additional_info'] == {'vida': 10}
    assert 1 not in h.objects
    assert all(1 not in zona.objs for fila in h.zone_matrix for zona in fila)


def test_clear_vacia_todo():
    h = Collision_handler((100, 100), TAM)
    h.add_element(1, (0, 0, 40, 40))
    h.clear()
    assert len(h.objects) == 0
    assert all(len(zona.objs) == 0 for fila in h.zone_matrix for zona in fila)


def test_rects_y_objetos_de_una_zona():
    h = Collision_handler((100, 100), TAM)
    h.add_element('a', (0, 0, 20, 20))
    h.add_element('b', (5, 5, 20, 20))

    assert h.get_objects_in_zone('a') == {'b'}
    assert h.get_rects_in_zone('a') == {Rect(5, 5, 20, 20)}


def test_objetos_fuera_de_la_rejilla_se_recortan():
    """Un rect que se sale de la rejilla se limita a las celdas existentes."""
    h = Collision_handler((100, 100), TAM)      # 2x2 celdas
    h.add_element('a', (90, 90, 50, 50))        # se sale por abajo y por la derecha

    assert h.objects['a']['zones'] == {(1, 1)}
    assert 'a' in h.zone_matrix[1][1].objs


def test_len_y_getitem():
    h = Collision_handler((100, 100), TAM)
    h.add_element('a', (0, 0, 10, 10))
    assert len(h) == 1
    assert h['a']['rect'] == Rect(0, 0, 10, 10)
