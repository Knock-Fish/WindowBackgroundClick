import threading
import ttkbootstrap as ttk
from Project.gui import GUI
from Project.src.globals import Store
from Project.src.module.window_information import window_information_module
from Project.src.module.background_click_group import background_click_group_module
from Project.src.module.position_group import position_group_module
from Project.src.module.control_group import control_group_module
from Project.method import threading_cycle_click, threading_hotkey, radiobutton_value


def gui_start():
    init_window = ttk.Window()  # 创建窗口root
    root = GUI(init_window)  # 实例化对象
    Store.root = root  # 将 root 添加到全局变量
    Store.init_window = init_window     # 根窗口添加到全局变量
    root.set_init_window("获取窗口句柄-后台自动点击脚本", [1000, 560], "./Project/static/favicon.ico")  # 设置窗口大小和位置
    background_click_group_module()  # 后台点击模块
    position_group_module()  # 坐标模块
    window_information_module()  # 窗口信息模块
    control_group_module()  # 控制模块

    # 开启循环 后台点击、监听键盘输入 线程
    threading.Thread(target=threading_cycle_click, args=(), daemon=True).start()  # 后台点击
    threading.Thread(target=threading_hotkey, args=(), daemon=True).start()  # 监听键盘输入
    radiobutton_value(1)     # 启动默认传入鼠标左键的值
    print("当前运行的线程：", threading.active_count())  # 打印当前启动线程总数

    init_window.mainloop()  # 显示根窗口
