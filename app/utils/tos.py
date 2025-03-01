import os
import tos
from tos import HttpMethodType
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 从环境变量获取 AK/SK/APIKEY信息
ak = os.getenv('VOLC_ACCESSKEY')
sk = os.getenv('VOLC_SECRETKEY')
api_key = os.getenv('ARK_API_KEY')


ENDPOINT = 'tos-ap-southeast-1.volces.com'
REGION = 'southeast-johor'
BUCKET_NAME = 'content-moderation'


def upload_frames(uid: str, file_list: list) -> dict:
    '''Upload frame images to TOS and return a dict from frame name to url'''
    name_url = {}
    for f in file_list:
        file = Path(f)
        url = upload_tos(f, ENDPOINT, REGION, BUCKET_NAME,
                         f"process/{uid}_{file.name}")
        name_url[file.stem] = url

    return name_url


def upload_tos(filename, tos_endpoint, tos_region, tos_bucket_name, tos_object_key):
    # 创建 TosClientV2 对象，对桶和对象的操作都通过 TosClientV2 实现
    tos_client, inner_tos_client = tos.TosClientV2(ak, sk, tos_endpoint, tos_region), tos.TosClientV2(ak, sk,
                                                                                                      tos_endpoint,
                                                                                                      tos_region)
    try:
        # 将本地文件上传到目标桶中, filename为本地压缩后图片的完整路径
        tos_client.put_object_from_file(
            tos_bucket_name, tos_object_key, filename)
        # 获取上传后预签名的 url
        return inner_tos_client.pre_signed_url(HttpMethodType.Http_Method_Get, tos_bucket_name, tos_object_key).signed_url
    except Exception as e:
        if isinstance(e, tos.exceptions.TosClientError):
            # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
            print('fail with client error, message:{}, cause: {}'.format(
                e.message, e.cause))
        elif isinstance(e, tos.exceptions.TosServerError):
            # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
            print('fail with server error, code: {}'.format(e.code))
            # request id 可定位具体问题，强烈建议日志中保存
            print('error with request id: {}'.format(e.request_id))
            print('error with message: {}'.format(e.message))
            print('error with http code: {}'.format(e.status_code))
        else:
            print('fail with unknown error: {}'.format(e))
        raise e

    # pre_signed_url_output = upload_tos(compressed_file, endpoint, region, bucket_name, object_key)
    # print("Pre-signed TOS URL: {}".format(pre_signed_url_output.signed_url))
