import sys
sys.path.append('..')

from django.http import JsonResponse
from emoji import emojize

from database_new import User, DATABASE
from uuid_token import forge_token, get_uuid_from_token
from email_sender import EmailSender
from controller import CONTROLLER


def sign_up(request):
    """用户注册请求处理函数

    url: 42.192.44.52:8000/sign_up/

    构造用户对象并写入数据库，以json形式向前端返回token
    """
    # 解包前端请求
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        email = request.GET.get('email')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

    if CONTROLLER.emoji_status is True:
        print(emojize(':white_check_mark: 已收到 sign_up 请求', language='alias'))
        print(emojize(':snake: username: ' + username, language='alias'))
        print(emojize(':key: password(已加密): ' + password, language='alias'))
        print(emojize(':envelope: email: ' + email, language='alias'))

    # 判断邮箱是否已被占用
    if email in DATABASE.email_list:  # 邮箱已被占用
        json_rsp = {
            "message_type": "rsp_sign_up",
            "token": 'None',
            "result": "email_occupied"
        }
    else:  # 邮箱可用
        # 生成验证码
        email_sender = EmailSender(email, username)
        email_sender.generate_content()
        # 发送验证邮件
        # email_sender.send()
        # 构造用户对象
        new_user = User(username=username, password=password, email=email, confirm_code=email_sender.confirm_code)
        # 将用户对象添加至数据库
        DATABASE.add_user(new_user)
        # 构造json
        new_token = forge_token(new_user.uuid)
        json_rsp = {
            "message_type": "rsp_sign_up",
            "token": new_token,
            "result": "success"
        }
    if CONTROLLER.emoji_status is True:
        print(emojize(':rocket: 已发送 rsp_sign_up 应答', language='alias'))
        print(json_rsp)

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache


def email_confirm(request):
    """新用户邮箱验证请求处理函数

    url: 42.192.44.52:8000/sign_up/email_confirm/

    将用户输入的验证码与数据库中的值进行比对，并以json形式向前端返回验证结果
    """
    # 解包前端请求
    if request.method == 'GET':
        token = request.GET.get('token')
        input_confirm_code = request.GET.get('confirm_code')
    if request.method == 'POST':
        token = request.POST.get('token')
        input_confirm_code = request.POST.get('confirm_code')

    if CONTROLLER.emoji_status is True:
        print(emojize(':white_check_mark: 已收到 email_confirm 请求', language='alias'))
        print(emojize(':snake: token: ' + token, language='alias'))
        print(emojize(':key: confirm_code: ' + input_confirm_code, language='alias'))

    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
    else:
        uuid = int(uuid_str)
        user = DATABASE.get_user(uuid)
        new_token = forge_token(uuid_str)
        # 比对验证码
        if input_confirm_code == user.confirm_code:
            json_rsp = {
                "message_type": "rsp_email_confirm",
                "token": new_token,
                "confirmed": True
            }
        else:
            json_rsp = {
                "message_type": "rsp_email_confirm",
                "token": new_token,
                "confirmed": False
            }

    if CONTROLLER.emoji_status is True:
        print(emojize(':rocket: 已发送 rsp_email_confirm 应答', language='alias'))
        print(json_rsp)

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache
