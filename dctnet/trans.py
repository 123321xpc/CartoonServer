# import os
# import cv2
# import numpy as np
# from dctnet.source.cartoonize import Cartoonizer
# from djangoProject.settings import IMG_ROOT, VEDIO_ROOT
# from run import get_model_list
#
# list_models = get_model_list("models")
#
# type_map = {
#     '3d': 0,
#     'artstyle': 1,
#     'handdrawn': 2,
#     'sketch': 3,
#     'anime': 4
# }
#
# algo_3d = Cartoonizer(list_models[0])
# algo_artstyle = Cartoonizer(list_models[1])
# algo_handdrawn = Cartoonizer(list_models[2])
# algo_sketch = Cartoonizer(list_models[3])
# algo_anime = Cartoonizer(list_models[4])
#
# algos = {
#     0: algo_3d,
#     1: algo_artstyle,
#     2: algo_handdrawn,
#     3: algo_sketch,
#     4: algo_anime
# }
#
#
# def trans_img(file_name, type):
#     path = os.path.join(IMG_ROOT, file_name)
#     img = cv2.imread(path)[..., ::-1]
#
#     # result = algos[type_map[type]].cartoonize(img)
#     result = algos[3].cartoonize(img)
#     result_out = np.array(result, dtype=np.uint8)
#
#     result_out = np.array(result, dtype=np.uint8)
#
#     input_img = cv2.imread(path)
#     height, width = input_img.shape[:2]
#
#     result_out = cv2.resize(result_out, (width, height))
#     file_name = type + '_' + file_name
#
#     file_img_out = os.path.join(os.path.join(IMG_ROOT, file_name))  # 输出文件路径
#     print("output:" + file_img_out)
#     cv2.imwrite(file_img_out, result_out)
#
#     return file_img_out
#
# if __name__ == '__main__':
#     trans_img(os.path.join(IMG_ROOT, "hjp.jpg"), 'sketch')