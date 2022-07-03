from pymysql import connect

sql = """create table test_create_paper_abstract(pmid int(11)not null, highlight_abstract longtext not null)"""

print(sql)

# 创建数据表
conn = connect(host='42.192.44.52', port=3306, user='root', password='root', database='gensci-web-doc-retrieval-db',
               charset='utf8')
cursor = conn.cursor()
cursor.execute(sql)
