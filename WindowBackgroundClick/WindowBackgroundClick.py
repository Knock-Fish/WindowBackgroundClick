from Project.src.module.gui_start import gui_start
from win32api import GetSystemMetrics
from Project.src.globals import Store
import win32gui
import win32con
import win32print


def get_real_resolution():
    # 获取真实的分辨率
    hdc = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    # 获取缩放后的分辨率
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


real_resolution = get_real_resolution()
screen_size = get_screen_size()
# 真实的分辨率 / 获取缩放后的分辨率 = 缩放比例
# 缩放存放存入全局模块中
Store.screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)

if __name__ == '__main__':
    gui_start()
