import win32gui
import winreg
import win32con
import win32ui
import win32api
import time
import ctypes
from ctypes import windll
from typing import Callable, Optional, List, Tuple

def windowEnumerationHandler(hwnd, windows):
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def front(win_name,sw_code=1) -> None:
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

def ShowCursor(visible=True):
    win32api.ShowCursor(visible)
def GetDoubleClickTime():
    return win32gui.GetDoubleClickTime()

def front2(hwnd,sw_code=1):
    # win32con.SW_NORMAL -> 1
    # win32con.SW_MINIMIZE -> 6
    # win32con.SW_MAXIMIZE -> 3
    # win32con.SW_MAX -> 11
    # shell = win32com.client.Dispatch("WScript.Shell")
    # shell.SendKeys('%')
    try:
        win32gui.ShowWindow(hwnd,sw_code)# 5
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        
    except:
        pass

def take_window_snapshot(hwnd):
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

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    # result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    # print result

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return {'size':(w,h), 'buffer':bmpstr, 'bmpinfo':bmpinfo}

def set_window_colorkey_transparent(hwnd, colorkey = (0,0,0)):
    # Create layered window
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*colorkey), 0, win32con.LWA_COLORKEY)

def get_hwnd(win_name) -> int:
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == win_name:
            return i[0]
        
def get_actual_focus_win() -> int:
    return win32gui.GetForegroundWindow()

def check_win(name) -> bool:
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == name:
            return i[0]
    return False


def moveWin(hwnd,coordinates):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, *coordinates, 0, 0,win32con.SWP_NOSIZE)
def resizeWin(hwnd,size):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, *size,win32con.SWP_NOMOVE)

def topmost(win):
    win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def hide_window(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOSIZE|win32con.SWP_NOMOVE|win32con.SWP_HIDEWINDOW)
def show_window(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOSIZE|win32con.SWP_NOMOVE|win32con.SWP_SHOWWINDOW)

def get_screen_size():
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

def get_is_dark_mode_enabled():
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    value, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
    winreg.CloseKey(registry_key)
    return value == 0

def get_cursor_pos():
    return win32gui.GetCursorPos()

def Clip_Cursor(left,top,right,bottom):
    win32gui.ClipCursor((left,top,right,bottom))

def getFreeDiskSpace(unidad:str='C:/'):
    r = win32api.GetDiskFreeSpace(unidad)
    return r[0]*r[1]*r[2]

def getTotalDiskSpace(unidad:str='C:/'):
    r = win32api.GetDiskFreeSpace(unidad)
    return r[0]*r[1]*r[3]

def askFile(title='Select a file',filter="Text Files (*.txt)|*.txt|Ejecutables|*.exe|All Files (*.*)|*.*|"):
    dlg = win32ui.CreateFileDialog(1, None, None, None, filter)
    # dlg.SetOFNInitialDir('C:/')
    dlg.SetOFNTitle(title)
    dlg.DoModal()
    return dlg.GetPathName()

def askColor(init_color=(0,0,0)):
    v = win32ui.CreateColorDialog(win32api.RGB(*init_color))
    v.DoModal()
    return rgbint2rgbtuple(v.GetColor())

def rgbint2rgbtuple(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return (red, green, blue)

def MessageBox(title,text,style=[0]):
    """"
    
        0 : win32con.MB_OK,
        1 : win32con.MB_OKCANCEL,
        2 : win32con.MB_ABORTRETRYIGNORE,
        3 : win32con.MB_YESNOCANCEL,
        4 : win32con.MB_YESNO,
        5 : win32con.MB_RETRYCANCEL,
        16 : win32con.MB_ICONHAND,
        32 : win32con.MB_ICONQUESTION,
        48 : win32con.MB_ICONEXCLAMATION,
        64 : win32con.MB_ICONASTERISK,
        128 : win32con.MB_USERICON,

        12 : win32con.MB_ICONWARNING,
        13 : win32con.MB_ICONERROR,
        14 : win32con.MB_ICONINFORMATION,
        15 : win32con.MB_ICONSTOP,

        0 : win32con.MB_DEFBUTTON1,
        256 : win32con.MB_DEFBUTTON2,
        512 : win32con.MB_DEFBUTTON3,
        768 : win32con.MB_DEFBUTTON4

        262144 : win32con.MB_TOPMOST,
        524288 : win32con.MB_RIGHT
    """
    dict_styles = {
        0 : win32con.MB_OK,
        1 : win32con.MB_OKCANCEL,
        2 : win32con.MB_ABORTRETRYIGNORE,
        3 : win32con.MB_YESNOCANCEL,
        4 : win32con.MB_YESNO,
        5 : win32con.MB_RETRYCANCEL,
        16 : win32con.MB_ICONHAND,
        32 : win32con.MB_ICONQUESTION,
        48 : win32con.MB_ICONEXCLAMATION,
        64 : win32con.MB_ICONASTERISK,
        128 : win32con.MB_USERICON,

        12 : win32con.MB_ICONWARNING,
        13 : win32con.MB_ICONERROR,
        14 : win32con.MB_ICONINFORMATION,
        15 : win32con.MB_ICONSTOP,

        0 : win32con.MB_DEFBUTTON1,
        256 : win32con.MB_DEFBUTTON2,
        512 : win32con.MB_DEFBUTTON3,
        768 : win32con.MB_DEFBUTTON4,

        262144 : win32con.MB_TOPMOST,
        524288 : win32con.MB_RIGHT
    }
    s = style[0]
    for x in style[1:]:
        s = s | dict_styles[x]
    
    return win32ui.MessageBox(text, title, s)
    

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
