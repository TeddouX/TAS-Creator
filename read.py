from json import load, dumps
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from pynput import keyboard as keyboardModule
from utils import Timer, InexactFloat
from time import sleep


f = open('TAS.json')
data = load(f)

keyboard = KeyboardController()
mouse = MouseController()

t = Timer()

def start():
    t.start()
    
    for i in data['inputs']:
        has_finished = False
        while not has_finished:
            if i["type"] == 'keyboard' and InexactFloat(t.get_time()) == InexactFloat(i['time']):
                key = i['key']
                duration = i['duration']

                if len(key) > 1:
                    if key == 'shift_l':
                        key = keyboardModule.Key.shift_l
                    elif key == 'ctrl_l':
                        key = keyboardModule.Key.ctrl_l
                    elif key == 'space':
                        key = keyboardModule.Key.space
                    elif key == 'esc':
                        key = keyboardModule.Key.esc
                    elif key == 'alt_l':
                        key = keyboardModule.Key.alt_l
                    elif key == 'enter':
                        key = keyboardModule.Key.enter
                
                keyboard.press(key)
                sleep(duration)
                keyboard.release(key)

                print('Pressed key "', key, '"')

                has_finished = True
            elif i['type'] == 'click' and InexactFloat(t.get_time()) == InexactFloat(i['time']):
                duration = i['duration']

                mouse.press(Button.left)
                sleep(duration)
                mouse.release(Button.left)

                print('Pressed mouse button')

                has_finished = True
            elif i['type'] == 'move' and InexactFloat(t.get_time()) == InexactFloat(i['time']):
                mouse.position = tuple(i['pos'])

                has_finished = True
            else:
                pass


if __name__ == '__main__':
    start()
