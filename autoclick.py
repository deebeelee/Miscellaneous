import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

delay = 0.1
button = Button.left
start_stop_key = KeyCode(char='`')
exit_key = KeyCode(char='~')
decr_key = KeyCode(char='-')
incr_key = KeyCode(char='=')

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super().__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True
        print("running")

    def stop_clicking(self):
        self.running = False
        print("stopped")

    def exit(self):
        self.stop_clicking()
        self.program_running = False
        print("exiting...")
        
    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()

def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()
    elif key == incr_key:
        click_thread.delay*=0.9
        print("speed -> "+str(round(click_thread.delay,ndigits=3))+" sec")
    elif key == decr_key:
        click_thread.delay/=0.9
        print("speed -> "+str(round(click_thread.delay,ndigits=3))+" sec")

with Listener(on_press=on_press) as listener:
    print('---autoclicker running now!---')
    listener.join()