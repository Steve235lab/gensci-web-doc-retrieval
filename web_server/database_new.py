# database_new.py
# 内存中数据对象与硬盘中数据库表文件交互
# Based on database.py
# Written by Steve D. J. on 2022/6/22.

import time

from pymysql import connect
from pymysql.converters import escape_string

# DATABASE对象中user_list成员的最大长度
USER_LIST_MAX_LENGTH = 1024


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
            self.confirm_code = kwargs['confirm_code']
            self.email_confirmed = False
            self.permissions = 'all'  # 后续完善权限系统后再做更改
        else:  # 传入了uuid，执行加载数据操作，使用已保存的数据初始化对象
            self.uuid = uuid
            self.username = username
            self.password = password
            self.email = email
            self.search_history = kwargs['search_history']
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


class Database:
    """内存中的数据对象集合，外部数据库交互接口

    该class仅用于创建唯一全局对象DATABASE，以方便系统其他部分访问数据，定义数据对象的保存与加载操作

    数据成员：
        -user_list: (list) 保存在内存中的用户对象集合，可以限制最大长度为 USER_LIST_MAX_LENGTH：向尾部添加元素，从头部删除元素
        -all_uuids: (list) 包含所有已被分配的uuid
        -email_list: (list) 包含所有用户的注册邮箱
        -user_index: (dict) 将用户中两个具有唯一性的可做标识的成员email和uuid放在字典中，便于查找
            {email: uuid}
        -searched_keywords: (dict) 以被搜索过的关键词为键，[result_timestamp, favourite_flag]为值的字典，方便归并重复关键词搜索
            其中 favourite_flag 初始为 False，当有任意用户收藏此关键词后置为True
            {keywords: [result_timestamp, favourite_flag]}

    方法成员：
        -write_user: 将User对象拆分为基本数据元，然后写入数据库
        -add_user: 将新注册的User对象放入user_list，然后write_user
        -get_user: 使用uuid先在user_list中查找，找到后返回User对象；如果找不到再到数据库中查找，找到后使用数据库中的数据初始化User对象，返
        回该User对象，然后将该User对象放入user_list尾部，并删除user_list头部元素
        -rewrite_user: 覆盖写入更改后的User对象以起到修改数据库中数据的效果
        -remove_user: 根据uuid删除用户，实际将指定uuid的用户在数据库中的removed标签置为True
    """

    def __init__(self):
        """读取数据库初始化DATABASE对象

        :return: None
        """
        self.user_list = []
        self.all_uuids = []
        self.email_list = []
        self.user_index = {}  # {email: uuid}
        self.searched_keywords = {}  # {keywords: [result_timestamp, favourite_flag]}
        # 连接到MySQL服务
        self.conn = connect(host='42.192.44.52', port=3306, user='root', password='root',
                            database='gensci-web-doc-retrieval-db', charset='utf8')
        self.cursor = self.conn.cursor()
        # 使用 User 表和 search_history 表中的数据初始化 self.user_list 和 self.all_uuids
        # 读 User 表
        sql = """select * from user"""
        self.cursor.execute(sql)
        users = self.cursor.fetchall()

        # 遍历 User 表中所有的行
        for user in users:
            removed_flag = user[-1]
            if removed_flag == 'False':
                uuid = user[0]
                email = user[3]
                if len(self.user_list) < USER_LIST_MAX_LENGTH:  # 控制内存中的用户数量不超出上限
                    username = user[1]
                    password = user[2]
                    confirm_code = user[4]
                    email_confirmed = bool(user[5])
                    permissions = user[6]
                    user_in_memory = User(uuid=uuid, username=username, password=password, email=email,
                                          search_history={},
                                          confirm_code=confirm_code, email_confirmed=email_confirmed,
                                          permissions=permissions)
                    self.user_list.append(user_in_memory)

                self.all_uuids.append(uuid)
                self.email_list.append(email)
                self.user_index[email] = uuid

        # 为 self.user_list 中的用户初始化 search_history 成员
        for index in range(len(self.user_list)):
            uuid = self.user_list[index].uuid
            sql = """select * from search_history where uuid = '%d' """ % uuid
            self.cursor.execute(sql)
            histories = self.cursor.fetchall()
            for history in histories:
                timestamp = history[0]
                result_timestamp = history[1]
                keywords = history[2]
                search_completed_flag = history[3]
                uuid = history[4]
                favourite_flag = history[5]
                self.user_list[index].search_history[timestamp] = [result_timestamp, keywords, search_completed_flag,
                                                                   uuid, favourite_flag]

        # 遍历 search_history 表，初始化searched_keywords
        sql = """select * from search_history"""
        self.cursor.execute(sql)
        histories = self.cursor.fetchall()
        for history in histories:
            keywords = history[2]
            if keywords in self.searched_keywords:  # searched_keywords中已经有相同关键词的搜索记录
                favourite_flag = history[5]
                if favourite_flag == 'True':
                    self.searched_keywords[keywords][1] = True
            else:  # 此条记录是第一条搜索该关键词的搜索记录
                result_timestamp = history[1]
                favourite_flag = history[5]
                if favourite_flag == 'True':
                    favourite_flag = True
                else:
                    favourite_flag = False
                self.searched_keywords[keywords] = [result_timestamp, favourite_flag]

    def is_connected(self):
        """数据库连接保活

        每次数据库操作前执行，确保该进程与MySQL数据库的连接处于可用状态，如果检测到连接已断开则执行重连操作
        """
        try:
            self.conn.ping(reconnect=True)
        except:
            self.conn = connect(host='42.192.44.52', port=3306, user='root', password='root',
                                database='gensci-web-doc-retrieval-db', charset='utf8')

    def write_user(self, user: User):
        """将User对象拆分为基本数据元，然后写入数据库

        :param user: (User object) 待写入的User对象
        :return: None
        """
        # 拆解 user 对象
        uuid = user.uuid
        username = user.username
        password = user.password
        email = user.email
        confirm_code = user.confirm_code
        email_confirmed = str(user.email_confirmed)
        permissions = user.permissions

        self.is_connected()
        # 生成 MySQL 指令并执行插入操作
        sql = """insert into user values ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (
            uuid, username, password, email, confirm_code, email_confirmed, permissions, 'False')
        self.cursor.execute(sql)
        self.conn.commit()

    def add_user(self, user: User):
        """将新注册的User对象放入user_list，然后write_user

        :param user: (User object) 新注册的用户对象
        :return: None
        """
        self.user_list.append(user)
        self.all_uuids.append(user.uuid)
        self.email_list.append(user.email)
        self.user_index[user.email] = user.uuid
        self.write_user(user)

        # 控制 user_list 中的对象数量
        while len(self.user_list) > USER_LIST_MAX_LENGTH:
            self.user_list.pop(0)

    def get_user(self, uuid: int):
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
                self.is_connected()
                sql = """select * from user where uuid = '%d' """ % uuid
                self.cursor.execute(sql)
                user = self.cursor.fetchall()
                username = user[1]
                password = user[2]
                email = user[3]
                confirm_code = user[4]
                email_confirmed = bool(user[5])
                permissions = user[6]
                found_user = User(uuid=uuid, username=username, password=password, email=email,
                                  search_history={},
                                  confirm_code=confirm_code, email_confirmed=email_confirmed,
                                  permissions=permissions)

                sql = """select * from search_history where uuid = '%d' """ % uuid
                self.cursor.execute(sql)
                histories = self.cursor.fetchall()
                for history in histories:
                    timestamp = history[0]
                    result_timestamp = history[1]
                    keywords = history[2]
                    search_completed_flag = history[3]
                    uuid = history[4]
                    favourite_flag = history[5]
                    found_user.search_history[timestamp] = [result_timestamp, keywords,
                                                            search_completed_flag,
                                                            uuid, favourite_flag]

                self.user_list.append(found_user)

                # 控制 user_list 中的对象数量
                while len(self.user_list) > USER_LIST_MAX_LENGTH:
                    self.user_list.pop(0)

                return found_user

    def rewrite_user(self, changed_user: User):
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
            self.is_connected()
            sql = """update user set uuid = ('%d'), username = ('%s'), password = ('%s'), email = ('%s'), confirm_code = ('%s'), email_confirmed = ('%s'), permissions = ('%s') where uuid = ('%d') """ % (
                uuid, changed_user.username, changed_user.password, changed_user.email, changed_user.confirm_code,
                changed_user.email_confirmed,
                changed_user.permissions,
                uuid)
            self.cursor.execute(sql)
            self.conn.commit()

    def remove_user(self, uuid: int):
        """ 根据uuid删除用户

        先在user_list中删除，然后将指定uuid的用户在数据库中的removed标签置为True

        :param uuid: (int) 用户编号
        :return: None
        """
        if uuid not in self.all_uuids:  # 用户不存在
            pass
        else:
            # 先在内存中删除
            user = self.get_user(uuid)
            self.email_list.remove(user.email)
            self.all_uuids.remove(uuid)
            self.user_index.pop(user.email)
            for index in range(len(self.user_list)):
                if self.user_list[index].uuid == uuid:
                    self.user_list.pop(index)
                    break

            # 将指定uuid的用户在数据库中的removed标签置为True
            self.is_connected()
            sql = """update user set removed = 'True' where uuid = ('%d')""" % uuid
            self.cursor.execute(sql)
            self.conn.commit()

    def add_search_history(self, keywords: str, uuid: int, raw_keywords: str):
        """向数据库中添加一条新的搜索记录

        生成当前时间戳，查找并更新 self.searched_keywords 确定 result_timestamp，写入数据库

        :param raw_keywords: (str) 用户输入的原始关键词，不包括筛选器
        :param keywords: (str) 用户搜索的关键词组合
        :param uuid: (int) 进行该次搜索的用户序号
        :return: (int) timestamp 该条新历史记录的时间戳
        """
        timestamp: int = int(time.mktime(time.localtime(time.time())))

        if keywords in self.searched_keywords:
            result_timestamp = self.searched_keywords[keywords][0]
        else:
            result_timestamp = timestamp
            self.searched_keywords[keywords] = [timestamp, False]

        self.is_connected()
        sql = """insert into search_history values ('%d', '%d', '%s', '%s', '%d', '%s', '%s')""" % (
            timestamp, result_timestamp, keywords, "False", uuid, "False", raw_keywords)
        self.cursor.execute(sql)
        self.conn.commit()

        return timestamp

    def get_search_history(self, uuid: int):
        """获取给定uuid用户的搜索记录

        :param uuid: 用户的uuid
        :return: history_list 该用户的搜索记录列表
        """
        # 返回记录的最大条数
        max_history_num = 100

        self.is_connected()
        sql = """select * from search_history where uuid = '%d' AND search_completed_flag = 'True' """ % uuid
        self.cursor.execute(sql)
        history_list = self.cursor.fetchall()
        if len(history_list) <= max_history_num:
            return history_list
        else:
            return history_list[(-1*max_history_num):]

    def get_result(self, timestamp: int):
        """获取给定时间戳的历史记录

        :param timestamp: 该次搜索的时间戳
        :return: history 根据给定时间戳从数据表中找到的一条历史记录
        """
        self.is_connected()
        sql = """select * from search_history where timestamp = '%d' """ % timestamp
        self.cursor.execute(sql)
        history = self.cursor.fetchall()

        return history

    def search_completed(self, keywords: str):
        """将数据库中所有搜索该关键词的搜索记录标记为已完成搜索

        :param keywords: (str) 关键词组合
        :return: None
        """
        self.is_connected()
        sql = """update search_history set search_completed_flag = 'True' where keywords = ('%s')""" % keywords
        self.cursor.execute(sql)
        self.conn.commit()

    def get_uuids_with_keywords(self, keywords: str):
        """通过搜索关键词查找发起搜索的用户uuid

        :param keywords:  (str) 关键词组合
        :return: (list) 所有搜索过该关键词组合的用户uuid
        """
        self.is_connected()
        sql = """select uuid from search_history where keywords = ('%s')""" % keywords
        self.cursor.execute(sql)
        uuids = self.cursor.fetchall()

        return uuids

    def add_paper_highlight_abstract(self, pmid: int, highlight_abstract: str):
        """将高亮处理后的文章摘要保存至数据库 paper_abstract 表

        :param pmid: 文章PMID
        :param highlight_abstract: 高亮处理后的文章摘要
        :return: None
        """
        highlight_abstract_escaped = escape_string(highlight_abstract)
        try:
            self.is_connected()
            sql = """insert into paper_abstract values ('%d', '%s')""" % (pmid, highlight_abstract_escaped)
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.is_connected()
            sql = """update paper_abstract set highlight_abstract = ('%s') where pmid = ('%d')""" % (highlight_abstract_escaped, pmid)
            self.cursor.execute(sql)
            self.conn.commit()

    def get_highlight_abstract_with_pmid(self, pmid: int):
        """使用PMID到数据库 paper_abstract 表中查找该文章

        :param pmid: 文章PMID
        :return: highlight_abstract 高亮处理后的文章摘要
        """
        self.is_connected()
        sql = """select * from paper_abstract where pmid = '%d' """ % pmid
        self.cursor.execute(sql)
        highlight_abstract = self.cursor.fetchone()[1]

        return highlight_abstract


# 唯一全局对象
DATABASE = Database()


if __name__ == "__main__":
    # test
    # 读数据库
    # import json
    # cache = DATABASE.user_list[0].search_history
    # json_test = json.dumps(cache)
    # print(json_test)

    # 写数据库
    # test_user = User(username='田所浩二', password='114514', email='test@test.com')
    # DATABASE.write_user(test_user)

    # 添加用户
    # test_user = User(username='野兽先辈', password='114514', email='test@test.com')
    # DATABASE.add_user(test_user)

    # 删除用户
    # DATABASE.remove_user(2)

    for user in DATABASE.user_list:
        print(user.username)
