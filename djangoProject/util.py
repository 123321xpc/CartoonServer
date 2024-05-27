import json
import io
import base64

class Result:
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    def to_json(self):
        return json.dumps({"code": self.code, "msg": self.msg, "data": self.data})

class Base64:
    def __init__(self, name, data, type):
        self.name = name
        self.data = data
        self.type = type

    def to_json(self):
        return json.dumps({"name": self.name, "data": self.data, "type": self.type})



def create_blob_from_file(file_path):
    # 将文件整合成一个Blob对象
    with open(file_path, 'rb') as file:
        file_data = file.read()

    blob = io.BytesIO(file_data)
    encoded_blob = base64.b64encode(blob.getvalue()).decode('utf-8')
    return encoded_blob

