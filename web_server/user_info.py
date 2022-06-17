# user_info.py
# 用户信息数据类定义
# Written by Steve D. J. on 2022/6/17.

from database import DATABASE


class User:
    """用户信息数据类

    用于创建包含用户信息的用户对象，详细文档见 ../docs/用户信息数据类设计.md

    数据成员：
        -uuid
        -username
        -password
        -email
        -search_history
        -favourites
        -confirm_code
        -email_confirmed
        -permissions
    """
    def __init__(self, username, password, email, uuid=None, **kwargs):
        # 根据uuid的赋值情况执行不同的操作分支
        if uuid is None:    # 未传入uuid，执行注册新用户操作，使用默认值初始化对象
            new_uuid = max(DATABASE.all_uuids) + 1
            self.uuid = new_uuid
            self.username = username
            self.password = password
            self.email = email
            self.search_history = {}
            self.favourites = {}
            self.confirm_code = None
            self.email_confirmed = False
            self.permissions = None
        else:   # 传入了uuid，执行加载数据操作，使用已保存的数据初始化对象
            self.uuid = uuid
            self.username = username
            self.password = password
            self.email = email
            self.search_history = kwargs['search_history']
            self.favourites = kwargs['favourites']
            self.confirm_code = kwargs['confirm_code']
            self.email_confirmed = kwargs['email_confirmed']
            self.permissions = kwargs['permissions']
