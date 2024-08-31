from Project.gui import GUI
from Project.src.globals import Store


def control_group_module():
    # 控制框架组件
    control_group = Store.root.set_init_labelframe("控制", 545, 445, 225, 180)  # 设置控制框架组件大小和位置
    control_group_labelframe = GUI(control_group)  # 实例化对象
    # 配置按钮
    control_group_labelframe.set_button(
        {
            "窗口前台": {
                'x': 15,
                'y': 60,
                'callback': 'set_top'
            },
            "取消置顶": {
                'x': 120,
                'y': 10,
                'callback': 'set_down'
            },
            "脚本置顶": {
                'x': 15,
                'y': 10,
                'callback': 'set_yop_p'
            },
            "结束进程": {
                'x': 120,
                'y': 60,
                'btn_style': 'danger',
                'callback': 'kill'
            },
            "打开文件所在位置": {
                'x': 40,
                'y': 110,
                'callback': 'bin'
            }
        }
    )
