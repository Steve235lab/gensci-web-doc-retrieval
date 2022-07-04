from pymysql import connect

conn = connect(host='42.192.44.52', port=3306, user='root', password='root',
                    database='gensci-web-doc-retrieval-db', charset='utf8')
cursor = conn.cursor()

sql = """select * from new_search_history"""
cursor.execute(sql)
history = cursor.fetchall()
cache = history[9][9]
print(cache)
#
# print(history[8].split(','))

# sql = """insert into new_search_history values ('%d', '%d', '%s', '%d', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (2, 1, 'test_insert', 1, 0, 0, '2022-07-03', '2022-07-04', 'Books and Documents,Clinical Trial', 2, 1, 1, 1)
# cursor.execute(sql)
# conn.commit()


