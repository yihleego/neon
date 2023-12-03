import threading

from pynput import mouse, keyboard


class EventType:
    CLICK = "click"
    DBCLICK = "dbclick"
    MOUSEDOWN = "mousedown"
    MOUSEUP = "mouseup"
    MOUSEMOVE = "mousemove"
    KEYDOWN = "keydown"
    KEYUP = "keyup"


_keyboard_states: dict[keyboard.Key, bool] = {}  # key -> pressed
_mouse_states: dict[mouse.Button, tuple[int, int]] = {}  # key -> position
_mouse_position: tuple[int, int] = (0, 0)
_listeners: dict[EventType, list] = {
    EventType.CLICK: [],
    EventType.DBCLICK: [],
    EventType.KEYDOWN: [],
    EventType.KEYUP: [],
    EventType.MOUSEDOWN: [],
    EventType.MOUSEUP: [],
    EventType.MOUSEMOVE: [],
}


def _on_press(key):
    _keyboard_states[key] = True
    _trigger(EventType.KEYDOWN, key, _mouse_position[0], _mouse_position[1])


def _on_release(key):
    _trigger(EventType.KEYUP, key, _mouse_position[0], _mouse_position[1])
    _keyboard_states[key] = False


def _on_click(x, y, button, pressed):
    if pressed:
        _mouse_states[button] = (x, y)
        _trigger(EventType.MOUSEDOWN, button, x, y)
    else:
        _trigger(EventType.MOUSEUP, button, x, y)
        _trigger(EventType.CLICK, button, x, y)
        _mouse_states[button] = None

        #print(_keyboard_states)
        #print(_mouse_states)


def _on_move(x, y):
    _position = (x, y)
    _trigger(EventType.MOUSEMOVE, None,x, y)


def _trigger(event, *args):
    listeners = _listeners[event]
    for keys, func in listeners:
        #print('keys', keys)
        ok = True
        for key in keys:
            if isinstance(key, keyboard.Key):
                if not _keyboard_states.get(key):
                    ok = False
                    break
            elif isinstance(key, mouse.Button):
                if not _mouse_states.get(key):
                    ok = False
                    break
            else:
                ok = False
                break
        if ok:
            func(*args)


def _run():
    with keyboard.Listener(on_press=_on_press, on_release=_on_release) as k_listener, \
            mouse.Listener(on_click=_on_click, on_move=_on_move) as m_listener:
        k_listener.join()
        m_listener.join()


def listen(event, keys, func):
    _listeners[event].append((keys, func))


def run():
    threading.Thread(target=_run, daemon=True).start()
