from pymysql import connect
import json


# 读取集合配置文件
sql = """create table new_search_history(history_id int(11)not null, primary key (history_id), result_path_id int(11)not null, raw_keywords varchar(256)not null, search_completed_flag int(11)not null, uuid int(11)not null, foreign key (uuid) references user(uuid), favourite_flag int(11)not null, start_time varchar(16)not null, end_time varchar(16)not null, filter_article_type varchar(128)not null,"""
set_conf = json.load(open("set_conf.json", 'r'))
for category in set_conf.keys():
    sql += ' ' + category + ' '
    sql += set_conf[category] + 'not null,'

sql = sql[:-1] + ')'
print(sql)

# 创建数据表
conn = connect(host='42.192.44.52', port=3306, user='root', password='root', database='gensci-web-doc-retrieval-db',
               charset='utf8')
cursor = conn.cursor()
cursor.execute(sql)
