import os
from django.conf import settings
from django.http import JsonResponse
from djangoProject.util import *
from djangoProject import trans_img, type_map
import threading
import queue



def process_file(uploaded_file_name, type, result_queue):
    file_out_path = trans_img(uploaded_file_name, type)
    imgs = create_blob_from_file(file_out_path)
    result_queue.put(Base64(type + '_' + uploaded_file_name, imgs, type).to_json())


def upload_imgs(request):

    try:
        type = request.POST.get('type')
        result_queue = queue.Queue()
        threads = []

        if type is not None:
            # 接收文件数据
            uploaded_files = request.FILES.getlist('file')
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(settings.IMG_ROOT, uploaded_file.name)

                    with open(file_path, 'wb') as fp:
                        for chunk in uploaded_file.chunks():
                            fp.write(chunk)

                    # 创建一个线程来处理文件
                    t = threading.Thread(target=process_file, args=(uploaded_file.name, type, result_queue))
                    threads.append(t)
                    t.start()

                # 等待所有线程执行完成
                for t in threads:
                    t.join()

                # 从队列中获取结果
                results = []
                while not result_queue.empty():
                    results.append(result_queue.get())
        else:
            # 接收文件数据
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                file_path = os.path.join(settings.IMG_ROOT, uploaded_file.name)
                with open(file_path, 'wb') as fp:
                    for chunk in uploaded_file.chunks():
                        fp.write(chunk)

                # 创建线程来处理文件
                for type in ['3d', 'sketch', 'handdrawn', 'anime', 'artstyle']:
                    t = threading.Thread(target=process_file, args=(uploaded_file.name, type, result_queue))
                    threads.append(t)
                    t.start()

                # 等待所有线程执行完成
                for t in threads:
                    t.join()

                # 从队列中获取结果
                results = []
                results.append(Base64('origin' + uploaded_file.name, create_blob_from_file(file_path), 'origin').to_json())
                while not result_queue.empty():
                    results.append(result_queue.get())

            # 处理成功，返回成功信息及文件信息
        result = Result(200, "转化成功！", results)  # 这里的 results 包含每个线程的处理结果
        return JsonResponse(result.to_json(), safe=False)

    except Exception as e:
        print(e)
        result = Result(400, "请求失败，请重试！", None)
        return JsonResponse(result.to_json(), safe=False, status=400)


