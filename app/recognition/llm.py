from volcenginesdkarkruntime import Ark
from fastapi import Depends
import os
import json


def get_ark_client():
    return Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=os.environ.get("ARK_API_KEY"),
    )


PROMPT_2 = '''请严格按照 JSON 格式返回检测结果，禁止任何换行或格式化处理。判断场景中是否存在暴力行为并返回**英文**结果：{"is_violence": (true if violence exist, else false),"category":"violence category if violence exist, else empty "}'''


def image2text(frame_url: str, client: Ark) -> str:
    response = client.chat.completions.create(
        model="doubao-vision-lite-32k-241015",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": ""},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": frame_url
                        }
                    },
                ],
            }
        ],
    )
    return (response.choices[0].message.content)


def check_violence(frame_url: str, client: Ark) -> str:
    response = client.chat.completions.create(
        model="doubao-vision-lite-32k-241015",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT_2},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": frame_url
                        }
                    },
                ],
            }
        ],
    )
    return json.loads(response.choices[0].message.content)
