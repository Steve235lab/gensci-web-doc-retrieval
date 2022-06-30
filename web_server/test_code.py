import json
import time

file_dir = 'static/json_data_test/'

# 读取 file.list 获取包含结果文献信息的json文件目录
start_time = time.time()
file_list = open(file_dir + 'file.list', 'r')
json_dir_list = file_list.readlines()
paper_info_list = []

for json_dir in json_dir_list:
    json_dir = json_dir[:-1]
    raw_paper_info = json.load(open(json_dir, 'r'))
    paper_info_list.append(raw_paper_info)

sorted_paper_info = sorted(paper_info_list, key=lambda x: x['publication_date'])
end_time = time.time()

# print(sorted_paper_info)
print("time: ", end_time-start_time)
