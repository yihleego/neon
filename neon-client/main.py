import platform
from ctypes.wintypes import tagPOINT

from pynput import keyboard

import api
import app
import listener
import recorder


def on_event(r):
    _system = platform.system().lower()
    is_linux = _system.find("linux") >= 0
    is_windows = _system.find("windows") >= 0
    is_mac = _system.find("darwin") >= 0 or _system.find("mac") >= 0
    if not is_windows:
        return

    def get_process_name_by_pid(pid):
        import psutil
        try:
            process = psutil.Process(pid)
            return process.name()
        except psutil.NoSuchProcess as e:
            return f"Process with PID {pid} not found"
        except psutil.AccessDenied as e:
            return f"Access denied to process with PID {pid}"

    def on_click(_, x, y):
        import pywinauto
        elem = pywinauto.uia_defines.IUIA().iuia.ElementFromPoint(tagPOINT(x, y))
        element = pywinauto.uia_element_info.UIAElementInfo(elem)
        target = element
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
        if process_id:
            process_name = get_process_name_by_pid(process_id)

        msg = f"handle: {handle}, process_id: {process_id}, process_name: {process_name}, automation_id: {automation_id}, class_name: {class_name}, control_id: {control_id}, control_type: {control_type}, rectangle: {rectangle}"
        print(msg)

        skips = ["chrome", "msedge"]
        for s in skips:
            if process_name.find(s) >= 0:
                return

        r.draw((int(rectangle.left), int(rectangle.top), int(rectangle.right - rectangle.left), int(rectangle.bottom - rectangle.top)), msg)

    # listener.listen(listener.EventType.CLICK, [mouse.Button.left, keyboard.Key.ctrl_l], on_click)
    listener.listen(listener.EventType.MOUSEMOVE, [keyboard.Key.ctrl_l], on_click)


if __name__ == '__main__':
    api.run()
    r = recorder.Recorder()
    r.show()
    on_event(r)
    listener.run()
    app.run()
