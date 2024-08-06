import pygame as pag
import sys
import datetime
import Utilidades as uti

TITLE: str = 'Program'
RESOLUCION = (800, 550)


class Clicker_game:
    def __init__(self) -> None:
        self.ventana: pag.Surface = pag.display.set_mode(RESOLUCION, pag.RESIZABLE|pag.DOUBLEBUF)
        self.ventana_rect: pag.Rect = self.ventana.get_rect()
        pag.display.set_caption(TITLE)
        
        # Variables necesarias
        self.drawing: bool = True
        self.draw_background: bool = True
        self.framerate: int = 60
        self.redraw: bool = True
        self.relog: pag.time.Clock = pag.time.Clock()
        self.updates: list[pag.Rect] = []
        self.background_color: tuple[int,int,int] = (20,20,20)

        # Otras variables
        ...
        ...

        # Variables por pantalla
        # Principal:
        self.list_to_draw: list[uti.Text|uti.Button|uti.Input|uti.Multi_list|uti.List] = []
        self.list_to_click: list[uti.Button] = []
        ...

        # Iniciar el programa
        self.load_resources()
        self.generate_objs()


        # Algoritmo para pasar de pantalla sin que esten unas dentro de otras
        self.screen_main_bool: bool = True
        ...                                         # Agregar variables booleanas para cada pantalla

        self.ciclo_general = [self.main_cycle]
        self.cicle_try = 0

        while self.cicle_try < 5:
            self.cicle_try += 1
            for x in self.ciclo_general:
                x()

    def load_resources(self):
        # Para cargar tu archivo json de configuraciones
        # Y alguna Base de datos si es necesario
        ... 

    def save_json(self):
        # Para guardar tu archivo json de configuraciones
        ... 

    # Donde se va a generar el texto, inputs, y demas cosas
    def generate_objs(self) -> None:
        # Cosas varias
        # uti.GUI.configs['fuente_simbolos'] = self.font_simbolos      ----   # Esto es para la GUI que retorna texto, mientras lo la uses no es obligatorio
        self.GUI_manager = uti.GUI.GUI_admin()
        self.Mini_GUI_manager = uti.mini_GUI.mini_GUI_admin(self.ventana_rect)

        # El resto de textos y demas cosas
        ...

    # Para mover los objetos denuevo, por ejemplo cuando la ventana cambie de tamaño
    def move_objs(self):
        ...

    # Para dibujar los objetos de las utilidades
    def draw_objs(self,lista):
        mx, my = pag.mouse.get_pos()
        if self.redraw:
            if self.draw_background:
                self.ventana.fill(self.background_color)
            for x in lista:
                if isinstance(x, uti.Button):
                    x.draw(self.ventana, (mx,my))
                elif isinstance(x, uti.Multi_list):
                    if x.listas[0].lista_palabras:
                        x.draw(self.ventana)
                else:
                    x.draw(self.ventana, False)
            self.GUI_manager.draw(self.ventana, (mx, my))
            self.Mini_GUI_manager.draw(self.ventana, (mx, my))
            pag.display.update()
            self.redraw = False
        else:
            self.updates.clear()
            for x in lista:
                if isinstance(x, uti.Button):
                    self.updates.append(x.draw(self.ventana, (mx,my)))
                elif isinstance(x, uti.Multi_list):
                    if self.lista_descargas.listas[0].lista_palabras:
                        self.updates.append(x.draw(self.ventana))
                else:
                    self.updates.append(x.draw(self.ventana))

            self.updates.append(self.GUI_manager.draw(self.ventana, (mx, my)))
            for x in self.Mini_GUI_manager.draw(self.ventana, (mx, my)):
                self.updates.append(x)

            self.updates = list(filter(lambda ele: isinstance(ele, pag.Rect),self.updates))

            pag.display.update(self.updates)
            
    def eventos_en_comun(self,evento):
        mx, my = pag.mouse.get_pos()
        if evento.type == pag.QUIT:
            pag.quit()
            sys.exit()
        elif evento.type == pag.KEYDOWN and evento.key == pag.K_F12:
            momento = datetime.datetime.today().strftime('%y%m%d_%f')
            pag.image.save(self.display,'screenshot_{}_{}.png'.format(TITLE,momento))
        elif evento.type == pag.WINDOWRESTORED:
            return True
        elif self.GUI_manager.active >= 0:
            if evento.type == pag.KEYDOWN and evento.key == pag.K_ESCAPE:
                self.GUI_manager.pop()
            elif evento.type == pag.MOUSEBUTTONDOWN and evento.button == 1:
                self.GUI_manager.click((mx, my))
            return True
        elif evento.type == pag.MOUSEBUTTONDOWN and evento.button == 1:
            if self.Mini_GUI_manager.click(evento.pos):
                return True
        elif evento.type == pag.MOUSEBUTTONDOWN and evento.button == 3:
            if self.Mini_GUI_manager.click(evento.pos):
                return True
        elif evento.type == pag.WINDOWMINIMIZED:
            self.drawing = False
            return True
        elif evento.type == pag.WINDOWFOCUSLOST:
            self.framerate = 30
            return True
        elif evento.type in [pag.WINDOWTAKEFOCUS, pag.WINDOWFOCUSGAINED,pag.WINDOWMAXIMIZED]:
            self.framerate = 60
            self.drawing = True
            return True
        elif evento.type in [pag.WINDOWRESIZED,pag.WINDOWMAXIMIZED,pag.WINDOWSIZECHANGED,pag.WINDOWMINIMIZED]:
            size = pag.display.get_window_size()
            self.ventana = pag.display.set_mode(size, pag.RESIZABLE|pag.DOUBLEBUF)
            self.ventana_rect = self.ventana.get_rect()

            self.move_objs()
            return True
        elif evento.type == pag.WINDOWSHOWN or evento.type == pag.WINDOWMOVED:
            size = pag.display.get_window_size()
            self.ventana = pag.display.set_mode(size, pag.RESIZABLE|pag.DOUBLEBUF)
            self.ventana_rect = self.ventana.get_rect()

            self.move_objs()
            return True
        return False
    
    def main_cycle(self):
        if self.screen_main_bool:
            self.cicle_try = 0
            self.redraw = True

        
        while self.screen_main_bool:
            self.relog.tick(self.framerate)

            mx, my = pag.mouse.get_pos()
            eventos = pag.event.get()
            self.GUI_manager.input_update(eventos)
            for evento in eventos:
                if self.eventos_en_comun(evento):
                    self.redraw = True
                    continue
                elif evento.type == pag.KEYDOWN and evento.key == pag.K_ESCAPE:
                    pag.quit()
                    sys.exit()
                elif evento.type == pag.MOUSEBUTTONDOWN and evento.button == 1:
                    for i,x in sorted(enumerate(self.list_to_click), reverse=True):
                        if x.click((mx, my)):
                            self.redraw = True
                            break
            if self.drawing:
                self.draw_objs(self.list_to_draw)  # La lista a dibujar de esta pantalla

if __name__ == '__main__':
    pag.init()
    Clicker_game()
