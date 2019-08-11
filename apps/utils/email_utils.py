from apps.users.models import EmailVerifyRecord
from onlineedu.settings import EMAIL_FROM
from django.core.mail import send_mail

import random
from datetime import datetime


def generate_random_str(length = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    for i in range(length):
        str += chars[random.randint(0, len(chars)-1)]
    return str

def send_register_email(email, send_type='register'):
    """
    发送注册邮件
    :param email: 接收方邮箱地址
    :param send_type: 类型
    :return:
    """
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code = code
    email_record.send_type = send_type
    email_record.email = email
    email_record.send_time = datetime.now()
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = "注册在线激活链接"
        email_body = "请点击此链接进行激活 http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass

    elif send_type == 'forget':
        email_title = "修改密码链接"
        email_body = "请点击此链接进行修改密码 http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass