# uuid_token.py
# token生成与解析
# Written by Steve D. J. on 2022/6/17.

import time
import jwt


KEY = 'django-insecure-aae68)ppyyk0y=-4of$%^d96-h48fxqcry2!g@j1g0ns6=zapa'
SALT = 'Steve235Lab'
TIME_OUT = 60 * 30  # 30min


def forge_token(uuid):
    """生成token

    token的生命周期由 TIME_OUT 决定

    :param uuid: (str) 用户的uuid，用于查找用户对象
    :return: (str) 发往客户端的token，示例：eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiMDAxIiwiZXhwIjoxNjU1NDUzMzg2LjEyODI2LCJzYWx0IjoiU3RldmUyMzVMYWIifQ.vLmc5nNmJc4xBN83CMneKEYG2GmIDan-p_fP91n7WTE
    """
    payload = {
        "uuid": str(uuid),
        'exp': time.time() + TIME_OUT,
        'salt': SALT
    }
    return jwt.encode(payload, KEY, algorithm="HS256")


def get_uuid_from_token(token):
    """从token中获取uuid

    当token在有效期内时返回uuid，否则返回 "token expired"

    :param token: (str) 客户端消息中附带的token
    :return: (str) uuid or "token expired"
    """
    try:
        uuid = jwt.decode(token, KEY, algorithms=["HS256"])['uuid']
        return uuid
    except jwt.ExpiredSignatureError:
        return "token expired"


if __name__ == "__main__":
    token = forge_token('001')
    print(token)
    uuid = get_uuid_from_token(token)
    print(uuid)
