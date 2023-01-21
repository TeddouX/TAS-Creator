from pynput import mouse, keyboard
from utils import Timer
from threading import Thread
import json

t = Timer()
time_since_last_move = Timer()

key_press_start_time = 0
last_key_pressed = ""
has_finished_keyboard = None

mouse_press_start_time = 0

inputs = []

def on_key_press(key):
    global key_press_start_time
    global last_key_pressed
    global has_finished_keyboard

    if key == last_key_pressed and not has_finished_keyboard:
        return
    else:
        has_finished_keyboard = False

    last_key_pressed = key

    key_press_start_time = t.get_time()

def on_key_release(key: keyboard.KeyCode):
    global has_finished_keyboard

    has_finished_keyboard = True
    key_press_end_time = t.get_time()
    time_pressed = key_press_end_time - key_press_start_time

    try:
        name = key.char
    except:
        if key == keyboard.Key.shift_l:
            name = 'shift_l'
        elif key == keyboard.Key.ctrl_l:
            name = 'ctrl_l'
        elif key == keyboard.Key.space:
            name = 'space'
        elif key == keyboard.Key.esc:
            name = 'esc'
        elif key == keyboard.Key.alt_l:
            name = 'alt_l'
        elif key == keyboard.Key.enter:
            name = 'enter'
        else:
            name = ''

    inputs.append({'type': 'keyboard', "key": name, 'time': key_press_start_time, 'duration': time_pressed})
    print(f'key: {name}, time: {key_press_start_time}, duration: {time_pressed}')


def on_click(x, y, button, pressed):
    global mouse_press_start_time

    if pressed:
        mouse_press_start_time = t.get_time()
    elif not pressed:
        mouse_press_end_time = t.get_time()
        time_pressed = mouse_press_end_time - mouse_press_start_time

        inputs.append({'type': 'click', 'time': mouse_press_start_time, 'duration': time_pressed})
        print(f'time: {mouse_press_start_time}, duration: {time_pressed}')


def on_move(x, y):
    try:
        if time_since_last_move.get_time() > 0.25:
            inputs.append({'type': 'move', 'pos': (x, y), 'time': t.get_time()})
            print(f'pos: {(x, y)}, time: {t.get_time()}')
            time_since_last_move.end()
    except:
        time_since_last_move.start()




mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click
)

keyboard_listener = keyboard.Listener(
    on_press=on_key_press,
    on_release=on_key_release
)

def start_mouse_listener():
    mouse_listener.start()

def start_key_listener():
    keyboard_listener.start()




def save():
    try:
        with open('TAS.json', 'x') as f:
            formated_inputs = json.dumps({'inputs': sorted(inputs, key = lambda d: d['time'])})
            f.write(formated_inputs)
    except:
        with open('TAS.json', 'w') as f:
            formated_inputs = json.dumps({'inputs': sorted(inputs, key = lambda d: d['time'])})
            f.write(formated_inputs)
            
    mouse_listener.stop()
    keyboard_listener.stop()

mouse_listener_thread = Thread(target=start_mouse_listener)
key_listener_thread = Thread(target=start_key_listener)

if __name__ == '__main__':
    key_listener_thread.start()
    mouse_listener_thread.start()
    t.start()

    while not t.has_finished:
        txt = input('')
        if txt == 'end':
            t.end()
            save()
            quit(0)