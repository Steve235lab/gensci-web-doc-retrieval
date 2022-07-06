import json

edge_type_set = json.load(open('static/search_result/114514/clue_info.json', 'r'))['header']['Edge_Type']
key_list = edge_type_set.keys()
