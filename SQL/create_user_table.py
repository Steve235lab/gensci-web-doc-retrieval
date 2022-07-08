from pymysql import connect
from controller import CONTROLLER

sql = """create table user(uuid int(11)not null, username varchar(64)not null, password varchar(64)not null, email varchar(128)not null, confirm_code varchar(64)not null, email_confirmed varchar(16)not null, permissions varchar(32)not null, removed varchar(16)not null)"""

print(sql)

# 创建数据表
conn = connect(host=CONTROLLER.db_host, port=CONTROLLER.db_port, user=CONTROLLER.db_user,
               password=CONTROLLER.db_password, database=CONTROLLER.db_name, charset=CONTROLLER.db_charset)
cursor = conn.cursor()
cursor.execute(sql)

# 添加管理员用户
sql = """insert into user values ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (0, 'admin', 'password', 'email', 'confirm_code', 1, 'all', 'False')
cursor.execute(sql)
conn.commit()
