class Store:
    root = None  # 实例化窗口
    init_window = None  # 根窗口
    hwnd = None  # 窗口句柄
    p_bin = None  # 程序路径
    process_id = None  # 进程ID
    point = None  # 线程数
    flag = False  # 控制脚本开关
    background_click_entry_var_time = None  # 时间间隔
    background_click_vars = None  # background_click组件的vars值
    background_click_entry_var_hotkey = None  # 热键
    background_click_group = None  # 后台点击框架
    time_tip = None  # 错误的时间间隔提示
    hwnd_tip = None  # 未获取窗口错误提示
    background_click_labelframe_get_button_value = None  # 按钮指针
    screen_scale_rate = None    # # 缩放比例
    on_release_callback_flag = False    # 启动（停止）按钮防抖
    @staticmethod
    def get(value):
        return value

    @staticmethod
    def set(value):
        return value
