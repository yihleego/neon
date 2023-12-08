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
