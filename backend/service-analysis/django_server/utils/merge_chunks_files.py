# import os
from ..apps.analysis.models import *
# 分片上传文件导入相关模块
from django.core.files.storage import FileSystemStorage
from .. import settings

chunked_storage = FileSystemStorage(location=settings.ANALYSE_BASE_DIR)


def merge_chunks(upload_id, data_type, filename, storage):
    base_path = os.path.join(storage.base_location, upload_id, data_type, 'fastqs')

    # 动态获取文件名
    chunks = ChunkedUpload.objects.filter(upload_id=upload_id, data_type=data_type, filename=filename).order_by(
        'chunk_number')
    if not chunks.exists():
        raise ValueError("No chunks found for merging")

    final_file_name = filename
    final_file_path = os.path.join(base_path, final_file_name)

    # 确保目录存在
    os.makedirs(base_path, exist_ok=True)
    # 合并文件
    with open(final_file_path, 'wb') as final_file:
        for chunk in chunks:
            with open(chunk.file.path, 'rb') as chunk_file:
                final_file.write(chunk_file.read())

    # 可选：删除分片文件
    for chunk in chunks:
        os.remove(chunk.file.path)

    return final_file_path
