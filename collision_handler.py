import math
from itertools import chain

from typing import Literal, Tuple, Optional, Callable, Any

from .maths import left_top_width_height, Rect, rect_colition, rect_get_center
from .logger import debug_print


class Arista:
    def __init__(self, node) -> None:
        self.node: Zone_node = node

class Zone_node:
    def __init__(self, left, top, width, height):
        self.rect: Rect = Rect(left, top, width, height)
        self.center = (self.rect[0]+(self.rect[2]/2),self.rect[1]+(self.rect[3]/2))
        self.adyacentes: list[Arista] = []
        self.objs: list[Tuple[str,Rect,list[Arista],dict]] = []
    def get_rect(self):
        return self.rect
    def get_rect_list(self):
        return self.objs
    def get_center(self):
        return self.center
    def clear(self):
        self.objs.clear()

    def del_element(self,id_obj: str):
        f = find(id_obj,self.objs)
        if not f:
            return
        for i,x in enumerate(f[2]):
            x.node.del_element(id_obj)
        for i,x in enumerate(self.objs):
            if x[0] == id_obj:
                return self.objs.pop(i)
    def __str__(self) -> str:
        return f"Zone_node(pos={self.rect.left},{self.rect.top}, objs={len(self.objs)})"
    def __repr__(self) -> str:
        return self.__str__()
    def __getitem__(self, key):
        return find(key,self.objs)


