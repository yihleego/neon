import win32gui
from pywinauto import Application, win32defines

handle = 0x606CE
app = Application(backend='uia')
app.connect(handle=handle)
wechat = app.window(class_name='Notepad')
wechat.set_focus()

dc = win32gui.GetDC(0)

pen = win32gui.CreatePen(win32defines.PS_SOLID, 2, 0x00ff00)
brush = win32gui.CreateSolidBrush(0x00ff00)
font = win32gui.LOGFONT()

# brush = win32structures.LOGBRUSH()
# brush.lbStyle = win32defines.BS_NULL
# brush.lbHatch = win32defines.HS_DIAGCROSS
# brush_handle = win32functions.CreateBrushIndirect(ctypes.byref(brush))
win32gui.SetBkMode(dc, win32defines.TRANSPARENT)
win32gui.SelectObject(dc, pen)
win32gui.SelectObject(dc, brush)
# win32gui.SelectObject(dc,font)
while True:
    rect = wechat.rectangle()
    rect2 = (rect.left, rect.top, rect.right, rect.bottom)
    win32gui.FrameRect(dc, rect2, brush)


import win32gui, win32ui, win32api, win32con
from win32api import GetSystemMetrics

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0,0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

red = win32api.RGB(255, 0, 0) # Red

past_coordinates = monitor
while True:
    m = win32gui.GetCursorPos()

    rect = win32gui.CreateRoundRectRgn(*past_coordinates, 2 , 2)
    win32gui.RedrawWindow(hwnd, past_coordinates, rect, win32con.RDW_INVALIDATE)

    for x in range(10):
        win32gui.SetPixel(dc, m[0]+x, m[1], red)
        win32gui.SetPixel(dc, m[0]+x, m[1]+10, red)
        for y in range(10):
            win32gui.SetPixel(dc, m[0], m[1]+y, red)
            win32gui.SetPixel(dc, m[0]+10, m[1]+y, red)

    past_coordinates = (m[0]-20, m[1]-20, m[0]+20, m[1]+20)