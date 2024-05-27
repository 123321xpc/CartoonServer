import os
from django.conf import settings
from django.http import JsonResponse
from djangoProject.util import create_blob_from_file, Base64, Result
from djangoProject import trans_video

# Create your views here.
def upload_vdo(request):


    try:
        type = request.POST.get('type')
        # 接收文件数据
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            file_path = os.path.join(settings.VEDIO_ROOT, uploaded_file.name)
            with open(file_path, 'wb') as fp:
                for chunk in uploaded_file.chunks():
                    fp.write(chunk)

            output_path = trans_video(uploaded_file.name, type)
            video = create_blob_from_file(output_path)
            base64_video = Base64(type + '_' + uploaded_file.name, video, type).to_json()
            print("ok")

        result = Result(200, "请求成功！", base64_video)
        return JsonResponse(result.to_json(), safe=False, status=200)
    except Exception as e:
        print(e)
        result = Result(400, "请求失败，请重试！", None)
        return JsonResponse(result.to_json(), safe=False, status=400)