import win32gui
import winreg
import win32con
import win32com.client
import win32ui
import win32api
import time
from ctypes import windll
from typing import Callable, Optional, List, Tuple

def windowEnumerationHandler(hwnd, windows):
    """
    Enumera todas las ventanas visibles y las agrega a la lista.
    """
    if not win32gui.IsWindowVisible(hwnd):
        return
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def front(win_name,sw_code=1) -> None:
    """
    Trae la ventana con el nombre especificado al frente.
    
    Parametros:
    win_name (str): El nombre de la ventana.
    sw_code (int): El código de la ventana.
     - win32con.SW_NORMAL -> 1
     - win32con.SW_MINIMIZE -> 6
     - win32con.SW_MAXIMIZE -> 3
     - win32con.SW_MAX -> 11
    """
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == win_name:
            try:
                win32gui.ShowWindow(i[0],sw_code)# 5
                win32gui.BringWindowToTop(i[0])
                win32gui.SetForegroundWindow(i[0])
            except:
                pass
            return True
    return False

def front2(hwnd,sw_code=1):
    """
    Trae la ventana con el handle especificado al frente.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    sw_code (int): El código de la ventana.
     - win32con.SW_NORMAL -> 1
     - win32con.SW_MINIMIZE -> 6
     - win32con.SW_MAXIMIZE -> 3
     - win32con.SW_MAX -> 11
    """
    try:
        win32gui.ShowWindow(hwnd,sw_code)
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        
    except:
        pass

def ShowCursor(visible=True):
    """
    Muestra o oculta el cursor.
    
    Parametros:
    visible (bool): Si es True, el cursor se muestra. Si es False, el cursor se oculta.
    """
    win32api.ShowCursor(visible)

def GetDoubleClickTime():
    """
    Retorna el tiempo de doble clic por defecto.
    """
    return win32gui.GetDoubleClickTime()


def take_window_snapshot(hwnd):
    """
    Toma una captura de la ventana con el handle especificado.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    """
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    front2(hwnd)

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return {'size':(w,h), 'buffer':bmpstr, 'bmpinfo':bmpinfo}

def set_window_colorkey_transparent(hwnd, colorkey = (0,0,0)):
    """
    Establece el color transparente de la ventana con el handle especificado.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    colorkey (tuple): El color transparente de la ventana.
    """
    # Create layered window
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*colorkey), 0, win32con.LWA_COLORKEY)

def get_hwnd(win_name) -> int:
    """
    Retorna el handle de la ventana con el nombre especificado.
    
    Parametros:
    win_name (str): El nombre de la ventana.
    """
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == win_name:
            return i[0]
        
def get_actual_focus_win() -> int:
    """
    Retorna el handle de la ventana que tiene el focus actual.
    """
    return win32gui.GetForegroundWindow()

def check_win(name) -> bool:
    """
    Verifica si la ventana con el nombre especificado existe.
    
    Parametros:
    name (str): El nombre de la ventana.
    """
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == name:
            return i[0]
    return False


def setWinPos(hwnd,coordinates):
    """
    Mueve la ventana con el handle especificado a las coordenadas especificadas.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    coordinates (tuple): Las coordenadas (x, y) de la ventana.
    """
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, *coordinates, 0, 0,win32con.SWP_NOSIZE|win32con.SWP_NOZORDER|win32con.SWP_NOACTIVATE)

def moveWin(hwnd,coordinates):
    """
    Mueve la ventana con el handle especificado a las coordenadas especificadas.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    coordinates (tuple): Las coordenadas (x, y) de la ventana.
    """
    win32gui.MoveWindow(hwnd, *coordinates, 0, 0, False)

def resizeWin(hwnd,size):
    """
    Cambia el tamaño de la ventana con el handle especificado.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    size (tuple): El tamaño (ancho, alto) de la ventana.
    """
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, *size,win32con.SWP_NOMOVE)

