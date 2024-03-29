# database.py
# 已弃用，请使用 database_new.py
# 内存中数据对象与硬盘中数据库表文件交互
# Written by Steve D. J. on 2022/6/17.

import json

from pymysql import connect

# DATABASE对象中user_list成员的最大长度
USER_LIST_MAX_LENGTH = 1024


class Database:
    """内存中的数据对象集合，外部数据库交互接口

    该class仅用于创建唯一全局对象DATABASE，以方便系统其他部分访问数据，定义数据对象的保存与加载操作

    数据成员：
        -user_list: (list) 保存在内存中的用户对象集合，可以限制最大长度为 USER_LIST_MAX_LENGTH：向尾部添加元素，从头部删除元素
        -all_uuids: (list) 包含所有已被分配的uuid

    方法成员：
        -write_user: 将User对象拆分为基本数据元，然后写入数据库
        -add_user: 将新注册的User对象放入user_list，然后write_user
        -get_user: 使用uuid先在user_list中查找，找到后返回User对象；如果找不到再到数据库中查找，找到后使用数据库中的数据初始化User对象，返
        回该User对象，然后将该User对象放入user_list尾部，并删除user_list头部元素
        -rewrite_user: 覆盖写入更改后的User对象以起到修改数据库中数据的效果
        -remove_user: 根据uuid删除用户，实际将指定uuid的用户在数据库中的removed标签置为Ture
    """

    def __init__(self):
        """读取数据库初始化DATABASE对象

        :return: None
        """
        self.user_list = []
        self.all_uuids = []
        # 连接到Docker上的MySQL服务容器，注意要先到Docker里手动运行MySQL
        # TODO: Docker容器中的MySQL服务端口号每次启动会发生改变，这里不应该使用固定值，寻找获取当前正确端口号的方法
        self.conn = connect(host='host.docker.internal', port=49153, user='root', password='mysqlpw',
                            database='gensci-web-doc-retrieval-db', charset='utf8')
        self.cursor = self.conn.cursor()
        # 使用 web_server_user 表中的数据初始化 self.user_list 和 self.all_uuids
        sql = """select * from web_server_user"""
        self.cursor.execute(sql)
        users = self.cursor.fetchall()

        # 遍历 web_server_user 表中所有的行
        for user in users:
            removed_flag = bool(user[-1])
            if removed_flag is False:
                uuid = user[0]
                if len(self.user_list) < USER_LIST_MAX_LENGTH:  # 控制内存中的用户数量不超出上限
                    username = user[1]
                    password = user[2]
                    email = user[3]
                    search_history = user[4]
                    search_history_json = json.loads(search_history)  # 得到的 search_history_json 是字典
                    favourites = user[5]
                    favourites_json = json.loads(favourites)
                    confirm_code = user[6]
                    email_confirmed = bool(user[7])
                    permissions = user[8]
                    user_in_memory = User(uuid=uuid, username=username, password=password, email=email,
                                          search_history=search_history_json, favourites=favourites_json,
                                          confirm_code=confirm_code, email_confirmed=email_confirmed,
                                          permissions=permissions)
                    self.user_list.append(user_in_memory)

                self.all_uuids.append(uuid)

    def write_user(self, user):
        """将User对象拆分为基本数据元，然后写入数据库

        :param user: (User object) 待写入的User对象
        :return: None
        """
        # 拆解 user 对象
        uuid = user.uuid
        username = user.username
        password = user.password
        email = user.email
        search_history = json.dumps(user.search_history)  # 得到的 search_history 是字符串
        favourites = json.dumps(user.favourites)
        confirm_code = user.confirm_code
        email_confirmed = str(user.email_confirmed)
        permissions = user.permissions

        # 生成 MySQL 指令并执行插入操作
        sql = """insert into web_server_user values ("%d","%s","%s","%s","%s","%s","%s","%s","%s", "%s")""" % (
            uuid, username, password, email, search_history, favourites, confirm_code, email_confirmed, permissions,
            "False")
        self.cursor.execute(sql)
        self.conn.commit()

    def add_user(self, user):
        """将新注册的User对象放入user_list，然后write_user

        :param user: (User object) 新注册的用户对象
        :return: None
        """
        self.user_list.append(user)
        self.all_uuids.append(user.uuid)
        self.write_user(user)

        # 控制 user_list 中的对象数量
        while len(self.user_list) > USER_LIST_MAX_LENGTH:
            self.user_list.pop(0)

    def get_user(self, uuid):
        """使用uuid查找用户对象

        用uuid先在user_list中查找，找到后返回User对象；如果找不到再到数据库中查找，找到后使用数据库中的数据初始化User对象，返回该User对象，然
        后将该User对象放入user_list尾部，并删除user_list头部元素

        :param uuid: (int) 用户编号
        :return: (User object) 找到的用户对象
        """
        if uuid not in self.all_uuids:  # 用户不存在
            return 'user not found'
        else:
            found_flag = False
            # 先在内存中查找
            for index in range(len(self.user_list)):
                if self.user_list[index].uuid == uuid:
                    found_flag = True
                    found_user = self.user_list[index]
                    # 将被找到的用户对象移至表尾
                    self.user_list.append(found_user)
                    self.user_list.pop(index)
                    return found_user

            # 到数据库中查找
            if found_flag is False:
                sql = """select * from web_server_user where uuid = "%d" """ % uuid
                self.cursor.execute(sql)
                user = self.cursor.fetchall()
                username = user[1]
                password = user[2]
                email = user[3]
                search_history = user[4]
                search_history_json = json.loads(search_history)
                favourites = user[5]
                favourites_json = json.loads(favourites)
                confirm_code = user[6]
                email_confirmed = bool(user[7])
                permissions = user[8]
                found_user = User(uuid=uuid, username=username, password=password, email=email,
                                  search_history=search_history_json, favourites=favourites_json,
                                  confirm_code=confirm_code, email_confirmed=email_confirmed,
                                  permissions=permissions)
                self.user_list.append(found_user)

                # 控制 user_list 中的对象数量
                while len(self.user_list) > USER_LIST_MAX_LENGTH:
                    self.user_list.pop(0)

                return found_user

    def rewrite_user(self, changed_user):
        """覆盖写入更改后的User对象以起到修改数据库中数据的效果

        先到user_list中查找替换掉具有相同uuid的对象（如有），然后覆盖写入到数据库中

        :param changed_user: (User object) 更改后的用户对象
        :return: None
        """
        uuid = changed_user.uuid
        if uuid not in self.all_uuids:  # 用户不存在
            pass
        else:
            # 先在内存中更改
            for index in range(len(self.user_list)):
                if self.user_list[index].uuid == uuid:
                    self.user_list.append(changed_user)
                    self.user_list.pop(index)
                    break

            # 覆盖写入到数据库中
            sql = """update web_server_user set uuid = ('%d'),username = ('%s'), password = ('%s'), email = ('%s'), search_history = ('%s'), favourites = ('%s'), confirm_code = ('%s'), email_confirmed = ('%s'), permissions = ('%s') where uuid = ('%d') """ % (
                uuid, changed_user.username, changed_user.password, changed_user.email, changed_user.search_history,
                changed_user.favourites, changed_user.confirm_code, changed_user.email_confirmed,
                changed_user.permissions,
                uuid)
            self.cursor.execute(sql)
            self.conn.commit()

    def remove_user(self, uuid):
        """ 根据uuid删除用户

        先在user_list中删除，然后将指定uuid的用户在数据库中的removed标签置为Ture

        :param uuid: (int) 用户编号
        :return: None
        """
        if uuid not in self.all_uuids:  # 用户不存在
            pass
        else:
            # 先在内存中删除
            self.all_uuids.remove(uuid)
            for index in range(len(self.user_list)):
                if self.user_list[index].uuid == uuid:
                    self.user_list.pop(index)
                    break

            # 将指定uuid的用户在数据库中的removed标签置为Ture
            sql = """update web_server_user set removed = "Ture" where uuid = ('%d')""" % uuid
            self.cursor.execute(sql)
            self.conn.commit()


