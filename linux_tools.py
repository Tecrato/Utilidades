import os
import subprocess
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import tempfile
import platform

# Function to check and install required packages
def _install_linux_packages():
    if platform.system() == 'Linux':
        try:
            # Check if scrot is installed
            subprocess.run(['scrot', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            try:
                # Install scrot
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'scrot'], check=True)
            except:
                try:
                    # Check if ImageMagick is installed
                    subprocess.run(['import', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    # Install ImageMagick
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'imagemagick'], check=True)

# Install required packages on import
_install_linux_packages()
import psutil

# Window management functions
def front(window_name):
    try:
        subprocess.run(['wmctrl', '-a', window_name])
        return True
    except:
        return False

# Cursor and display functions
def ShowCursor(visible=True):
    pass  # Not directly supported in Linux

def GetDoubleClickTime():
    return 500  # Default value for Linux

# System information functions
def get_screen_size():
    root = tk.Tk()
    root.withdraw()
    return (root.winfo_screenwidth(), root.winfo_screenheight())

def get_cursor_pos():
    root = tk.Tk()
    root.withdraw()
    return (root.winfo_pointerx(), root.winfo_pointery())

# Disk space functions
def getFreeDiskSpace(path='/'):
    stat = os.statvfs(path)
    return stat.f_bavail * stat.f_frsize

def getTotalDiskSpace(path='/'):
    stat = os.statvfs(path)
    return stat.f_blocks * stat.f_frsize

# Dialog functions
def askFile(title='Select a file', filter=None):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=title)

def askColor(init_color=(0,0,0)):
    root = tk.Tk()
    root.withdraw()
    return colorchooser.askcolor(initialcolor=init_color)[0]

# Message box function
def MessageBox(title, text, style=None):
    root = tk.Tk()
    root.withdraw()
    return messagebox.showinfo(title, text)

# Window management functions
def front2(hwnd, sw_code=1):
    try:
        subprocess.run(['wmctrl', '-ia', str(hwnd)])
        return True
    except:
        return False

def moveWin(hwnd, coordinates):
    x, y = coordinates
    subprocess.run(['wmctrl', '-ir', str(hwnd), '-e', f'0,{x},{y},-1,-1'])

def resizeWin(hwnd, size):
    width, height = size
    subprocess.run(['wmctrl', '-ir', str(hwnd), '-e', f'0,-1,-1,{width},{height}'])

def topmost(win):
    subprocess.run(['wmctrl', '-ir', str(win), '-b', 'add,above'])

def hide_window(hwnd):
    subprocess.run(['wmctrl', '-ir', str(hwnd), '-b', 'add,hidden'])

def show_window(hwnd):
    subprocess.run(['wmctrl', '-ir', str(hwnd), '-b', 'remove,hidden'])

# Screenshot functionality
def take_window_snapshot(hwnd):
    try:
        # Use scrot or ImageMagick's import command for screenshots
        with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
            # Try scrot first, fall back to import
            try:
                subprocess.run(['scrot', tmp.name], check=True)
            except:
                subprocess.run(['import', '-window', 'root', tmp.name], check=True)
            
            # Read the captured image
            with open(tmp.name, 'rb') as f:
                img_data = f.read()
            
            # Get image dimensions using file command
            output = subprocess.check_output(['file', tmp.name])
            width, height = [int(dim) for dim in output.decode().split(',')[1].split('x')]
            
            return {'size': (width, height), 'buffer': img_data, 'bmpinfo': {}}
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None

# System theme detection
def get_is_dark_mode_enabled():
    try:
        output = subprocess.check_output(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'])
        return b'dark' in output.lower()
    except:
        return False

# Cursor management
def Clip_Cursor(left, top, right, bottom):
    pass  # Not directly supported in Linux

# Tray icon implementation
class Win32TrayIcon:
    def __init__(self, icon_path, tooltip="", menu_items=None, on_left_click=None, on_right_click=None):
        if platform.system() == 'Linux':
            # Import pystray only on Linux
            import pystray
            from PIL import Image
            self.pystray = pystray
            self.Image = Image
            
            # Create menu items
            menu = []
            for item in menu_items or []:
                menu.append(self.pystray.MenuItem(item[0], item[1]))
            
            # Load icon
            icon = self.Image.open(icon_path)
            
            # Create tray icon
            self.tray = self.pystray.Icon(
                'tray_icon',
                icon,
                tooltip,
                self.pystray.Menu(*menu)
            )
        else:
            # Use native implementation on Windows
            self.tray = None

    def run(self):
        if platform.system() == 'Linux':
            self.tray.run()

    def stop(self):
        if platform.system() == 'Linux':
            self.tray.stop()

    def show_notification(self, title, message, timeout=5):
        if platform.system() == 'Linux':
            subprocess.run(['notify-send', title, message, f'--expire-time={timeout * 1000}'])
