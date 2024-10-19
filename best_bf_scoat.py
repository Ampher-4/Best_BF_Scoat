import ctypes
import time
from ctypes import wintypes
import threading

user32 = ctypes.windll.user32

# Define constants
WH_MOUSE_LL = 14
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

# Define the mouse callback function
def low_level_mouse_proc(nCode, wParam, lParam):
    if wParam == WM_RBUTTONDOWN:
        threading.Thread(target=press_q_continuously).start()
    return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)

# Set the mouse hook
CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
pointer = CMPFUNC(low_level_mouse_proc)
hook = ctypes.windll.user32.SetWindowsHookExA(WH_MOUSE_LL, pointer, ctypes.windll.kernel32.GetModuleHandleW(None), 0)

# Function to press 'Q' continuously
def press_q_continuously():
    while True:
        if user32.GetAsyncKeyState(0x02):  # Check if the right mouse button is still pressed
            user32.keybd_event(0x51, 0, 0, 0)  # Press 'Q'
            user32.keybd_event(0x51, 0, 2, 0)  # Release 'Q'
            time.sleep(0.1)
        else:
            break

# Keep the script running
while True:
    msg = wintypes.MSG()
    ctypes.windll.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)
    ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
    ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