class User:
    """用户信息数据类

    用于创建包含用户信息的用户对象，详细文档见 ../docs/用户信息数据类设计.md

    class User 原位于 user_info.py 因为其中包含对 DATABASE 的操作，交叉调用存在问题，故移动至该文件下

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
        if uuid is None:  # 未传入uuid，执行注册新用户操作，使用默认值初始化对象
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
        else:  # 传入了uuid，执行加载数据操作，使用已保存的数据初始化对象
            self.uuid = uuid
            self.username = username
            self.password = password
            self.email = email
            self.search_history = kwargs['search_history']
            self.favourites = kwargs['favourites']
            self.confirm_code = kwargs['confirm_code']
            self.email_confirmed = kwargs['email_confirmed']
            self.permissions = kwargs['permissions']

    def print_user_info(self):
        """打印用户对象的各数据成员"""
        print("uuid: ", self.uuid)
        print("username: ", self.username)
        print("password: ", self.password)
        print("email: ", self.email)
        print("search_history: ")


# 唯一全局对象
DATABASE = Database()

if __name__ == "__main__":
    # test
    # 读数据库
    # cache = DATABASE.user_list[0].search_history
    # json_test = json.dumps(cache)
    # print(json_test)

    # 写数据库
    # test_user = User(username='田所浩二', password='114514', email='test@test.com')
    # DATABASE.write_user(test_user)

    # 添加用户
    test_user = User(username='野兽先辈', password='114514', email='test@test.com')
    DATABASE.add_user(test_user)

    for user in DATABASE.user_list:
        pass
