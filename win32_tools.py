import win32gui
import winreg
import win32con
import win32ui
import win32api

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

def front2(hwnd,sw_code=1):
    # win32con.SW_SHOW
    # win32con.SW_SHOWMINIMIZED
    # win32con.SW_SHOWNORMAL
    # win32con.SW_MINIMIZE
    # win32con.SW_MAXIMIZE
    # win32con.SW_SHOWMAXIMIZED
    # win32con.SW_MAX
    # shell = win32com.client.Dispatch("WScript.Shell")
    # shell.SendKeys('%')
    try:
        win32gui.ShowWindow(hwnd,sw_code)# 5
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        
    except:
        pass

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

def check_process(name) -> bool:
    import psutil
    for proc in psutil.process_iter(['name']):
        print(proc.info['name'])
        if proc.info['name'] == name:
            return True
    return False

def moveWin(win,coordinates):
    hwnd = win
    win32gui.MoveWindow(hwnd, -coordinates[0], -coordinates[1], 0,0, False)
def resizeWin(win,coordinates,size):
    hwnd = win
    win32gui.MoveWindow(hwnd, -coordinates[0], -coordinates[1], size[0],size[1], False)

def topmost(win):
    win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def get_is_dark_mode_enabled():
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    value, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
    winreg.CloseKey(registry_key)
    return value == 0

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