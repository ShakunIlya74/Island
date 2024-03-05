import time
from ppadb.client import Client as AdbClient


client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
devices = client.devices()

if len(devices) == 0:
    print('No devices')
    quit()

device = devices[0]

print(f'Connected to {device}')

# time.sleep(1)

#Commands to control phone
#device.shell('input touchscreen tap x y')

#device.shell('input touchscreen swipe x1 y1 x2 y2')

#device.shell('Input keyevent eventID')

#device.shell('Input text "Enter your text here"')


def tap(x, y):
    print(tap, x, y)
    device.shell(f'input touchscreen tap {x} {y}')


def swipe(x1, y1, x2, y2):
    device.shell(f'input touchscreen swipe {x1} {y1} {x2} {y2}')


def keyevent(event_id):
    device.shell(f'input keyevent {event_id}')


def make_a_screenshot(file_name='temp_screen.png'):
    device.shell(f'screencap /sdcard/screen.png')
    device.pull(f'/sdcard/screen.png', f'../data/screenshots/{file_name}')




if __name__ == '__main__':
    make_a_screenshot()
    print('Screenshot saved as temp_screen.png')


def big_swipe_down(pixels_down=150):
    swipe(1040, 2030, 1040, 2030-pixels_down)


def small_swipe_down(pixels_down=50):
    swipe(740, 530, 740, 530-pixels_down)
