# coding: utf-8
#
#
"""
window screenshot: https://github.com/ludios/Desktopmagic
tk file dialogs: https://pythonspot.com/tk-file-dialogs/
python template match: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
"""

import functools
import time
from collections import namedtuple

import cv2
import numpy as np
import PIL
import pyautogui
import pywinauto
from matplotlib import pyplot as plt
from PIL import ImageGrab


def makeWait(seconds: float):
    @functools.wraps(makeWait)
    def inner():
        time.sleep(seconds)
    return inner


MatchResult = namedtuple('MatchResult', ['pos', 'val', 'image', 'template'])
BeforeClick = makeWait(0)


class Session():
    def __init__(self):
        self.screenshot = None


session = Session()


def pil2opencv(im):
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def win_screenshot():
    session.screenshot = ImageGrab.grab()
    return session.screenshot


def find(filename):
    img = cv2.imread(filename, 0)
    background = pil2opencv(win_screenshot())
    background = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)

    res = cv2.matchTemplate(img, background, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    return MatchResult(top_left, max_val, img, background)


def click(x, y):
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()


def clickImage(filename):
    res = find(filename)
    w, h = res.image.shape[::-1]

    top_left = res.pos
    center = (top_left[0] + w//2, top_left[1] + h//2)
    click(*center)


def main():
    clickImage("window.jpg")


if __name__ == "__main__":
    main()
