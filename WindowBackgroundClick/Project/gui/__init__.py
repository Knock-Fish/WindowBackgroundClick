import ttkbootstrap as ttk
from Project.method import *
from Project.src.globals import Store
from functools import partial
import threading


class GUI:
    def __init__(self, init_window_name):
        # 根窗口
        self.init_window_name = init_window_name
        # 获取屏幕的大小
        self.screen_width = self.init_window_name.winfo_screenwidth()
        self.screen_height = self.init_window_name.winfo_screenheight()
        self.if_screen_size()
        # 存放文本框的数据
        self.local_vars = {}
        # 获取用户输入文本框的值
        self.entry_value = {}
        # 存放按钮的指针
        self.button_value = {}
        # 缩放比例
        self.scaling_width = 0
        self.scaling_height = 0
        self.if_screen_size()

    # 不同分辨率下布局兼容处理
    def if_screen_size(self):
        # 新分辨率 / 原始分辨率 = 缩放比例
        self.scaling_width = self.screen_width / 1920
        self.scaling_height = self.screen_height / 1080
        # 将缩放比例保存到全局变量模块
        Store.scaling_width = self.scaling_width
        Store.scaling_height = self.scaling_height

    # 设置窗口
    def set_init_window(self, window_title, size, icon):
        self.init_window_name.title(window_title)  # 定义窗口标题
        # 窗口大小和位置参数
        window_width, window_height = int(size[0] * self.scaling_width), int(size[1] * self.scaling_height)
        print(int(size[0] * self.scaling_width))
        # 定义窗口大小和窗口弹出时的默认展示位置
        self.init_window_name.geometry(
            "{}x{}+{}+{}".format(
                window_width,
                window_height,
                0,
                0
            )
        )
        # 固定页面不可放大缩小
        self.init_window_name.resizable(False, False)
        # 设置窗口左上 icon 图标
        self.init_window_name.iconbitmap(icon)

    # 设置按钮
    def set_button(self, create_button_component):
        for item in create_button_component:  # 遍历字典
            parameter = create_button_component[item]  # 保存外层字典的键名
            name = parameter.get('name')  # 获取按钮的变量名
            x, y = parameter.get('x'), parameter.get('y')  # 获取内层字典的 x,y 值
            # 触发事件的回调函数，默认为 None
            callback = parameter.get('callback') if 'callback' in parameter != False else None
            # 函数传参
            fun_p = parameter.get('fun_p') if 'fun_p' in parameter != False else None
            # 拼接成完整的函数调用
            str_fun = ''
            if callback is not None:
                if fun_p is not None:
                    str_fun = '{}({})'.format(callback, fun_p)
                else:
                    str_fun = '{}()'.format(callback)
            else:
                str_fun = None
            # 按钮的样式，默认为 primary
            btn_style = parameter.get('btn_style') if 'btn_style' in parameter != False else "primary"
            # 如果name不为None，则为当前按钮添加变量名，否则直接创建按钮（减少无意义的变量）
            if name is not None:
                exec("{} = ttk.Button("
                     "self.init_window_name,"  # 添加到指定窗口
                     "text=item,"  # 按钮名称 = 外层元组的键名
                     "bootstyle=btn_style,"  # 按钮样式
                     "command=lambda f=str_fun: eval(f)"  # 触发事件的回调函数
                     ")".format(name))
                exec("{}.place("  # 放置部件
                     "x=x * self.scaling_width,"
                     "y=y * self.scaling_height"
                     ")".format(name))
                # 将按钮指针保存到 self.button_value 元组中
                self.button_value[name] = eval(name)
            else:
                ttk.Button(
                    self.init_window_name,  # 添加到指定窗口
                    text=item,  # 按钮名称 = 外层元组的键名
                    bootstyle=btn_style,  # 按钮样式
                    command=lambda f=str_fun: eval(f)  # 触发事件的回调函数
                ).place(  # 放置部件
                    x=x * self.scaling_width,
                    y=y * self.scaling_height
                )

    # 配置文本框，用来放置数据
    def set_entry(self, create_entry_component):
        for item in create_entry_component:  # 遍历列表
            # 设置文本框的属性，默认为 只读
            state = item.get('state') if 'state' in item != False else "readonly"
            # 设置文本框的样式，默认为 primary
            entry_style = item.get('entry_style') if 'entry_style' in item != False else "primary"
            # 如设置了var参数，则会对文本框指定的值名进行赋值 ttk.StringVar()
            if 'var' in item:
                temp = item.get("var")
                exec(temp + '= ttk.StringVar()', globals(), self.local_vars)
                var = self.local_vars.get(temp)
            else:
                var = None
            # 如果var不为None，则为当前文本框添加变量名，否则直接创建文本框（防止出现entry_None无意义的变量）
            if var is not None:
                # 给文本框添加变量名，变量名为：entry_ + 指定的var参数的值名。可以通过此变量名获取用户输入到文本框的值
                exec("entry_{} = ttk.Entry("
                     "self.init_window_name,"  # 添加到指定窗口
                     "bootstyle=entry_style,"  # 文本框样式
                     "textvariable=var,"  # var初始化文本框的内容
                     "state=state"  # 文本框属性
                     ")".format(item.get("var")))
                exec("entry_{}.place("  # 放置部件
                     "x=item.get('x') * self.scaling_width,"
                     "y=item.get('y') * self.scaling_height,"
                     "width={},"
                     "height=35 * self.scaling_height"
                     ")".format(item.get("var"), item.get('width') * self.scaling_width))
                # 文本框变量名 以键值对 保存到 entry_value 中
                self.entry_value["entry_{}".format(item.get("var"))] = eval("entry_{}".format(item.get("var")))
            else:
                ttk.Entry(
                    self.init_window_name,  # 添加到指定窗口
                    bootstyle=entry_style,  # 文本框样式
                    textvariable=var,  # var初始化文本框的内容
                    state=state  # 文本框属性
                ).place(
                    x=item.get('x') * self.scaling_width,
                    y=item.get('y') * self.scaling_height,
                    width=item.get('width') * self.scaling_width,  # 文本框的宽度
                )

    # 程序添加标签，用来标注
    def set_label(self, create_label_component):
        for item in create_label_component:  # 遍历字典
            x, y = create_label_component.get(item)[0:2]  # x,y 的值
            if len(create_label_component.get(item)) == 3:  # 判断列表中是否有 样式 参数
                label_style = create_label_component.get(item)[2]
            else:
                label_style = "primary"  # 如没有指定样式，则默认为 primary
            ttk.Label(
                self.init_window_name,  # 添加到指定窗口
                text=item,  # 部件名称
                bootstyle=label_style  # 部件样式
            ).place(  # 放置部件
                x=x * self.scaling_width,
                y=y * self.scaling_height
            )

    # 单选框
    def set_radiobutton(self, var, create_radiobutton_component):
        for item in create_radiobutton_component:  # 遍历字典
            parameter = create_radiobutton_component[item]  # 保存外层字典的键名
            x, y = parameter.get('x'), parameter.get('y')  # 获取内层字典的 x,y 值
            # 设置单选框的值，默认为 None
            value = parameter.get('value') if 'value' in parameter != False else None
            # 触发事件的回调函数，默认为 None
            callback = eval(parameter.get('callback')) if 'callback' in parameter != False else None
            # 单选框的样式。默认为 primary
            radio_button_style = parameter.get('btn_style') if 'btn_style' in parameter != False else "primary"
            ttk.Radiobutton(
                self.init_window_name,  # 添加到指定的窗口
                text=item,  # 单选框的名称
                variable=var,  # 将选中的单选框的 value 值保存到 var，然后赋值给 variable
                value=value,  # 设置单选框的值
                command=lambda: callback('{}'.format(var.get())),  # 触发事件的回调函数
                bootstyle=radio_button_style  # 单选框的样式
            ).place(  # 放置部件
                x=x * self.scaling_width,
                y=y * self.scaling_height
            )

    # 标签框架
    def set_init_labelframe(self, text, x, y, width, height, position="center", labelframe_style="primary"):
        l_frame = ttk.Labelframe(
            self.init_window_name,  # 添加到指定的窗口
            text=text,  # 框架标题
            bootstyle=labelframe_style  # 框架样式，默认为 primary
        )
        l_frame.place(
            # 框架位置和大小
            anchor=position,  # 默认为 center
            x=x * self.scaling_width,
            y=y * self.scaling_height,
            width=width * self.scaling_width,
            height=height * self.scaling_height
        )
        return l_frame

    # 获取存放在已经定义var参数的文本框数据
    def get_local_vars(self):
        return self.local_vars

    # 获取存放在button_value的指针
    def get_button_value(self):
        return self.button_value
