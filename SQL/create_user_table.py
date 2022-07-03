from pymysql import connect

sql = """create table test_create_user(uuid int(11)not null, username varchar(64)not null, password varchar(64)not null, email varchar(128)not null, confirm_code varchar(64)not null, email_confirmed varchar(16)not null, permissions varchar(32)not null, removed varchar(16)not null)"""

print(sql)

# 创建数据表
conn = connect(host='42.192.44.52', port=3306, user='root', password='root', database='gensci-web-doc-retrieval-db',
               charset='utf8')
cursor = conn.cursor()
cursor.execute(sql)
