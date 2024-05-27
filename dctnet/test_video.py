import os

import cv2
import numpy as np
from moviepy.editor import VideoFileClip

from dctnet.source.cartoonize import Cartoonizer


def get_model_list(model_dir):
    list_models = []
    m_dirs = os.listdir(model_dir)
    for dir in m_dirs:
        path_model = os.path.join(model_dir,dir)
        list_models.append(path_model)
    return list_models

def add_audio(src_video_path, dest_video_path, output_video_path):
    """
    添加音频到视频
    :param src_video_path: 原视频路径
    :param dest_video_path: 目标视频路径（无音频）
    :param output_video_path: 输出视频路径（有音频）
    :return:
    """
    src_video = VideoFileClip(src_video_path)
    dest_video = VideoFileClip(dest_video_path)
    dest_video = dest_video.set_audio(src_video.audio)
    dest_video.write_videofile(output_video_path, codec='libx264')
    src_video.close()
    dest_video.close()

if __name__ == '__main__':
    file_img = "hhh.mp4"

    i=3

    list_models = get_model_list("models")
    algo =Cartoonizer(list_models[i])

    cap = cv2.VideoCapture(file_img)
    frame_count=0
    frame_skip=1

    # 获取视频的宽度、高度和FPS
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 创建一个VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用mp4编码
    out = cv2.VideoWriter('output_no_audio.mp4', fourcc, fps, (width, height))

    while True:
        success,img = cap.read()
        if  success:
            if frame_count % frame_skip == 0:  # Only process every nth frame
                result = algo.cartoonize(img[..., ::-1])
                result_out = np.array(result, dtype=np.uint8)
                out.write(result_out)  # 将处理后的帧写入VideoWriter
                cv2.imshow('video', result_out)
            frame_count += 1
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放VideoCapture和VideoWriter
    cap.release()
    out.release()

    # 添加音频到视频
    add_audio(file_img, 'output_no_audio.mp4', 'output_with_audio.mp4')
