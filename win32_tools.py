import win32gui, win32con, win32com.client
def windowEnumerationHandler(hwnd, windows):
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def front(win_name) -> None:

    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == win_name:
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.ShowWindow(i[0],win32con.SW_SHOWNORMAL)# 5
            win32gui.SetForegroundWindow(i[0])
            return True
    return False

def check_win(name) -> bool:
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == name:
            return True
    return False