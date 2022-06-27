import json
import time

print("Loading data from json files...")

# 更改至测试用路径，部署到生产环境时须注释掉下面一行代码
file_dir = 'E:/gensci_internship/gensci-web-doc-retrieval/web_server/static/json_data_test/'

# 读取 file.list 获取包含结果文献信息的json文件目录
file_list = open(file_dir + 'file.list', 'r')

json_dir_list = file_list.readlines()

json_dir = json_dir_list[0][:-1]

# json_file = open(json_dir, 'r')
# json_str = json_file.read()
# raw_paper_info = json.loads(json_str)

# start_time = time.time()
# for i in range(1000):
#     raw_paper_info = json.load(open(json_dir, 'r'))
#     pmid = raw_paper_info['pmid']
#     journal = raw_paper_info['journal']
#     publication_type = raw_paper_info['publication_type']
#     publication_year = raw_paper_info['publication_year']
# end_time = time.time()
# print(end_time - start_time)
#
# start_time = time.time()
# for i in range(1000):
#     pmid = json.load(open(json_dir, 'r'))['pmid']
#     journal = json.load(open(json_dir, 'r'))['journal']
#     publication_type = json.load(open(json_dir, 'r'))['publication_type']
#     publication_year = json.load(open(json_dir, 'r'))['publication_year']
# end_time = time.time()
# print(end_time - start_time)

abstract_highlight_list = json.load(
    open('E:/gensci_internship/gensci-web-doc-retrieval/web_server/static/json_data_test/json/PMID-29145468.json',
         'r'))['abstract_highlight']

# abstract_highlight_str = ''
# for i in range(len(abstract_highlight_list)):
#     word = abstract_highlight_list[i]
#     if word != '':
#         if word[0] == '<':
#             color_sp = word.find('font_color=') + 11
#             color_ep = word.find('>')
#             color = word[color_sp:color_ep]
#             abstract_highlight_str += '<span style="font-weight: bold; font-style: italic; color: ' + color + ';">'
#             abstract_highlight_str += abstract_highlight_list[i + 1] + '</span>'
#             try:
#                 abstract_highlight_list[i + 1] = ''
#             except:
#                 pass
#         else:
#             abstract_highlight_str += word

# print(abstract_highlight_str)
