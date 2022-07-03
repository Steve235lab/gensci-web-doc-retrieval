from pymysql import connect

conn = connect(host='42.192.44.52', port=3306, user='root', password='root',
                    database='gensci-web-doc-retrieval-db', charset='utf8')
cursor = conn.cursor()

sql = """select * from new_search_history"""
cursor.execute(sql)
history = cursor.fetchone()

print(history[8].split(','))

