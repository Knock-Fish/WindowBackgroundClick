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
    window_information = Store.root.set_init_labelframe("窗口信息", 340, 180, 630, 340)  # 设置窗口信息框架组件大小和位置
    window_information_labelframe = GUI(window_information)  # 实例化对象
    # 配置窗口标签
    window_information_labelframe.set_label(
        {
            "窗口句柄": [15, 15],
            "窗口类名": [200, 15],
            "窗口标题": [15, 65],
            "线程ID": [15, 115],
            "进程ID": [210, 115],
            "进程名称": [15, 165],
            "进程路径": [15, 215],
            "CPU用量": [15, 265],
            "线程数": [413, 265]
        }
    )

    # 配置窗口文本框
    window_information_labelframe.set_entry(
        [
            {  # 窗口句柄
                'width': 100,
                'x': 90,
                'y': 10,
                'var': "var_hwnd"
            },
            {  # 窗口类名
                'width': 300,
                'x': 275,
                'y': 10,
                'var': 'var_clsname'
            },
            {  # 窗口标题
                'width': 485,
                'x': 90,
                'y': 60,
                'var': 'var_title'
            },
            {  # 线程ID
                'width': 100,
                'x': 90,
                'y': 110,
                'var': 'var_thread_id'
            },
            {  # 进程ID
                'width': 115,
                'x': 275,
                'y': 110,
                'var': 'var_process_id'
            },
            {  # 进程名称
                'width': 300,
                'x': 90,
                'y': 160,
                'var': 'var_process'
            },
            {  # 进程路径
                'width': 485,
                'x': 90,
                'y': 210,
                'var': 'var_p_bin'
            },
            {  # CPU用量
                'width': 305,
                'x': 90,
                'y': 260,
                'var': 'var_mem_percent'
            },
            {  # 线程数
                'width': 100,
                'x': 475,
                'y': 260,
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
        height=60 * Store.scaling_height,
        width=60 * Store.scaling_width,
        borderwidth=-3,
        cursor="target"
    )
    canvas.create_rectangle(
        2 * Store.scaling_width,
        2 * Store.scaling_height,
        53 * Store.scaling_width,
        53 * Store.scaling_height,
        outline="grey"
    )
    image_file_key = Image.open("./static/key.png")
    resized_image_key = image_file_key.resize(
        (
            int(40 * Store.scaling_width),
            int(40 * Store.scaling_height)
        )
    )
    # image_file_key = ttk.PhotoImage(file='./static/key.png')  # 读取图片
    resized_image_key.save('./static/key_temp.png')
    image_file = ttk.PhotoImage(file='./static/key_temp.png')
    canvas.create_image(
        29 * Store.scaling_width,
        29 * Store.scaling_height,
        anchor='center',
        image=image_file
    )  # 将图片显示在画布上
    canvas.place(
        x=510 * Store.scaling_width,
        y=125 * Store.scaling_height
    )  # 放置画布
    canvas.bind("<B1-Motion>", window_information_show_menu)  # 绑定事件

    canvas2 = ttk.Canvas(
        window_information,
        height=80 * Store.scaling_height,
        width=80 * Store.scaling_width,
        borderwidth=-3,
    )
    # image_file2 = ttk.PhotoImage(file='./static/picture.png')  # 读取图片
    image_file2_picture = Image.open("./static/picture.png")
    resized_image_picture = image_file2_picture.resize(
        (
            int(55 * Store.scaling_width),
            int(55 * Store.scaling_height)
        )
    )
    resized_image_picture.save("./static/picture_temp.png")
    image_file2 = ttk.PhotoImage(file="./static/picture_temp.png")
    canvas2.create_image(
        37 * Store.scaling_width,
        37 * Store.scaling_height,
        anchor='center',
        image=image_file2
    )  # 将图片显示在画布上
    canvas2.create_rectangle(
        2 * Store.scaling_width,
        2 * Store.scaling_height,
        73 * Store.scaling_width,
        73 * Store.scaling_height,
        outline="grey"
    )
    canvas2.place(
        x=415 * Store.scaling_width,
        y=115 * Store.scaling_height
    )  # 放置画布


# 替换图片
def picture(pbin):
    try:
        # 获取窗口所在的文件夹
        icon_path = os.path.split(pbin)[0]
        # 使用os模块获取文件夹中所有文件的路径
        listdir = os.listdir(icon_path)
        # 找出后缀为 .ico 的文件
        target = [item for item in listdir if '.ico' in item]
        # 拼接路径并读取该路径 ico 图标
        icon = Image.open(icon_path + "\\" + target[0])
        # 将图片尺寸设置为 55 * 55
        resized_image = icon.resize(
            (
                int(55 * Store.scaling_width),
                int(55 * Store.scaling_height)
            )
        )
        # 保存图片
        resized_image.save('./static/icon.png')
        # 替换图片
        image_file2.config(file='./static/icon.png')
    except:
        # 如未能正确读取到ico图标，则显示默认图片
        image_file2.config(file="./static/picture_temp.png")


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
        picture(p_bin)
        # 添加到globals全局变量模块
        Store.hwnd, Store.p_bin, Store.process_id, Store.point = hwnd, p_bin, process_id, point
    except:
        pass
