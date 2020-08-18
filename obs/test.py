import win32gui
import win32con
import win32api
import pywinauto
from pywinauto import Desktop
import pyautogui
windows = Desktop(backend="uia").windows()
print([w.window_text() for w in windows])

name = "OBS 25.0.8 (64-bit, windows) - Profile: Безымянный - Scenes: Безымянный"
hwndMain = win32gui.FindWindow(None, name)
hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x44, 0)

from pywinauto.application import Application
app = Application()
app.connect(path="C:\Program Files\obs-studio\\bin\\64bit\\obs64.exe")
win = app.window_(title_re = "OBS.*")
win.type_keys("^d")
x = 2
