import math
from typing import Optional, Tuple, TypedDict

from .maths import left_top_width_height, Rect, rect_colition

class ObjectInfo(TypedDict):
    rect: Rect
    aditional_info: dict
    zones: set[tuple[int,int]]

class Zone_node:
    def __init__(self, left, top, width, height):
        self.rect: Rect = Rect(left, top, width, height)
        self.objs: set[str|int] = set()
    def get_objs_ids(self) -> set[str|int]:
        return self.objs
    def __str__(self) -> str:
        return f"Zone_node(pos={self.rect.left},{self.rect.top}, objs={len(self.objs)})"
    def __repr__(self) -> str:
        return self.__str__()


class Collision_handler:
    def __init__(self, zone_size: Tuple[int,int], node_size: int):
        self.zone_size: Tuple[int,int] = zone_size
        self.node_size: int = node_size
        self.num_nodes: Tuple[int,int] = (math.ceil(self.zone_size[0]/self.node_size),math.ceil(self.zone_size[1]/self.node_size))

        self.objects: dict[str|int|float,ObjectInfo] = {}

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
            self.zone_matrix.append(l.copy())

    def clear(self):
        for y in self.zone_matrix:
            for x in y:
                x.objs.clear()
        self.objects.clear()
    def add_element(self, id_obj, rect: left_top_width_height, aditional_info: Optional[dict] = None, **kwargs):
        if aditional_info is None:
            aditional_info = {}
        rect = Rect(*rect)



        row_min = max(0, rect.top // self.node_size)
        row_max = min(self.num_nodes[1] - 1, (rect.top + rect.height - 1) // self.node_size)
        col_min = max(0, rect.left // self.node_size)
        col_max = min(self.num_nodes[0] - 1, (rect.left + rect.width - 1) // self.node_size)

        zones = set()
        for y in range(int(row_min), int(row_max) + 1):
            for x in range(int(col_min), int(col_max) + 1):
                self.zone_matrix[y][x].objs.add(id_obj)
                zones.add((x, y))

        self.objects[id_obj] = {"rect": rect, "aditional_info": aditional_info, "zones": zones}


    def del_element(self,id_obj):
        for zone in self.objects[id_obj]["zones"]:
            self.zone_matrix[zone[1]][zone[0]].objs.discard(id_obj)
        return self.objects.pop(id_obj)

    def move_obj(self,id_obj,r):
        obj = self.del_element(id_obj)
        self.add_element(id_obj, r, obj["aditional_info"])

    def get_all_zones_rects(self):
        "Return : gets all zones rects"
        lista = []
        for y in self.zone_matrix:
            for x in y:
                lista.append(x.rect)
        return lista

    def get_all_objects(self):
        "Return : gets all objects"
        return self.objects.values()

    def get_zones_rect_in(self, id_obj):
        "Return : gets zones colliding with the element"
        lista = set()
        for zone in self.objects[id_obj]["zones"]:
            lista.add(self.zone_matrix[zone[1]][zone[0]].rect)
        return lista

    def get_rects_in_zone(self, id_obj) -> set:
        "Return : the list of blocks in the zones collinding"

        zones = self.objects[id_obj]["zones"]
        lista = set()
        for zone in zones:
            for obj in self.zone_matrix[zone[1]][zone[0]].objs:
                if obj != id_obj:
                    lista.add(self.objects[obj]["rect"])
        return lista

    def get_objects_in_zone(self, id_obj) -> set:
        "Return : the list of objects in the zones collinding"

        zones = self.objects[id_obj]["zones"]
        lista = set()
        for zone in zones:
            for obj in self.zone_matrix[zone[1]][zone[0]].objs:
                if obj != id_obj:
                    lista.add(obj)
        return lista

    def get_collides(self, id_obj):
        "Return : the list of colliding elements"
        objs = self.get_objects_in_zone(id_obj)
        lista = set()
        for obj in objs:
            if rect_colition(self.objects[id_obj]["rect"], self.objects[obj]["rect"]):
                lista.add(obj)
        return lista

    def __getitem__(self, key):
        return self.objects[key]
    def __len__(self):
        return len(self.objects)