def topmost(win):
    """
    Establece que la ventana con el handle especificado se muestre siempre en frente.
    
    Parametros:
    win (int): El handle de la ventana.
    """
    win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def hide_window(hwnd):
    """
    Oculta la ventana con el handle especificado.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    """
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOSIZE|win32con.SWP_NOMOVE|win32con.SWP_HIDEWINDOW)
def show_window(hwnd):
    """
    Muestra la ventana con el handle especificado.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    """
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOSIZE|win32con.SWP_NOMOVE|win32con.SWP_SHOWWINDOW)

def get_screen_size():
    """
    Retorna el tamaño de la pantalla.
    """
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

def get_window_rect(hwnd):
    """
    Retorna la posición de la ventana con el handle especificado.
    
    Parametros:
    hwnd (int): El handle de la ventana.
    """
    return win32gui.GetWindowRect(hwnd)

def get_is_dark_mode_enabled():
    """
    Retorna True si el modo oscuro está habilitado, False en caso contrario.
    """
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    value, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
    winreg.CloseKey(registry_key)
    return value == 0

def get_cursor_pos():
    """
    Retorna la posición actual del cursor.
    """
    return win32gui.GetCursorPos()

def Clip_Cursor(left,top,right,bottom):
    """
    Define el área de la que el cursor no puede salir.
    
    Parametros:
    left (int): La coordenada x izquierda.
    top (int): La coordenada y superior.
    right (int): La coordenada x derecha.
    bottom (int): La coordenada y inferior.
    """
    win32gui.ClipCursor((left,top,right,bottom))

def getFreeDiskSpace(unidad:str='C:/'):
    """
    Retorna el espacio libre en el disco especificado.
    
    Parametros:
    unidad (str): La unidad del disco.
    """
    r = win32api.GetDiskFreeSpace(unidad)
    return r[0]*r[1]*r[2]

def getTotalDiskSpace(unidad:str='C:/'):
    """
    Retorna el espacio total en el disco especificado.
    
    Parametros:
    unidad (str): La unidad del disco.
    """
    r = win32api.GetDiskFreeSpace(unidad)
    return r[0]*r[1]*r[3]

def askFile(title='Select a file',filter="Text Files (*.txt)|*.txt|Ejecutables|*.exe|All Files (*.*)|*.*|"):
    """
    Abre un cuadro de diálogo para seleccionar un archivo.
    
    Parametros:
    title (str): El título del cuadro de diálogo.
    filter (str): El filtro de archivos.
    
    Retorna:
    str: La ruta del archivo seleccionado.
    """
    dlg = win32ui.CreateFileDialog(1, None, None, None, filter)
    # dlg.SetOFNInitialDir('C:/')
    dlg.SetOFNTitle(title)
    dlg.DoModal()
    return dlg.GetPathName()

def askColor(init_color=(0,0,0)):
    """
    Abre un cuadro de diálogo para seleccionar un color.
    
    Parametros:
    init_color (tuple): El color inicial seleccionado.
    
    Retorna:
    tuple: El color seleccionado.
    """
    v = win32ui.CreateColorDialog(win32api.RGB(*init_color))
    v.DoModal()
    return rgbint2rgbtuple(v.GetColor())

