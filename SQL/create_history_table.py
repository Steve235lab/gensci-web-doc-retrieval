from pymysql import connect
import json
from controller import CONTROLLER


# 读取集合配置文件
sql = """create table new_search_history(history_id int(11)not null, primary key (history_id), result_path_id int(11)not null, raw_keywords varchar(256)not null, search_completed_flag int(11)not null, uuid int(11)not null, foreign key (uuid) references user(uuid), favourite_flag int(11)not null, start_time varchar(16)not null, end_time varchar(16)not null, filter_article_type varchar(128)not null,"""
set_conf = json.load(open("set_conf.json", 'r'))
for category in set_conf.keys():
    sql += ' ' + category + ' '
    sql += set_conf[category] + 'not null,'

sql = sql[:-1] + ')'
print(sql)

# 创建数据表
conn = connect(host=CONTROLLER.db_host, port=CONTROLLER.db_port, user=CONTROLLER.db_user,
               password=CONTROLLER.db_password, database=CONTROLLER.db_name, charset=CONTROLLER.db_charset)
cursor = conn.cursor()
cursor.execute(sql)

# 添加0号记录
sql = """insert into new_search_history values ('%d', '%d', '%s', '%d', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (0, 0, 'raw_keywords', 0, 0, 0, '2022-07-08', '2022-07-08', 'filter_article_type', '0-18y', 'English', 'Humans', 'Female')
cursor.execute(sql)
conn.commit()
