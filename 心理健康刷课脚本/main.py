import time
import cv2
import numpy as np
from pywinauto.application import Application

# 定义函数：在窗口截图中查找指定图片的位置
def find_image_in_window(window, image_path):
    hwnd = window.wrapper_object().handle
    app = Application(backend="uia").connect(handle=hwnd)
    dlg_spec = app.window(handle=hwnd)
    # 截取窗口截图
    screenshot = dlg_spec.capture_as_image()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # 读取要查找的按钮图片
    button_image = cv2.imread(image_path)
    result = cv2.matchTemplate(screenshot, button_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 如果匹配度足够高，返回按钮位置
    if max_val > 0.8:
        h, w, _ = button_image.shape
        button_center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
        return button_center
    return None

# 定义函数：点击指定位置
def click_position(window, position):
    hwnd = window.wrapper_object().handle
    app = Application(backend="uia").connect(handle=hwnd)
    dlg_spec = app.window(handle=hwnd)
    dlg_spec.click_input(coords=position)

# 定义函数：监测视频是否播放结束（基于结束图标）
def is_video_finished(window, end_icon_image_path):
    end_icon_pos = find_image_in_window(window, end_icon_image_path)
    return end_icon_pos is not None

# 主函数
def main():
    # 连接到目标窗口（根据窗口标题修改）
    app = Application(backend="uia").connect(title="目标窗口标题")
    window = app.window(title="目标窗口标题")

    play_button_path = "play_button.png"  # 播放按钮图片路径
    next_button_path = "next_button.png"  # 下一节按钮图片路径
    end_icon_image_path = "end_icon.png"  # 结束图标图片路径

    while True:
        # 查找播放按钮并点击
        play_button_pos = find_image_in_window(window, play_button_path)
        if play_button_pos:
            click_position(window, play_button_pos)
            print("点击了播放按钮")

            # 监测视频是否播放结束
            while not is_video_finished(window, end_icon_image_path):
                time.sleep(1)

            # 查找下一节按钮并点击
            next_button_pos = find_image_in_window(window, next_button_path)
            if next_button_pos:
                click_position(window, next_button_pos)
                print("点击了下一节按钮")
        else:
            print("未找到播放按钮，继续监测")

        # 每次循环间隔一段时间，避免过度占用资源
        time.sleep(1)

if __name__ == "__main__":
    main()
