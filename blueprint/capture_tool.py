#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
"""
用于Windows界面快速截图，并替换选中的文件

- 实现：

依赖了QQ2011版的截图小工具，使用PIL从剪贴板中获取截图
"""

import argparse
import os
import subprocess
import sys
import tkinter as tk
import tkinter.filedialog
from time import sleep
from tkinter import IntVar, StringVar

import win32clipboard
from PIL import ImageGrab, ImageTk

__dir__ = os.path.dirname(os.path.abspath(__file__))


def empty_clipboard():
    """empty clipboard"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replace", action="store_true",
                        help="replace exists file")
    args = parser.parse_args()

    empty_clipboard()

    root = tkinter.Tk()

    def on_screenshot(event=None):
        # 用于PC自动化中，方便的选择图片和替换图片
        subprocess.call(os.path.join(__dir__, "SnapShot.exe"), shell=True)

        clipimage = ImageGrab.grabclipboard()
        if not clipimage:
            sys.exit("Clipboard empty")
        # photo = ImageTk.PhotoImage(clipimage)
        filename = tk.filedialog.asksaveasfilename(
            title="要保存的文件", filetypes=(("jpeg file", "*.jpg"),))
        if filename:
            if not filename.endswith(".jpg"):
                filename = filename + ".jpg"
            clipimage.save(filename)
        empty_clipboard()

    tk.Button(root, text="截图", command=on_screenshot).pack()
    tk.Button(root, text="退出", command=root.destroy).pack(
        side=tk.RIGHT)
    # tk.Label(root, image=photo).pack()

    # def save():
    #     filename = tk.filedialog.asksaveasfilename(
    #         title="要保存的文件", filetypes=(("jpeg file", "*.jpg"),))
    #     if filename:
    #         if not filename.endswith(".jpg"):
    #             filename = filename + ".jpg"
    #         clipimage.save(filename)
    #     empty_clipboard()

    # root.after(0, save)  # 延迟调用

    # bring tkinter window to the top
    root.title("截图工具")
    root.geometry("300x100")
    root.bind("<Control-f>", on_screenshot)
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

    # root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
