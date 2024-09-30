import win32ui
from Project.gui import GUI
from Project.src.globals import Store
import win32api
import win32gui
import win32process
import psutil
from Project.src.module.position_group import position_group_show_menu
import ttkbootstrap as ttk
import os
from PIL import Image


def window_information_module():
    # 窗口信息框架组件
    window_information = Store.root.set_init_labelframe("窗口信息", 272, 144, 504, 272)  # 设置窗口信息框架组件大小和位置
    window_information_labelframe = GUI(window_information)  # 实例化对象
    # 配置窗口标签
    window_information_labelframe.set_label(
        {
            "窗口句柄": [12, 12],
            "窗口类名": [160, 12],
            "窗口标题": [12, 52],
            "线程ID": [12, 92],
            "进程ID": [168, 92],
            "进程名称": [12, 132],
            "进程路径": [12, 172],
            "CPU用量": [12, 212],
            "线程数": [330, 212]
        }
    )

    # 配置窗口文本框
    window_information_labelframe.set_entry(
        [
            {  # 窗口句柄
                'width': 80,
                'x': 72,
                'y': 8,
                'var': "var_hwnd"
            },
            {  # 窗口类名
                'width': 240,
                'x': 220,
                'y': 8,
                'var': 'var_clsname'
            },
            {  # 窗口标题
                'width': 388,
                'x': 72,
                'y': 48,
                'var': 'var_title'
            },
            {  # 线程ID
                'width': 80,
                'x': 72,
                'y': 88,
                'var': 'var_thread_id'
            },
            {  # 进程ID
                'width': 92,
                'x': 220,
                'y': 88,
                'var': 'var_process_id'
            },
            {  # 进程名称
                'width': 240,
                'x': 72,
                'y': 128,
                'var': 'var_process'
            },
            {  # 进程路径
                'width': 388,
                'x': 72,
                'y': 168,
                'var': 'var_p_bin'
            },
            {  # CPU用量
                'width': 244,
                'x': 72,
                'y': 208,
                'var': 'var_mem_percent'
            },
            {  # 线程数
                'width': 80,
                'x': 380,
                'y': 208,
                'var': 'var_num_threads'
            }
        ]
    )
    # 全局文本框 var 的值
    global window_information_vars, image_file, image_file2  # 图片(如果显示图片这个功能定义在一个方法里，image_file，一定要声明为全局变量，窗口才会显示图片)
    window_information_vars = window_information_labelframe.get_local_vars()

    # 创建画布
    canvas = ttk.Canvas(
        window_information,
        height=48.5 * Store.screen_scale_rate,
        width=48.5 * Store.screen_scale_rate,
        borderwidth=-3,
        cursor="target"
    )
    canvas.create_rectangle(
        2 * Store.screen_scale_rate,
        2 * Store.screen_scale_rate,
        42 * Store.screen_scale_rate,
        42 * Store.screen_scale_rate,
        outline="grey"
    )
    image_file_key = Image.open("./Project/static/key.png")
    resized_image_key = image_file_key.resize(
        (
            int(32 * Store.screen_scale_rate),
            int(32 * Store.screen_scale_rate)
        )
    )
    # image_file_key = ttk.PhotoImage(file='../Project/static/key.png')  # 读取图片
    resized_image_key.save('./Project/static/key_temp.png')
    image_file = ttk.PhotoImage(file='./Project/static/key_temp.png')
    canvas.create_image(
        23 * Store.screen_scale_rate,
        23 * Store.screen_scale_rate,
        anchor='center',
        image=image_file
    )  # 将图片显示在画布上
    canvas.place(
        x=408 * Store.screen_scale_rate,
        y=100 * Store.screen_scale_rate
    )  # 放置画布
    canvas.bind("<B1-Motion>", window_information_show_menu)  # 绑定事件

    canvas2 = ttk.Canvas(
        window_information,
        height=65 * Store.screen_scale_rate,
        width=65 * Store.screen_scale_rate,
        borderwidth=-3,
    )
    # image_file2 = ttk.PhotoImage(file='../Project/static/picture.png')  # 读取图片
    image_file2_picture = Image.open("./Project/static/picture.png")
    resized_image_picture = image_file2_picture.resize(
        (
            int(44 * Store.screen_scale_rate),
            int(44 * Store.screen_scale_rate)
        )
    )
    resized_image_picture.save("./Project/static/picture_temp.png")
    image_file2 = ttk.PhotoImage(file="./Project/static/picture_temp.png")
    canvas2.create_image(
        29 * Store.screen_scale_rate,
        29 * Store.screen_scale_rate,
        anchor='center',
        image=image_file2
    )  # 将图片显示在画布上
    canvas2.create_rectangle(
        2 * Store.screen_scale_rate,
        2 * Store.screen_scale_rate,
        55 * Store.screen_scale_rate,
        55 * Store.screen_scale_rate,
        outline="grey"
    )
    canvas2.place(
        x=332 * Store.screen_scale_rate,
        y=92 * Store.screen_scale_rate
    )  # 放置画布


def get_exe_icon(exe_path):
    try:
        # 获取exe文件的图标
        large, small = win32gui.ExtractIconEx(exe_path, 0)
        win32gui.DestroyIcon(small[0])
        # 创建一个设备上下文
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(
            hdc,
            int(32 * Store.screen_scale_rate),
            int(32 * Store.screen_scale_rate)
        )
        # 在设备上下文中绘制图标
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])

        # 保存图标到本地文件
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (
                int(bmpinfo['bmWidth'] * Store.screen_scale_rate),
                int(bmpinfo['bmHeight'] * Store.screen_scale_rate)
            ),
            bmpstr, 'raw', 'BGRX', 0, 1)
        # 将图片尺寸设置为 55 / 55
        img = img.resize(
            (
                int(44 * Store.screen_scale_rate),
                int(44 * Store.screen_scale_rate)
            )
        )
        img.save('./Project/static/icon.png')
        image_file2.config(file='./Project/static/icon.png')

    except:
        # 如未能正确读取到图标，则显示默认图片
        image_file2.config(file="./Project/static/picture_temp.png")


def window_information_show_menu(event):
    try:
        vars_dict = window_information_vars  # 获取文本框 var 的值
        point = win32api.GetCursorPos()  # 鼠标位置

        hwnd = win32gui.WindowFromPoint(point)  # 窗口句柄
        vars_dict.get('var_hwnd').set(hwnd)

        title = win32gui.GetWindowText(hwnd)  # 窗口标题
        vars_dict.get('var_title').set(title)

        clsname = win32gui.GetClassName(hwnd)  # 窗口类名
        vars_dict.get('var_clsname').set(clsname)

        # 线程ID，进程ID
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
        vars_dict.get('var_thread_id').set(thread_id)

        # 程序名称 通过进程ID获取
        process = psutil.Process(process_id)
        vars_dict.get('var_process_id').set(process_id)
        vars_dict.get('var_process').set(process.name())

        # 程序路径 通过进程ID获取
        p_bin = psutil.Process(process_id).exe()
        vars_dict.get('var_p_bin').set(p_bin)

        # CPU利用率
        mem_percent = psutil.Process(process_id).memory_percent()
        vars_dict.get('var_mem_percent').set(mem_percent)

        # 线程数 通过进程ID获取
        num_threads = psutil.Process(process_id).num_threads()
        vars_dict.get('var_num_threads').set(num_threads)
        position_group_show_menu(hwnd, point)
        # 替换图标
        get_exe_icon(p_bin)
        # 添加到globals全局变量模块
        Store.hwnd, Store.p_bin, Store.process_id, Store.point = hwnd, p_bin, process_id, point
    except:
        pass
