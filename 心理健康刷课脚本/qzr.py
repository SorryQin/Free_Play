import time
import cv2
import numpy as np
import pyautogui
from pywinauto.application import Application

# 定义函数：格式化当前时间并添加到信息前
def print_with_timestamp(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{current_time}] {message}")

# 定义函数：在显示器左半部分截图中查找指定图片的位置
def find_image_in_left_screen(image_path):
    try:
        # 等待 1 秒
        time.sleep(1)
        # 获取屏幕尺寸
        screen_width, screen_height = pyautogui.size()
        # 截取显示器左半部分的截图
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width // 2, screen_height))
        screenshot = np.asarray(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # 读取要查找的按钮图片
        button_image = cv2.imread(image_path)
        if button_image is None:
            print_with_timestamp(f"无法读取图片: {image_path}")
            return None
        result = cv2.matchTemplate(screenshot, button_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 如果匹配度足够高，返回按钮位置
        if max_val > 0.6:
            h, w, _ = button_image.shape
            button_center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return button_center
    except Exception as e:
        print_with_timestamp(f"查找图片时出现错误: {e}")
    return None

# 定义函数：点击指定位置
def click_position(position):
    try:
        pyautogui.click(position)
    except Exception as e:
        print_with_timestamp(f"点击位置时出现错误: {e}")

# 定义函数：监测视频是否播放结束（基于结束图标）
def is_video_finished(end_icon_image_path):
    end_icon_pos = find_image_in_left_screen(end_icon_image_path)
    return end_icon_pos is not None

# 定义函数：将页面滚动到最下端
def scroll_to_bottom():
    try:
        # 假设每次滚动的步数为 -1000，可根据实际情况调整
        scroll_step = -10000
        while True:
            pyautogui.scroll(scroll_step)
            time.sleep(0.5)
            # 可以添加一些条件来判断是否已经滚动到最下端，这里简单处理
            break
    except Exception as e:
        print_with_timestamp(f"滚动页面时出现错误: {e}")

# 主函数
def main():
    play_button_path = "C:/Users/62544/Desktop/shua/Qin/play_button.png"  # 播放按钮图片路径
    next_button_path = "C:/Users/62544/Desktop/shua/Qin/next_button.png"  # 下一节按钮图片路径
    end_icon_image_path = "C:/Users/62544/Desktop/shua/Qin/end_icon.png"  # 结束图标图片路径

    while True:
        # 查找播放按钮并点击
        play_button_pos = find_image_in_left_screen(play_button_path)
        if play_button_pos:
            click_position(play_button_pos)
            print_with_timestamp("点击了播放按钮")

            # 监测视频是否播放结束
            while not is_video_finished(end_icon_image_path):
                time.sleep(1)
            print_with_timestamp("监测到任务点已完成")

            # 查找下一节按钮并点击
            next_button_pos = find_image_in_left_screen(next_button_path)
            if next_button_pos:
                click_position(next_button_pos)
                print_with_timestamp("点击了下一节按钮")
            else:
                print_with_timestamp("未找到下一节按钮，尝试滚动页面")
                # 滚动页面到最下端
                scroll_to_bottom()
                # 再次查找下一节按钮
                next_button_pos = find_image_in_left_screen(next_button_path)
                if next_button_pos:
                    click_position(next_button_pos)
                    print_with_timestamp("滚动后点击了下一节按钮")
                    # 等待 1 秒
                    time.sleep(1)
                    # 再次检测下一节按钮
                    next_button_pos_again = find_image_in_left_screen(next_button_path)
                    if next_button_pos_again:
                        click_position(next_button_pos_again)
                        print_with_timestamp("1 秒后再次点击了下一节按钮")
                    else:
                        print_with_timestamp("1 秒后未找到下一节按钮，继续监测")
                else:
                    print_with_timestamp("滚动后仍未找到下一节按钮，继续监测")
        else:
            print_with_timestamp("未找到播放按钮，继续监测")

        # 每次循环间隔一段时间，避免过度占用资源
        time.sleep(1)

if __name__ == "__main__":
    main()