from ctypes.wintypes import tagPOINT

from pynput import mouse, keyboard

ctrl_pressed = False


def on_press(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True


def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False


def on_click(x, y, button, pressed):
    global ctrl_pressed
    if button == mouse.Button.left:
        if pressed and ctrl_pressed:
            import pywinauto
            elem = pywinauto.uia_defines.IUIA().iuia.ElementFromPoint(tagPOINT(x, y))
            element = pywinauto.uia_element_info.UIAElementInfo(elem)
            target = element
            while not target.handle:
                target = target.parent
            handle = target.handle
            process_id = target.process_id
            automation_id = target.automation_id
            class_name = target.class_name
            control_id = target.control_id
            control_type = target.control_type
            rectangle = target.rectangle

            print('handle:', handle,
                  'process_id:', process_id,
                  'automation_id:', automation_id,
                  'class_name:', class_name,
                  'control_id:', control_id,
                  'control_type:', control_type,
                  'rectangle:', rectangle)


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
        mouse.Listener(on_click=on_click) as m_listener:
    k_listener.join()
    m_listener.join()
