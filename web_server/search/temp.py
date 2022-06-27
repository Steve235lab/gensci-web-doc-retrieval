import json
import time

print("Loading data from json files...")

# 更改至测试用路径，部署到生产环境时须注释掉下面一行代码
file_dir = 'E:/gensci_internship/gensci-web-doc-retrieval/json_data_test/'

# 读取 file.list 获取包含结果文献信息的json文件目录
file_list = open(file_dir + 'file.list', 'r')

json_dir_list = file_list.readlines()

json_dir = json_dir_list[0][:-1]

# json_file = open(json_dir, 'r')
# json_str = json_file.read()
# raw_paper_info = json.loads(json_str)

start_time = time.time()
for i in range(1000):
    raw_paper_info = json.load(open(json_dir, 'r'))
    pmid = raw_paper_info['pmid']
    journal = raw_paper_info['journal']
    publication_type = raw_paper_info['publication_type']
    publication_year = raw_paper_info['publication_year']
end_time = time.time()
print(end_time - start_time)

start_time = time.time()
for i in range(1000):
    pmid = json.load(open(json_dir, 'r'))['pmid']
    journal = json.load(open(json_dir, 'r'))['journal']
    publication_type = json.load(open(json_dir, 'r'))['publication_type']
    publication_year = json.load(open(json_dir, 'r'))['publication_year']
end_time = time.time()
print(end_time - start_time)
