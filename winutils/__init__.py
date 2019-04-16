# coding: utf-8
#
# coding: utf-8
#

import io
import os
from collections import namedtuple

import win32con
from PIL import ImageGrab

import win32api
import win32gui
import win32process

Window = namedtuple('Window', ['hwnd', 'text', 'rect', 'pid', 'path'])


def isRealWindow(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False
    if win32gui.GetParent(hwnd) != 0:
        return False
    hasOwner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasOwner)
            or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasOwner)):
        if win32gui.GetWindowText(hwnd):
            return True
    return False


def callback(hwnd, windows):
    if not isRealWindow(hwnd):
        return
    rect = win32gui.GetWindowRect(hwnd)
    text = win32gui.GetWindowText(hwnd)
    threadpid, procpid = win32process.GetWindowThreadProcessId(hwnd)
    pwnd = None
    procpath = None
    try:
        pwnd = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False,
                                    procpid)
        procpath = win32process.GetModuleFileNameEx(pwnd, 0)
    except:
        pass

    windows.append(Window(hwnd, text, rect, procpid, procpath))


def list_app():
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# def app_find(tpp):
#     """
#     Args:
#         tpp: title or pid or path
#     """
#     for app in list_app():
#         if app.text == tpp:
#             return app
#         if app.pid == tpp:
#             return app
#         try:
#             # windows has no os.path.samefile
#             if os.stat(app.path) == os.stat(tpp):
#                 return app
#         except (WindowsError, TypeError):
#             pass
#     return None


# class App(object):
#     def __init__(self, name):
#         self._name = name

#     def screenshot(self, filename):
#         app = app_find(self._name)
#         if app is None:
#             return None, False

#         img = ImageGrab.grab(app.rect)
#         return img

#     def is_alive(self):
#         app = app_find(self._name)
#         return app is not None


if __name__ == "__main__":
    for app in list_app():
        print("App:", app)
