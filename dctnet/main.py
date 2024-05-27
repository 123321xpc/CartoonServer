import os
import tkinter as tk

import cv2
from PIL import Image, ImageTk

from source.cartoonize import Cartoonizer


def get_model_list(model_dir):
    list_models = []
    m_dirs = os.listdir(model_dir)
    for dir in m_dirs:
        path_model = os.path.join(model_dir, dir)
        list_models.append(path_model)
    return list_models


list_modules: list[str] = get_model_list("models")  # 获取模型目录下的所有模型

algo = Cartoonizer(list_modules[1])  # 初始化Cartoonizer类，指定第一个模型


# 更新并显示视频帧的函数
def show_frame():
    _, frame = cap.read()  # 从摄像头读取一帧
    resized_frame = cv2.resize(frame, (200, 150))  # 调整帧的大小
    cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGBA)  # 将帧颜色从BGR转换为RGBA
    img = Image.fromarray(cv2image)  # 将数组转换为图像

    imgtk = ImageTk.PhotoImage(image=img)  # 创建Tkinter兼容的图片
    for label in image_labels:
        label.imgtk = imgtk  # 引用更新，防止Python的垃圾回收
        label.configure(image=imgtk)  # 更新标签的显示图片

    main_label.after(10, show_frame)  # 每10毫秒调用一次函数自身，更新帧


# 创建窗口和布局的函数
def create_window():
    global main_label, image_labels, cap
    cap = cv2.VideoCapture(0)  # 打开摄像头

    window = tk.Tk()
    window.title("Camera Interface with Titles")  # 窗口标题
    window.geometry('900x400')  # 窗口尺寸

    title_texts = ["原画", "anime", "artstyle", "handdrawn", "sketch"]  # 各图像的标题文本

    # 创建并布置包含主图像及其标题的框架
    main_frame = tk.Frame(window)
    main_frame.pack(side="top", fill="both", expand=True)

    main_label = tk.Label(main_frame)
    main_label.pack(side="top", fill="both", expand=True)

    title_label_main = tk.Label(main_frame, text="原画")
    title_label_main.pack(side="top")

    # 创建并布置包含底部图像及其标题的框架
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(side="bottom", fill="both", expand=True)

    image_labels = [main_label]  # 包含所有图像标签的列表，开始时添加主图像标签
    title_labels = [title_label_main]  # 包含所有标题标签的列表，开始时添加主图像的标题

    # 创建第一个图像和标题
    frame1 = tk.Frame(bottom_frame)
    frame1.pack(side="left", fill="both", expand=True)
    label1 = tk.Label(frame1)
    label1.pack(side="top", fill="both", expand=True)
    title_label1 = tk.Label(frame1, text="anime")
    title_label1.pack(side="top")
    image_labels.append(label1)
    title_labels.append(title_label1)

    # 创建第二个图像和标题
    frame2 = tk.Frame(bottom_frame)
    frame2.pack(side="left", fill="both", expand=True)
    label2 = tk.Label(frame2)
    label2.pack(side="top", fill="both", expand=True)
    title_label2 = tk.Label(frame2, text=title_texts[2])
    title_label2.pack(side="top")
    image_labels.append(label2)
    title_labels.append(title_label2)

    # 创建第三个图像和标题
    frame3 = tk.Frame(bottom_frame)
    frame3.pack(side="left", fill="both", expand=True)
    label3 = tk.Label(frame3)
    label3.pack(side="top", fill="both", expand=True)
    title_label3 = tk.Label(frame3, text=title_texts[3])
    title_label3.pack(side="top")
    image_labels.append(label3)
    title_labels.append(title_label3)

    # 创建第四个图像和标题
    frame4 = tk.Frame(bottom_frame)
    frame4.pack(side="left", fill="both", expand=True)
    label4 = tk.Label(frame4)
    label4.pack(side="top", fill="both", expand=True)
    title_label4 = tk.Label(frame4, text=title_texts[4])
    title_label4.pack(side="top")
    image_labels.append(label4)
    title_labels.append(title_label4)

    show_frame()  # 开始显示图像
    window.mainloop()  # 进入主事件循环


create_window()
