import mss
import cv2
import numpy
import time
from PIL import Image
import os
from pynput import keyboard

def on_press(key):
    global running
    global capture_screenshot
    if key == keyboard.Key.right:
        capture_screenshot = True
    elif key == keyboard.Key.down:
        running = False

def get_unique_filename():
    current_time = time.strftime("%Y%m%d-%H%M%S")
    return f"screenshot_{current_time}.png"

def main(folder_name):
    global running
    global capture_screenshot
    running = True
    capture_screenshot = False

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print("To take a screenshot, press the right arrow key. To quit, press the down arrow key.")
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 2560, "height": 1440} #for my apple thunderbolt display
        #monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080} #for a normal monitor
        sct_img = sct.grab(monitor)

        while running:
            if capture_screenshot:
                img = numpy.array(sct_img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(img)
                filename = get_unique_filename()
                image.save(os.path.join(folder_name, filename))
                print(f"Screenshot saved: {filename}")
                capture_screenshot = False
            time.sleep(0.1)
            sct_img = sct.grab(monitor)

    listener.stop()

if __name__ == "__main__":
    folder_name = input("Enter the name of the folder to save the screenshots: ")
    os.makedirs(folder_name, exist_ok=True)
    main(folder_name)











