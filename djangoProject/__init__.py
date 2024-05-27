import os
import cv2
import numpy as np
from dctnet.source.cartoonize import Cartoonizer
from djangoProject.settings import IMG_ROOT, VEDIO_ROOT
from dctnet.run import get_model_list
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import threading
import wave


type_map = {
    '3d' : 0,
    'artstyle': 1,
    'handdrawn': 2,
    'sketch': 3,
    'anime': 4
}

processed_frames_list = []


list_models = get_model_list("dctnet/models")

def process_frame_and_put_in_queue(img, frame_number, algo):
    result = trans_img_vdo(img, algo)
    processed_frames_list.append((frame_number, result))
    print(str(frame_number) + " processed")






def trans_img_vdo(img, algo):
    result = algo.cartoonize(img)
    return np.array(result, dtype=np.uint8)


def trans_video(file_name, type):
    input_path = os.path.join(VEDIO_ROOT, file_name)
    algo = Cartoonizer(list_models[type_map[type]])
    print("input:" + input_path)
    cap = cv2.VideoCapture(input_path)
    frame_count = 0
    frame_skip = 2
    threads = []

    # 获取视频的宽度、高度和FPS
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 创建一个VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用mp4编码
    no_audio_output_file_path = os.path.join(VEDIO_ROOT, type + '_' + "no_audio" + '_' + file_name)
    output_file_path = os.path.join(VEDIO_ROOT, type + '_' + file_name)
    print("output:" + no_audio_output_file_path)

    out = cv2.VideoWriter(no_audio_output_file_path, fourcc, fps, (width, height))
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获取视频的总帧数
    print("total frames:" + str(total_frames))


    while cap.isOpened():
        success, img = cap.read()
        if success:
            print('frame:' + str(frame_count))
            t = threading.Thread(target=process_frame_and_put_in_queue, args=(img, frame_count, algo))
            t.start()
            threads.append(t)
            frame_count += 1
        else:
            break

    # 等待所有线程处理完成
    for thread in threads:
        thread.join()

    print("finished processing")

    processed_frames_list.sort(key=lambda x: x[0])  # 按帧号排序

    for frame_number, frame in processed_frames_list:
        out.write(frame)
        print('写入frame:' + str(frame_number))

    cap.release()
    out.release()

    add_audio(input_path, no_audio_output_file_path, output_file_path)

    return output_file_path

def add_audio(src_video_path, dest_video_path, output_video_path):
    """
    添加音频到视频
    :param src_video_path: 原视频路径
    :param dest_video_path: 目标视频路径（无音频）
    :param output_video_path: 输出视频路径（有音频）
    :return:
    """
    print('src_video_path:' + src_video_path)
    print('dest_video_path:' + dest_video_path)
    print('output_video_path:' + output_video_path)

    src_video = VideoFileClip(src_video_path)
    dest_video = VideoFileClip(dest_video_path)
    dest_video = dest_video.set_audio(src_video.audio)
    dest_video.write_videofile(output_video_path, codec='libx264')
    src_video.close()
    dest_video.close()

def trans_img(file_name, type):

    path = os.path.join(IMG_ROOT, file_name)
    img = cv2.imread(path)[..., ::-1]

    algo = Cartoonizer(list_models[type_map[type]])
    result = algo.cartoonize(img)

    result_out = np.array(result, dtype=np.uint8)


    file_name = type + '_' + file_name

    file_img_out = os.path.join(os.path.join(IMG_ROOT,file_name))  # 输出文件路径
    print("output:" + file_img_out)
    cv2.imwrite(file_img_out, result_out)

    return file_img_out