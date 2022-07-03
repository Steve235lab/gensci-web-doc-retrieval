from pymysql import connect
import json


# 读取枚举值
enum_values = []
enum_conf = json.load(open("enum_conf.json", 'r'))
for category in enum_conf.keys():
    enum_value = ''
    enum_values_for_a_filter = enum_conf[category]
    for meta in enum_values_for_a_filter:
        enum_value += meta.keys[0]

# # 创建数据表
# conn = connect(host='42.192.44.52', port=3306, user='root', password='root', database='gensci-web-doc-retrieval-db',
#                charset='utf8')
# cursor = conn.cursor()
# sql = "create table history(history_id int(11)not null, result_path_id int(11), raw_keywords varchar(256), search_completed_flag int(11), uuid int(11), favourite_flag int(11), start_time varchar(16), end_time varchar(16), filters enum(" + \
#       "), primary key(history_id))"

