import pygame as pag

class mini_GUI_admin:
    def __init__(self, limit: pag.Rect) -> None:
        self.__list = []
        self.__limit = limit
    
    def add(self,mini_GUI,func=None,raw_pos=None):
        self.__list.append({'GUI':mini_GUI,'func':func,'raw_pos':raw_pos})
        self.__list[-1]['GUI'].limits = self.limit
        self.__list[-1]['GUI'].direccion(self.__list[-1]['GUI'].rect)

    
    def draw(self, surface,pos):
        for x in self.__list:
            x['GUI'].draw(surface,pos)

    def click(self, pos):
        for i, g in sorted(enumerate(self.__list),reverse=True):
            result = g['GUI'].click(pos)
            if result == 'exit':
                self.__list.pop(i)
                return False
            elif result or result == 0:
                self.__list.pop(i)
                if g['func']: g['func'](result)
                return result
            elif self.__list[i]['GUI'].rect.collidepoint(pos):
                self.__list.pop(i)
                self.__list.append(g)
                return False
    
    def clear(self):
        self.__list.clear()
    
    @property
    def limit(self):
        return self.__limit
    @limit.setter
    def limit(self,limit):
        self.__limit = limit
        for x in self.__list:
            x['GUI'].limits = self.__limit
            if x['raw_pos']:
                x['GUI'].pos = x['raw_pos']
            else:
                x['GUI'].pos = x['GUI'].pos


