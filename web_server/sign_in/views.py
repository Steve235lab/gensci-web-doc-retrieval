import sys

sys.path.append('..')

from emoji import emojize
from django.http import JsonResponse

from database_new import DATABASE
from uuid_token import forge_token
from controller import CONTROLLER
from email_sender import EmailSender


def sign_in(request):
    """用户登录请求处理函数

    url: 42.192.44.52:8000/sign_in/

    登录信息验证，并向前端返回结果
    """
    # 解包前端请求
    if request.method == 'GET':
        email = request.GET.get('email')
        input_password = request.GET.get('password')
        # print(request.GET)
    if request.method == 'POST':
        email = request.POST.get('email')
        input_password = request.POST.get('password')

    if CONTROLLER.emoji_status is True:
        print(emojize(':white_check_mark: 已收到 sign_in 请求', language='alias'))
        print(emojize(':envelope: email: ' + email, language='alias'))
        print(emojize(':key: password(已加密): ' + input_password, language='alias'))

    # 判断用户是否已注册
    if email not in DATABASE.email_list:  # 用户未注册
        json_rsp = {
            "message_type": "rsp_sign_in",
            "token": 'None',
            "result": "unregistered_user"
        }
    else:
        # 验证密码正误
        uuid = DATABASE.user_index[email]
        user = DATABASE.get_user(uuid)
        username = user.username
        if input_password == user.password:  # 密码正确
            # 生成token
            new_token = forge_token(uuid)
            json_rsp = {
                "message_type": "rsp_sign_in",
                "token": new_token,
                "result": "success",
                "username": username
            }
            # json_rsp["Access-Control-Allow-Origin"] = "*"
        else:  # 密码错误
            json_rsp = {
                "message_type": "rsp_sign_in",
                "token": 'None',
                "result": "wrong_password"
            }

    if CONTROLLER.emoji_status is True:
        print(emojize(':rocket: 已发送 rsp_sign_in 应答', language='alias'))
        print(json_rsp)

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache


def email_confirm(request):
    """修改密码时验证用户输入的邮箱是否已注册

    url: 42.192.44.52:8000/sign_in/email_confirm/
    """
    # 解包前端请求
    if request.method == 'GET':
        email = request.GET.get('email')
    if request.method == 'POST':
        email = request.POST.get('email')

    # 判断用户是否已注册
    if email not in DATABASE.email_list:  # 用户未注册
        json_rsp = {
            "message_type": "rsp_email_confirm",
            "result": "email_noexist"
        }
    else:
        json_rsp = {
            "message_type": "rsp_email_confirm",
            "result": "success"
        }
        # 使用邮箱获取用户名
        uuid = DATABASE.user_index[email]
        user = DATABASE.get_user(uuid)
        username = user.username
        # 发送验证邮件
        email_sender = EmailSender(email, username)
        email_sender.generate_reset_password_content()
        email_sender.send()

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache


def reset_password(request):
    """修改密码请求处理函数

    url: 42.192.44.52:8000/sign_in/reset_password/
    """
    # 解包前端请求
    if request.method == 'GET':
        confirm_code = request.GET.get('code')
        new_password = request.GET.get('password')
        email = request.GET.get('email')
    if request.method == 'POST':
        confirm_code = request.POST.get('code')
        new_password = request.POST.get('password')
        email = request.POST.get('email')

    # 使用邮箱获取uuid
    uuid = DATABASE.user_index[email]
    user = DATABASE.get_user(uuid)
    # 比对验证码
    if confirm_code == user.confirm_code:
        json_rsp = {
            "message_type": "rsp_email_confirm",
            "result": "success"
        }
        user.password = new_password
        DATABASE.rewrite_user(user)
    else:
        json_rsp = {
            "message_type": "rsp_email_confirm",
            "result": "False"
        }

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache


