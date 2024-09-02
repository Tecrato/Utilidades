import win32gui, winreg

import win32con

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

def is_dark_mode_enabled():
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
    value, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
    winreg.CloseKey(registry_key)
    return value == 0