import json

file_dir = 'static/json_data_test/'

# 读取 file.list 获取包含结果文献信息的json文件目录
file_list = open(file_dir + 'file.list', 'r')
json_dir_list = file_list.readlines()
json_dir = json_dir_list[0][:-1]
raw_paper_info = json.load(open(json_dir, 'r'))
op = raw_paper_info['pmid']
print(raw_paper_info['pmid'])
