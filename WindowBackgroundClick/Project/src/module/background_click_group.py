import time

import keyboard

from Project.gui import GUI
from Project.src.globals import Store
import ttkbootstrap as ttk


def background_click_group_module():
    global background_click_group
    # 后台点击框架组件
    background_click_group = Store.root.set_init_labelframe("后台点击", 825, 271, 310, 525)  # 设置后台点击框架组件大小和位置
    background_click_labelframe = GUI(background_click_group)  # 实例化对象
    Store.background_click_group = background_click_group
    # 配置标签
    background_click_labelframe.set_label(
        {
            "点击类型": [20, 30],
            "每次点击间隔时间": [20, 80],
            "秒": [260, 80],
            "启动和停止和热键": [20, 140],
            # "请输入正确的值": [150, 110, "danger"],
        }
    )

    # 配置文本框
    background_click_labelframe.set_entry(
        [
            {  # 每次点击间隔时间
                'width': 100,
                'x': 155,
                'y': 75,
                'var': 'var_time',
                'state': None
            },
            {  # 启动和停止和热键
                'width': 100,
                'x': 155,
                'y': 135,
                'var': 'var_hotkey',
                # 'state': None
            }
        ]
    )
    var = ttk.StringVar()  # 被选择单选框的值赋值给 var
    var.set(1)  # 默认选中鼠标左键
    # 配置单选框
    background_click_labelframe.set_radiobutton(
        var,
        {
            "鼠标左键": {
                'x': 100,
                'y': 32,
                'value': 1,
                'callback': 'radiobutton_value',
            },
            "鼠标右键": {
                'x': 200,
                'y': 32,
                'value': 2,
                'callback': 'radiobutton_value'
            },
        },
    )
    # 全局文本框 var 的值
    global background_click_vars
    background_click_vars = background_click_labelframe.get_local_vars()
    # 初始化间隔时间为1
    background_click_vars.get('var_time').set(1)
    # 初始化热键
    background_click_vars.get('var_hotkey').set('X')

    def get_key_value(even):
        if Store.flag:
            print("脚本启动中……")
            time.sleep(0.1)
        else:
            key = keyboard.read_key()
            background_click_vars.get('var_hotkey').set(key.upper())
            Store.background_click_entry_var_hotkey = background_click_labelframe.entry_value.get("entry_var_hotkey")
            Store.init_window.focus_set()
            time.sleep(0.1)

    background_click_labelframe.entry_value.get("entry_var_hotkey").bind('<Key>', get_key_value)
    # 用户输入在点击间隔时间文本框的值保存到globals全局变量模块
    Store.background_click_entry_var_time = background_click_labelframe.entry_value.get("entry_var_time")
    # 用户设置热键的值保存到globals全局变量模块
    Store.background_click_entry_var_hotkey = background_click_labelframe.entry_value.get("entry_var_hotkey")
    # 配置按钮
    background_click_labelframe.set_button(
        {
            '启动脚本': {
                'name': 'start',
                'x': 20,
                'y': 200,
                'callback': 'cycle_click',
            },
            '停止脚本': {
                'name': 'stop',
                'x': 20,
                'y': 200,
                'btn_style': 'danger',
                'callback': 'clear_cycle_click',
            }
        }
    )
    background_click_labelframe.get_button_value().get("stop").place_forget()
    Store.background_click_labelframe_get_button_value = background_click_labelframe.get_button_value()
    Store.time_tip = ttk.Label(
        background_click_group,
        text="请输入正确的值",
        bootstyle="danger"
    )
    Store.hwnd_tip = ttk.Label(
        background_click_group,
        text="未获取到指定的窗口",
        bootstyle="danger"
    )
