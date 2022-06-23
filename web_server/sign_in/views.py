import sys
sys.path.append('..')

from django.http import JsonResponse

from database_new import DATABASE
from uuid_token import forge_token


def sign_in(request):
    """用户登录请求处理函数

    url: 42.192.44.52:8000/sign_in/

    登录信息验证，并向前端返回结果
    """
    # 解包前端请求
    email = request.GET.get('email')
    input_password = request.GET.get('password')
    print(request.GET)

    # 判断用户是否已注册
    if email not in DATABASE.email_list:    # 用户未注册
        json_rsp = {
            "message_type": "rsp_sign_in",
            "token": 'None',
            "result": "unregistered_user"
        }
        cache = JsonResponse(json_rsp)
        cache["Access-Control-Allow-Origin"] = "*"
        return cache
    else:
        # 验证密码正误
        uuid = DATABASE.user_index[email]
        user = DATABASE.get_user(uuid)
        if input_password == user.password:     # 密码正确
            # 生成token
            new_token = forge_token(uuid)
            json_rsp = {
                "message_type": "rsp_sign_in",
                "token": new_token,
                "result": "success"
            }
            # json_rsp["Access-Control-Allow-Origin"] = "*"
            print(json_rsp)
            cache = JsonResponse(json_rsp)
            cache["Access-Control-Allow-Origin"] = "*"
            return cache
        else:   # 密码错误
            json_rsp = {
                "message_type": "rsp_sign_in",
                "token": 'None',
                "result": "wrong_password"
            }
            cache = JsonResponse(json_rsp)
            cache["Access-Control-Allow-Origin"] = "*"
            return cache


