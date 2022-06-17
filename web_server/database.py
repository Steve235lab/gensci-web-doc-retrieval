# database.py
# 内存中数据对象与硬盘中数据库表文件交互
# Written by Steve D. J. on 2022/6/17.


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

    def write_user(self, user):
        """将User对象拆分为基本数据元，然后写入数据库

        :param user: (User object) 待写入的User对象
        :return: None
        """
        pass

    def add_user(self, user):
        """将新注册的User对象放入user_list，然后write_user

        :param user: (User object) 新注册的用户对象
        :return: None
        """
        pass

    def get_user(self, uuid):
        """使用uuid查找用户对象

        用uuid先在user_list中查找，找到后返回User对象；如果找不到再到数据库中查找，找到后使用数据库中的数据初始化User对象，返回该User对象，然
        后将该User对象放入user_list尾部，并删除user_list头部元素

        :param uuid: (str) 用户编号
        :return: (User object) 找到的用户对象
        """
        pass

    def rewrite_user(self, changed_user):
        """覆盖写入更改后的User对象以起到修改数据库中数据的效果

        先到user_list中查找替换掉具有相同uuid的对象（如有），然后覆盖写入到数据库中

        :param changed_user: (User object) 更改后的用户对象
        :return: None
        """
        pass

    def remove_user(self, uuid):
        """ 根据uuid删除用户

        将指定uuid的用户在数据库中的removed标签置为Ture

        :param uuid: (str) 用户编号
        :return: None
        """
        pass


# 唯一全局对象
DATABASE = Database()
