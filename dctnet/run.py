import os

import cv2
import numpy as np

from dctnet.source.cartoonize import Cartoonizer


def get_model_list(model_dir):
    list_models = []
    m_dirs = os.listdir(model_dir)
    for dir in m_dirs:
        path_model = os.path.join(model_dir, dir)
        list_models.append(path_model)
    return list_models


if __name__ == '__main__':


    file_img = "hjp.jpg"
    i = 3

    list_models = get_model_list("models")
    algo = Cartoonizer(list_models[i])

    img = cv2.imread(file_img)[..., ::-1]
    result = algo.cartoonize(img)
    result_out = np.array(result, dtype=np.uint8)

    input_img = cv2.imread(file_img)
    height, width = input_img.shape[:2]

    result_out = cv2.resize(result_out, (width, height))

    cv2.namedWindow("out", cv2.WINDOW_NORMAL or cv2.WINDOW_KEEPRATIO or cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(file_img, cv2.imread(file_img))
    cv2.imshow("out", result_out)
    cv2.waitKey(0)

    file_img_out = os.path.split(list_models[i])[-1] + "_out_" + file_img  # 输出文件路径
    cv2.imwrite(file_img_out, result_out)  # 输出
