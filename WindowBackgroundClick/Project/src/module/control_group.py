from Project.gui import GUI
from Project.src.globals import Store


def control_group_module():
    # 控制框架组件
    control_group = Store.root.set_init_labelframe("控制", 436, 356, 180, 144)  # 设置控制框架组件大小和位置
    control_group_labelframe = GUI(control_group)  # 实例化对象
    # 配置按钮
    control_group_labelframe.set_button(
        {
            "窗口前台": {
                'x': 12,
                'y': 48,
                'callback': 'set_top'
            },
            "取消置顶": {
                'x': 96,
                'y': 8,
                'callback': 'set_down'
            },
            "脚本置顶": {
                'x': 12,
                'y': 8,
                'callback': 'set_yop_p'
            },
            "结束进程": {
                'x': 96,
                'y': 48,
                'btn_style': 'danger',
                'callback': 'kill'
            },
            "打开文件所在位置": {
                'x': 32,
                'y': 88,
                'callback': 'bin'
            }
        }
    )
