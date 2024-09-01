import win32api
import win32gui
import win32con
import subprocess
import os
import time
from Project.src.globals import Store
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
import keyboard
import re


# 置顶 通过句柄
def set_top():
    try:
        win32gui.SetForegroundWindow(Store.hwnd)
    except:
        pass


# 取消置顶
def set_down():
    try:
        Store.init_window.wm_attributes("-topmost", False)
    except:
        pass


# 脚本置顶
def set_yop_p():
    try:
        Store.init_window.wm_attributes("-topmost", True)
    except:
        pass


# 终止程序
def kill():
    try:
        result = messagebox.askyesno("提示", "是否关闭该进程？", type='yesno')
        if result:
            subprocess.Popen("taskkill /F /T /PID" + ' ' + str(Store.process_id), shell=True)
            subprocess.Popen("taskkill /F /T /IM" + ' ' + str(Store.p_bin), shell=True)
        else:
            return
    except:
        pass


# 打开文件夹
def bin():
    # 把路径分割成 dirname 和 basename，返回一个元组
    pbin = os.path.split(Store.p_bin)[0]  # 获取元组下标为0的参数
    print(pbin)
    os.startfile(str(pbin))  # 打开文件夹


# 鼠标点击事件
# 左键点击
def do_left_click(time_v):
    # 模拟鼠标指针，传送到指定坐标
    long_position = win32api.MAKELONG(0, 0)
    # keyboard.press("w")
    while Store.flag:
        # 模拟鼠标左键按下
        win32api.SendMessage(Store.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        # 模拟鼠标左键弹起
        win32api.SendMessage(Store.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
        time.sleep(time_v)


# 右键点击
def do_right_click(time_v):
    # 模拟鼠标指针，传送到指定坐标
    long_position = win32api.MAKELONG(0, 0)
    while Store.flag:
        # 模拟鼠标右键按下
        win32api.SendMessage(Store.hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, long_position)
        # 模拟鼠标右键弹起
        win32api.SendMessage(Store.hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, long_position)
        time.sleep(time_v)


# 获取选中单选框的值
def radiobutton_value(value):
    global r_v
    r_v = int(value)


# 脚本线程
def threading_cycle_click():
    while True:
        if Store.flag and Store.hwnd is not None:
            if r_v == 1:
                do_left_click(interval)
            else:
                do_right_click(interval)
        else:
            time.sleep(1)


# 获取用户设置的点击间隔的值
def get_interval():
    try:
        global interval
        Store.time_tip.place_forget()
        interval = float(Store.background_click_entry_var_time.get())
        if interval == 0:
            return Store.time_tip.place(
                x=150 * Store.scaling_width,
                y=110 * Store.scaling_height
            )
        Store.flag = True
        # 切换停止按钮
        Store.background_click_labelframe_get_button_value.get("stop").place(
            x=20 * Store.scaling_width,
            y=200 * Store.scaling_height
        )
        Store.background_click_labelframe_get_button_value.get("start").place_forget()
    except:
        # 错误提示
        Store.time_tip.place(
            x=150 * Store.scaling_width,
            y=110 * Store.scaling_height
        )


# 获取按钮指针
def get_button(value):
    try:
        global button_value
        button_value = value
    except:
        print("获取按钮指针失败")


# 启动脚本
def cycle_click():
    if Store.hwnd is not None:
        Store.hwnd_tip.place_forget()
        get_interval()
    else:
        Store.hwnd_tip.place(
            x=120 * Store.scaling_width,
            y=205 * Store.scaling_height
        )


# 停止脚本
def clear_cycle_click():
    Store.flag = False
    # 切换启动按钮
    Store.background_click_labelframe_get_button_value.get("start").place(
        x=20 * Store.scaling_width,
        y=200 * Store.scaling_height
    )
    Store.background_click_labelframe_get_button_value.get("stop").place_forget()


def on_release_callback(event):
    if event.name.upper() == hotkey:
        Store.on_release_callback_flag = True
    else:
        Store.on_release_callback_flag = False


# 启动和停止热键
def threading_hotkey():
    global hotkey
    hotkey = Store.background_click_entry_var_hotkey.get().upper()
    keyboard.on_release(on_release_callback)
    while True:
        if Store.on_release_callback_flag:
            Store.on_release_callback_flag = False
            if Store.flag:
                clear_cycle_click()
            else:
                cycle_click()
                hotkey = Store.background_click_entry_var_hotkey.get().upper()
        hotkey = Store.background_click_entry_var_hotkey.get().upper()
        time.sleep(0.1)
