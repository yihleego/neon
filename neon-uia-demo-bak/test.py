import ctypes
import time
from ctypes.wintypes import tagPOINT

import pywinauto
import win32gui
from pywinauto import win32defines, win32structures, win32functions


def detect():
    m = win32gui.GetCursorPos()
    elem = pywinauto.uia_defines.IUIA().iuia.ElementFromPoint(tagPOINT(m[0], m[1]))
    element = pywinauto.uia_element_info.UIAElementInfo(elem)
    target = element
    name = target.name
    automation_id = target.automation_id
    class_name = target.class_name
    control_id = target.control_id
    control_type = target.control_type
    rectangle = target.rectangle

    while not target.handle or not target.process_id:
        target = target.parent
    handle = target.handle
    process_id = target.process_id
    process_name = ""
    # if process_id:
    #     process_name = get_process_name_by_pid(process_id)

    # msg = f"handle: {handle}, process_id: {process_id}, process_name: {process_name}, automation_id: {automation_id}, class_name: {class_name}, control_id: {control_id}, control_type: {control_type}, rectangle: {rectangle}"
    # print(msg)

    return {
        "name": name,
        "automation_id": automation_id,
        "class_name": class_name,
        "control_id": control_id,
        "control_type": control_type,
        "rectangle": rectangle,
        "handle": handle,
        "process_id": process_id,
        "process_name": process_name,
    }


# handle = 0xF0676
# app = Application(backend='uia')
# app.connect(handle=handle)
# wechat = app.window(class_name='Notepad')
# wechat.set_focus()

color = 0x0000ff

# create the pen(outline)
pen_handle = win32functions.CreatePen(win32defines.PS_SOLID, 3, color)

# create the brush (inside)
brush = win32structures.LOGBRUSH()
brush.lbStyle = win32defines.BS_NULL
brush.lbHatch = win32defines.HS_DIAGCROSS
brush_handle = win32functions.CreateBrushIndirect(ctypes.byref(brush))

font = win32structures.LOGFONTW()
font.lfHeight = 20
font.lfWeight = win32defines.FW_BOLD
font_handle = win32functions.CreateFontIndirect(ctypes.byref(font))

# get the Device Context
dc = win32functions.CreateDC("DISPLAY", None, None, None)

# push our objects into it
win32functions.SelectObject(dc, brush_handle)
win32functions.SelectObject(dc, pen_handle)
win32functions.SelectObject(dc, font_handle)
win32gui.SetTextColor(dc, color)
win32gui.SetBkMode(dc, win32defines.TRANSPARENT)
hwnd = win32gui.WindowFromPoint((0, 0))

past_handle = None
past_rect = None
while True:
    dddd = detect()

    # draw the rectangle to the DC
    # rect = wechat.rectangle()
    rect = dddd["rectangle"]

    if past_handle and past_rect and past_rect != rect:
        win32gui.InvalidateRect(hwnd, past_rect, True)
        win32gui.UpdateWindow(hwnd)

    win32functions.Rectangle(dc, rect.left, rect.top, rect.right, rect.bottom)

    # rect.top -= font.lfHeight
    # win32functions.DrawText(dc, "helloworld", -1,rect, win32con.DT_LEFT | win32con.DT_TOP)
    win32functions.TextOut(dc, rect.left, rect.top - font.lfHeight, "helloworld", len("helloworld"))

    past_handle = dddd["handle"]
    past_rect = (rect.left - 100, rect.top - font.lfHeight - 100, rect.right + 100, rect.bottom + 100)
    time.sleep(0.1)

# Delete the brush and pen we created
win32functions.DeleteObject(brush_handle)
win32functions.DeleteObject(pen_handle)

# delete the Display context that we created
win32functions.DeleteDC(dc)
