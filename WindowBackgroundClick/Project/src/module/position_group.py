from Project.gui import GUI
from Project.src.globals import Store
import win32gui


def position_group_module():
    # 坐标框架组件
    position_group = Store.root.set_init_labelframe("坐标", 225, 445, 400, 180)  # 设置坐标框架组件大小和位置
    position_group_labelframe = GUI(position_group)  # 实例化对象
    # 配置坐标组件标签
    position_group_labelframe.set_label(
        {
            "窗口左上": [15, 10],
            "窗口右上": [205, 10],
            "窗口左下": [15, 60],
            "窗口右下": [205, 60],
            "坐标 x, y": [15, 110]
        }
    )
    # 配置坐标组件文本框
    position_group_labelframe.set_entry(
        [
            {  # 窗口左上
                'width': 100,
                'x': 90,
                'y': 5,
                'var': 'var_top'
            },
            {  # 窗口右上
                'width': 100,
                'x': 280,
                'y': 5,
                'var': 'var_right'
            },
            {  # 窗口左下
                'width': 100,
                'x': 90,
                'y': 55,
                'var': 'var_left'
            },
            {  # 窗口右下
                'width': 100,
                'x': 280,
                'y': 55,
                'var': 'var_bottom'
            },
            {  # 坐标x,y
                'width': 290,
                'x': 90,
                'y': 105,
                'var': 'var_point'
            }
        ]
    )
    # 全局文本框 var 的值
    global vars_dict
    vars_dict = position_group_labelframe.get_local_vars()


def position_group_show_menu(hwnd, point):
    try:
        # 窗口坐标 通过窗口句柄获取 四个角的坐标
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        vars_dict.get('var_left').set(left)
        vars_dict.get('var_top').set(top)
        vars_dict.get('var_right').set(right)
        vars_dict.get('var_bottom').set(bottom)
        vars_dict.get('var_point').set(point)
    except:
        pass