class Collision_handler:
    """
        add_element(id_obj: str|int,rect: left_top_width_height) -> add an element at the colition algorithm

        get_rect_list(id_obj: str|int) -> the list of blocks in the zones collinding with the element

        get_zones_in(id_obj: str|int) -> for get zones in of the element

        del_element(id_obj: str|int) -> del and element

        move_obj(id_obj: str|int) -> automatic \"del\" an \"add\"
    """
    def __init__(self, zone_size: Tuple[int,int], node_size: int, diagonal = True):
        self.zone_size: Tuple[int,int] = zone_size
        self.node_size: int = node_size
        self.diagonal = diagonal
        self.num_nodes: Tuple[int,int] = (math.ceil(self.zone_size[0]/self.node_size),math.ceil(self.zone_size[1]/self.node_size))

        self.last_elements: dict[str|int,Zone_node] = {}
        self.last_zone_added: Zone_node = None

        self.zone_matrix: list[list[Zone_node]] = []
        self.generate_zone_matrix()

    def generate_zone_matrix(self):
        self.zone_matrix.clear()

        for y in range(self.num_nodes[1]):
            l: list[Zone_node] = []
            for x in range(self.num_nodes[0]):
                top = self.node_size*y
                left = self.node_size*x
                n = Zone_node(left, top, self.node_size, self.node_size)
                l.append(n)
            self.zone_matrix.append(l)
        self.last_zone_added = self.zone_matrix[0][0]
        self.__set_adyacentes()
    def __set_adyacentes(self):
        for i, y in enumerate(self.zone_matrix):
            for i2, x in enumerate(y):
                for y2 in range(-1,2):
                    for x2 in range(-1,2):
                        if (y2 == 0 and x2 == 0):
                            continue
                        if (abs(y2) == abs(x2)) and not self.diagonal:
                            continue
                        if (i+y2<0 or i+y2>=self.num_nodes[1]) or (i2+x2<0 or i2+x2>=self.num_nodes[0]):
                            continue
                        x.adyacentes.append(Arista(self.zone_matrix[i+y2][i2+x2]))

    def clear(self):
        for y in self.zone_matrix:
            for x in y:
                x.clear()
        self.last_elements.clear()
        self.last_zone_added = self.zone_matrix[0][0]

    def add_element(self,id_obj,rect:left_top_width_height, aditional_info: dict = {}, **kwargs):
        """Aditional info es por si quieres guardar mas variables para ese rect, para despues no tener que hacer una conversion buscando
        en otra lista y volver a des-optimizar el proceso"""
        # rect = Rect(*rect)
        center = rect_get_center(rect)
        # initial_node = kwargs.get("initial_node",self.last_zone_added)
        initial_coords = (
            max(
                0,
                min(
                    self.num_nodes[0] - 1,
                    int((center[0]/self.zone_size[0])*(self.num_nodes[0]-1))
                )
            ), 
            max(
                0,
                min(
                    self.num_nodes[1] - 1,
                    int((center[1]/self.zone_size[1])*(self.num_nodes[1]-1))
                )
            )
        )
        initial_node = self.zone_matrix[initial_coords[1]][initial_coords[0]]
        actual_node = (math.dist(initial_node.center,center),initial_node)
        while True:
            most_close: Tuple = actual_node
            for x in actual_node[1].adyacentes:
                if (distancia := math.dist(x.node.center,center)) < actual_node[0]:
                    most_close = (distancia,x.node)
                    break
            
            if most_close[1] != actual_node[1]:
                actual_node = most_close
                continue
            if not rect_colition(rect, actual_node[1].rect):
                actual_node[1].objs.append((id_obj,rect,set(), aditional_info))
                self.last_elements[id_obj] = actual_node[1]
                break
            # aristas_tocadas = set()
            # zone_actual = actual_node[1]
            # zones_revisadas = set()
            # zones_faltantes = []





            # while True:
            #     for x in zone_actual.adyacentes:
            #         if x.node in zones_revisadas:
            #             continue
            #         zones_revisadas.add(x.node)
            #         if rect_colition(rect, x.node.rect):
            #             x.node.objs.append((id_obj,rect,set(), aditional_info))
            #             aristas_tocadas.add(x)
            #             if x.node not in zones_revisadas:
            #                 zones_faltantes.append(x.node)
            #     if not zones_faltantes:
            #         break
            #     zone_actual = zones_faltantes.pop()
            # # for x in actual_node[1].adyacentes:
            # #     if rect_colition(rect,x.node.rect):
            # #         x.node.objs.append((id_obj,rect,[], aditional_info))
            # #         aristas_tocadas.append(x)


            aristas_tocadas = self.get_aristas_colision(rect, actual_node[1])
            for x in aristas_tocadas:
                x.node.objs.append((id_obj,rect,set(), aditional_info))

            actual_node[1].objs.append((id_obj,rect,aristas_tocadas, aditional_info))
            self.last_elements[id_obj] = actual_node[1]
            self.last_zone_added = actual_node[1]
            break

    def get_aristas_colision(self, rect: Rect, zone: Zone_node, zones_visited: set = None ):
        if zones_visited is None:
            zones_visited = set()
        aristas = set()
        zones_visited.add(zone)
        for x in zone.adyacentes:
            if x.node in zones_visited:
                continue
            zones_visited.add(x.node)
            if rect_colition(rect, x.node.rect):
                aristas.add(x)
                for x in self.get_aristas_colision(rect, x.node, zones_visited):
                    aristas.add(x)
        return aristas

    def del_element(self,id_obj):
        obj = find(id_obj, self.last_elements[id_obj].objs)
        if not obj:
            return
        for arista in obj[2]:
            arista.node.del_element(id_obj)
        self.last_elements[id_obj].objs.remove(obj)
        self.last_elements.pop(id_obj)

    def move_obj(self,id_obj,r):
        if not id_obj in self.last_elements:
            self.last_elements[id_obj] = self.zone_matrix[0][0]
        a = self.last_elements[id_obj]
        last = self.last_elements[id_obj].del_element(id_obj)
        self.add_element(id_obj, r, last[3], initial_node=a)

    def get_rect_list(self, id_obj, all_info: bool = False):
        "Return : the list of blocks in the zones collinding"
        if all_info:
            lista = [x for x in self.last_elements[id_obj].objs]
        else:
            lista = [x[1] for x in self.last_elements[id_obj].objs]
        aristas = find(id_obj,self.last_elements[id_obj].objs)
        if aristas:
            if all_info:
                for x in aristas[2]:
                    for x in x.node.objs:
                        lista.append(x)
            else:
                for x in aristas[2]:
                    for x in x.node.objs:
                        lista.append(x[1])

        return lista
    
    def get_collides(self, id_obj, rect: Optional[Rect] = None, filter_func: Optional[Callable] = None, all_info: bool = False) -> list[tuple[str, Rect, dict]]:
        lista_rects = self.get_rect_list(id_obj, all_info=all_info)
        if filter_func:
            lista_rects = filter(filter_func, lista_rects)
        if not rect:
            rect = find(id_obj,self.last_elements[id_obj].objs)
            if not rect:
                return []
        list_collide = []
        set_collides_ids = set()

        for x in lista_rects:
            if all_info:
                new_rect = x[1]
                if new_rect[0] in set_collides_ids:
                    continue
                set_collides_ids.add(new_rect[0])
                if rect_colition(rect[1],new_rect) and not rect[1] == new_rect:
                    list_collide.append((x[0], x[1], x[3]))
            else:
                new_rect = x
                if new_rect in set_collides_ids:
                    continue
                set_collides_ids.add(new_rect)
                if rect_colition(rect[1],new_rect) and not rect[1] == new_rect:
                    list_collide.append(x)
                

        return list_collide
            
    def get_all_rects(self):# Tuple[Any,...]
        lista = {}
        for y in self.zone_matrix:
            for x in y:
                for z in x.objs:
                    if z[0] in lista:
                        continue
                    lista[z[0]] = (z[0],z[1],z[3])
        return lista.values()

    def get_zones_in(self, id_obj):
        "Return : gets zones colliding with the element"
        lista = [self.last_elements[id_obj].rect]
        aristas = find(id_obj,self.last_elements[id_obj].objs)
        if aristas:
            for x in aristas[2]:
                lista.append(x.node.rect)
        return lista

    def get_all_zones_rects(self):
        lista = []
        for y in self.zone_matrix:
            for x in y:
                lista.append(x.rect)
        return lista


def find(txt,lista: list[Tuple[str,Rect,list[Arista], dict]]) -> Tuple[str, Rect, list[Arista], dict] | Literal[False]:
    for i,x in enumerate(lista):
        if x[0] == txt:
            return x
    return False
