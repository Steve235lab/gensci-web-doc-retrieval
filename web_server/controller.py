# controller.py
# 系统行为控制器
# Written by Steve D. J. on 2022/6/28.


class Controller:
    """系统行为控制器

    该class仅用于创建唯一全局对象 CONTROLLER，用于控制系统的行为

    -test_mode: 测试模式开关
        True: 打开测试模式，会在 search/views.py 的 search 和 get_paper_info 函数中将数据源切换至测试用数据
        False: 关闭测试模式，使用真实的数据源，仅用于生产环境，测试环境下会因为找不到路径而报错
    -emoji_status: 控制台请求应答详情输出开关
        True: 打开请求应答详情输出，推荐在支持 emoji 输出的终端中使用
        False: 关闭请求应答详情输出，控制台只打印Django默认的信息
    -paper_info_data_source: search/views.py 的 get_paper_info 函数数据来源选择器
        excel: 使用excel文件作为数据源，加载速度较慢
        json: 使用json文件作为数据源，加载速度较快
    -clue_info_data_source: search/views.py 的 get_clue_info 函数数据来源选择器
        excel: 使用excel文件作为数据源，加载速度较慢
        json: 使用json文件作为数据源，加载速度较快
    """
    def __init__(self):
        self.test_mode: bool = True
        self.emoji_status: bool = True
        self.paper_info_data_source: str = 'json'
        self.clue_info_data_source: str = 'json'

        # MySQL数据库相关设定
        self.db_host = '42.192.44.52'
        self.db_port = 3306
        self.db_user = 'root'
        self.db_password = 'root'
        self.db_name = 'gensci-web-doc-retrieval-db'
        self.db_charset = 'utf8'

        # 发送邮件相关设定
        self.email_sender = 'xuchixuchixu@foxmail.com'
        self.email_auth_passport = 'idmbeadoeeohbaja'
        self.email_subject = 'gensci-web-doc-retrieval'
        self.smtp_host = 'smtp.qq.com'

        # token过期时间
        self.token_survive_time = 60 * 60 * 24  # 24h
        # token加盐
        self.token_salt = 'Steve235Lab'
        # token密钥
        self.token_key = 'django-insecure-aae68)ppyyk0y=-4of$%^d96-h48fxqcry2!g@j1g0ns6=zapa'


CONTROLLER = Controller()