def rgbint2rgbtuple(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return (red, green, blue)

def MessageBox(title, text, button_type=0, icon=None, default_button=0, position=None):
    """
    Muestra un cuadro de diálogo con un mensaje.
    
    Args:
        title (str): Título del cuadro de diálogo.
        text (str): Texto a mostrar en el cuadro de diálogo.
        button_type (int, optional): Tipo de botones a mostrar. Valores posibles:
            0: OK
            1: OK, CANCEL
            2: ABORT, RETRY, IGNORE
            3: YES, NO, CANCEL
            4: YES, NO
            5: RETRY, CANCEL
        icon (int, optional): Ícono a mostrar. Valores posibles:
            12: Advertencia (WARNING)
            13: Error (ERROR)
            14: Información (INFORMATION)
            15: Detener (STOP)
            16: Mano (HAND)
            32: Pregunta (QUESTION)
            48: Exclamación (EXCLAMATION)
            64: Asterisco (ASTERISK)
        default_button (int, optional): Botón predeterminado. Valores posibles:
            0: Primer botón
            1: Segundo botón
            2: Tercer botón
            3: Cuarto botón
        position (str, optional): Posición del cuadro de diálogo. Valores posibles:
            'topmost': Siempre visible
            'right': Alineado a la derecha
    
    Returns:
        int: El ID del botón pulsado.
            Para OK: 1
            Para CANCEL: 2
            Para ABORT: 3
            Para RETRY: 4
            Para IGNORE: 5
            Para YES: 6
            Para NO: 7
    
    Ejemplos:
        >>> MessageBox('Título', 'Mensaje')
        >>> MessageBox('Pregunta', '¿Continuar?', button_type=4, icon=32)
        >>> MessageBox('Error', 'Operación fallida', button_type=0, icon=13, position='topmost')
    """
    # Mapear tipos de botones
    button_types = {
        0: win32con.MB_OK,
        1: win32con.MB_OKCANCEL,
        2: win32con.MB_ABORTRETRYIGNORE,
        3: win32con.MB_YESNOCANCEL,
        4: win32con.MB_YESNO,
        5: win32con.MB_RETRYCANCEL
    }
    
    # Mapear iconos
    icons = {
        12: win32con.MB_ICONWARNING,
        13: win32con.MB_ICONERROR,
        14: win32con.MB_ICONINFORMATION,
        15: win32con.MB_ICONSTOP,
        16: win32con.MB_ICONHAND,
        32: win32con.MB_ICONQUESTION,
        48: win32con.MB_ICONEXCLAMATION,
        64: win32con.MB_ICONASTERISK
    }
    
    # Mapear botones predeterminados
    default_buttons = {
        0: win32con.MB_DEFBUTTON1,
        1: win32con.MB_DEFBUTTON2,
        2: win32con.MB_DEFBUTTON3,
        3: win32con.MB_DEFBUTTON4
    }
    
    # Mapear posiciones
    positions = {
        'topmost': win32con.MB_TOPMOST,
        'right': win32con.MB_RIGHT
    }
    
    # Inicializar el estilo con el tipo de botón
    if button_type not in button_types:
        button_type = 0
    style = button_types[button_type]
    
    # Añadir icono si se especifica
    if icon is not None and icon in icons:
        style |= icons[icon]
    
    # Añadir botón predeterminado si se especifica
    if default_button in default_buttons:
        style |= default_buttons[default_button]
    
    # Añadir posición si se especifica
    if position is not None and position in positions:
        style |= positions[position]
    
    try:
        return win32ui.MessageBox(text, title, style)
    except Exception as e:
        print(f"Error mostrando mensaje: {e}")
        return 0

class Win32TrayIcon:
    """
    Ícono en bandeja del sistema para Windows con soporte completo de eventos.
    
    Args:
        icon_path: Ruta al archivo .ico
        tooltip: Texto al hacer hover
        menu_items: Lista de (texto, callback) para menú contextual
        on_left_click: Función a ejecutar en clic izquierdo
        on_right_click: Función a ejecutar en clic derecho (anula menú)
    """
    
    def __init__(self, 
                 icon_path: str, 
                 tooltip: str = "", 
                 menu_items: Optional[List[Tuple[str, Callable]]] = None,
                 on_left_click: Optional[Callable] = None,
                 on_right_click: Optional[Callable] = None):
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.menu_items = menu_items or []
        self.on_left_click = on_left_click
        self.on_right_click = on_right_click
        self.hwnd = None
        self.running = True
        self.menu_commands = {}

    def run(self):
        self._create_window()
        self.__mainloop()

    def __mainloop(self):
        while self.running:
            win32gui.PumpWaitingMessages()
            time.sleep(0.1)
        self.__destroy()

    def _create_window(self):
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "PythonSysTrayIcon"
        wc.lpfnWndProc = self._message_handler
        self.class_atom = win32gui.RegisterClass(wc)
        
        self.hwnd = win32gui.CreateWindow(
            self.class_atom, 
            "SysTray", 
            win32con.WS_OVERLAPPED, 
            0, 0, 0, 0, 0, 0, 
            wc.hInstance, 
            None
        )
        
        self._update_icon()
        self._create_menu()

    def _message_handler(self, hwnd: int, msg: int, wparam: int, lparam: int) -> int:
        # Manejo de eventos del icono
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        if msg == win32con.WM_USER + 20:  # Mensaje de la bandeja del sistema
            if lparam == win32con.WM_LBUTTONDOWN:
                if self.on_left_click:
                    self.on_left_click()
                return 0
                
            elif lparam == win32con.WM_RBUTTONDOWN:
                if self.on_right_click:
                    self.on_right_click()
                else:
                    self._show_context_menu()
                return 0
        
        # Manejo de comandos del menú
        elif msg == win32con.WM_COMMAND:
            item_id = wparam & 0xFFFF
            if item_id in self.menu_commands:
                self.menu_commands[item_id]()
                return 0
        
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def _update_icon(self):
        # Carga y actualiza el ícono
        hicon = win32gui.LoadImage(
            0, self.icon_path, 
            win32con.IMAGE_ICON, 
            0, 0, 
            win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        )
        
        nid = (
            self.hwnd, 
            0, 
            win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
            win32con.WM_USER + 20, 
            hicon, 
            self.tooltip
        )
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    def _create_menu(self):
        # Construye menú contextual con items
        self.menu = win32gui.CreatePopupMenu()
        self.menu_commands.clear()
        
        for idx, (text, callback) in enumerate(self.menu_items):
            self.menu_commands[idx] = callback
            win32gui.AppendMenu(
                self.menu, 
                win32con.MF_STRING, 
                idx, 
                text
            )

    def _show_context_menu(self):
        # Muestra el menú en posición correcta
        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(
            self.menu,
            win32con.TPM_LEFTALIGN,
            pos[0],
            pos[1],
            0,
            self.hwnd,
            None
        )
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def update_menu(self, new_items: List[Tuple[str, Callable]]):
        """Actualiza dinámicamente el menú contextual"""
        self.menu_items = new_items
        self._create_menu()

    def show_notification(self, title: str, message: str, timeout: int = 5):
        """Muestra notificación estilo Windows con ícono"""
        hicon = win32gui.LoadImage(
            0, self.icon_path, 
            win32con.IMAGE_ICON, 
            0, 0, 
            win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        )
        nid = (
            self.hwnd, 
            0,
            win32gui.NIF_INFO,
            win32con.WM_USER + 20,
            0,
            self.tooltip,
            message,
            timeout,
            title,
            win32gui.NIIF_ICON_MASK
        )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def stop(self):
        self.running = False

    def __destroy(self):
        """Limpiar recursos"""
        win32gui.DestroyWindow(self.hwnd)
        win32gui.UnregisterClass(self.class_atom, None)
        win32gui.PostQuitMessage(0)


class Speaker:
    def __init__(self, ):
        self.speek = win32com.client.Dispatch('SAPI.SpVoice')
        self.__voice_index = 0
    
    def speak(self, text):
        self.speek.Speak(text)

    @property
    def voices(self):
        return [self.speek.GetVoices().Item(i).GetDescription() for i in range(self.speek.GetVoices().Count)]
    
    
    @property
    def voice(self):
        return self.speek.Voice.GetDescription()
    
    @property
    def voice_index(self):
        return self.__voice_index
    @voice_index.setter
    def voice_index(self, index: int):
        if index < 0 or index >= self.speek.GetVoices().Count:
            raise ValueError(f"Invalid voice index: {index}")
        self.__voice_index = index
        self.speek.Voice = self.speek.GetVoices().Item(index)
    
    def set_voice(self, voice_name: str):
        for i, voice in enumerate(self.voices):
            if voice == voice_name:
                self.speek.Voice = self.speek.GetVoices().Item(i)
                self.__voice_index = i
                return
        raise ValueError(f"Voice '{voice_name}' not found")

