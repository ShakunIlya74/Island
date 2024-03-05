import time

from adb_manipulator_utils import tap, make_a_screenshot
from scraping.adb_manipulator_utils import big_swipe_down, small_swipe_down
from scraping.analyze_picture_utils import get_pixel_color


def download_program(program_name, from_start=True):
    print(f"Downloading program: {program_name}")
    if from_start:
        tap(820, 330)
        time.sleep(1)
    tap(970, 610) # tap on download button
    time.sleep(1.5)
    tap(970, 610) # ensure (open day
    time.sleep(1)
    tap(94, 180)  # close day
    print("First past")
    time.sleep(1)
    while True:
        big_swipe_down()
        big_swipe_down()
        screenshot_name = 'temp_screen.png'
        while True: # scrolling till white
            small_swipe_down()
            make_a_screenshot(screenshot_name)
            color = get_pixel_color('../data/screenshots/'+screenshot_name, 750, 390)
            print("searching for white ",color)
            # check if the screen is white
            if sum(color[0:3]) > 220*3:
                break

        print("small white found, looking for new day")
        while True:  # scrolling till gray (new day)
            small_swipe_down()
            make_a_screenshot(screenshot_name)
            color = get_pixel_color('../data/screenshots/'+screenshot_name, 750, 390)
            print("searching for gray again ", color)
            # check if the screen is gray (181, 166, 150, 255)
            if color[0] < 200 and color[1] < 200 and color[2] < 200:
                break
        tap(970, 610) # tap on download button
        time.sleep(1.5)
        tap(970, 610) # ensure (open day
        time.sleep(2.5)
        print("Downloaded day, closed day")
        tap(94,180) # close day
        time.sleep(1)






if __name__ == '__main__':
    prog_names = ['Bodyweight 1']
    # download_program(prog_names[0])
    download_program(prog_names[0], from_start=False)