import json
import datetime
from threading import Thread
import sys

sys.path.append('..')

from emoji import emojize
import openpyxl
from django.http import JsonResponse

from database_new import DATABASE
from uuid_token import forge_token, get_uuid_from_token


def search(request):
    """搜索请求处理函数

    url: 42.192.44.52:8000/search/

    解包前端发送的json，将各字段组合成搜索语句，将搜索记录保存至数据库

    **启动搜索服务**：在这里添加搜索服务的入口
    """
    # 解包前端请求
    if request.method == 'GET':
        if DATABASE.emoji_status is True:
            print(emojize(':white_check_mark: 已收到 search 请求', language='alias'))
            print(request.GET)

        token = request.GET.get('token')
        keywords = request.GET.get('keywords')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        article_type = request.GET.get('article_type')
        language = request.GET.get('language')
        species = request.GET.get('species')
        sex = request.GET.get('sex')
        age = request.GET.get('age')

    if request.method == 'POST':
        if DATABASE.emoji_status is True:
            print(emojize(':white_check_mark: 已收到 search 请求', language='alias'))
            print(request.POST)

        token = request.POST.get('token')
        keywords = request.POST.get('keywords')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        article_type = request.POST.get('article_type')
        language = request.POST.get('language')
        species = request.POST.get('species')
        sex = request.POST.get('sex')
        age = request.POST.get('age')

        print("article_type: ", article_type)
        print("language: ", language)
        print("species: ", species)
        print("sex: ", sex)
        print("age: ", age)

    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
    else:
        uuid = int(uuid_str)

        # 拼接搜索语句
        if start_time is None:
            start_time = '1900-01-01'
        if end_time is None:
            end_time = datetime.datetime.now().strftime('%Y-%m-%d')
        robust_keywords = '(' + keywords + ') AND ("' + start_time + '"[Date - Publication]:' + '"' + end_time + '"[Date - Publication])'
        if article_type is not None and len(article_type) > 0 and article_type != '[]':
            article_type = article_type.replace('[', '').replace('"', '').replace(']', '').split(',')
            if len(article_type) > 0:
                robust_keywords += ' AND ('
                for f in article_type:
                    robust_keywords += '(' + f + '[FILT]) OR ('
                robust_keywords = robust_keywords[:-5] + ')'
        if language is not None and len(language) > 0 and language != '[]':
            language = language.replace('[', '').replace('"', '').replace(']', '').split(',')
            if len(language) > 0:
                robust_keywords += ' AND ('
                for f in language:
                    robust_keywords += '(' + f + '[Language]) OR ('
                robust_keywords = robust_keywords[:-5] + ')'
        if species is not None and len(species) > 0 and species != '[]':
            species = species.replace('[', '').replace('"', '').replace(']', '').split(',')
            if len(species) > 0:
                robust_keywords += ' AND ('
                for f in species:
                    robust_keywords += '(' + f + '[FILT]) OR ('
                robust_keywords = robust_keywords[:-5] + ')'
        if sex is not None and len(sex) > 0 and sex != '[]':
            sex = sex.replace('[', '').replace('"', '').replace(']', '').split(',')
            if len(sex) > 0:
                robust_keywords += ' AND ('
                for f in sex:
                    robust_keywords += '(' + f + '[FILT]) OR ('
                robust_keywords = robust_keywords[:-5] + ')'
        if age is not None and len(age) > 0 and age != '[]':
            age = age.replace('[', '').replace('"', '').replace(']', '').split(',')
            if len(age) > 0:
                robust_keywords += ' AND ('
                for f in age:
                    robust_keywords += '(' + f + '[FILT]) OR ('
                robust_keywords = robust_keywords[:-5] + ')'

        print("Search keywords: ", robust_keywords)

        # 保存搜索记录
        timestamp = DATABASE.add_search_history(robust_keywords, uuid, keywords)

        # 开启一个单独的线程运行搜索服务并在搜索完成后执行善后处理
        search_thread = Thread(target=run_search, args=(robust_keywords, timestamp))
        search_thread.start()

        # 向前端返回响应
        new_token = forge_token(uuid_str)
        json_rsp = {
            'message_type': 'search_received',
            'token': new_token
        }

    if DATABASE.emoji_status is True:
        print(emojize(':rocket: 已发送 search_received 应答', language='alias'))
        print(json_rsp)

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache


def run_search(robust_keywords: str, timestamp: int):
    """适用于单个线程的执行搜索及搜索完成善后任务的函数

    将 robust_keywords 输入搜索脚本，启动搜索服务；完成搜索后将本次搜索在 search_history 表中的条目修改为已完成搜索

    :param robust_keywords: (str) 经过鲁棒性处理后的搜索关键词组合
    :param timestamp: (int) 本次搜索对应的搜索记录的时间戳
    :return: None
    """
    # 获取结果保存路径
    history = DATABASE.get_result(timestamp)[0]
    result_timestamp = history[1]
    result_dir = 'static/search_result/' + str(result_timestamp) + '/'

    # TODO: 启动搜索，使用 robust_keywords 作为关键词进行搜索，将 paper_info.xlsx 和 clue_info.xlsx 两个文件输出到 result_dir 下

    # 将数据库中所有搜索该关键词的搜索记录标记为已完成搜索
    DATABASE.search_completed(robust_keywords)

    # TODO: 向发起搜索的用户发送提醒邮件


def get_history(request):
    """获取用户历史记录请求处理函数

    url: 42.192.44.52:8000/search/history/

    使用uuid在数据库中查找该用户的历史记录，以json形式发送到前端
    """
    # 解包前端请求
    if request.method == 'GET':
        token = request.GET.get('token')
    if request.method == 'POST':
        token = request.POST.get('token')

    if DATABASE.emoji_status is True:
        print(emojize(':white_check_mark: 已收到 get_history 请求', language='alias'))
        print(emojize(':snake: token: ' + token, language='alias'))

    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
    else:
        uuid = int(uuid_str)
        # 使用uuid查找用户的历史记录。注意，这里查询到的不一定是全部记录，这取决于 Database.get_search_history 中设定的最大条数。
        history_list = DATABASE.get_search_history(uuid)
        history_list = history_list[::-1]
        # print(history_list)
        new_token = forge_token(uuid_str)
        json_rsp = {
            'message_type': 'history_list',
            'history': [],
            'token': new_token
        }
        # 将历史记录放入 'history' 字段
        for history in history_list:
            timestamp = history[0]
            raw_keywords = history[6]
            robust_keywords = history[2]
            history_dic = {'timestamp': timestamp, 'raw_keywords': raw_keywords, 'robust_keywords': robust_keywords}
            json_rsp['history'].append(history_dic)

    if DATABASE.emoji_status is True:
        print(emojize(':rocket: 已发送 rsp_get_history 应答', language='alias'))
        print(json_rsp)

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache


# def get_result(request):
#     """获取搜索结果请求处理函数
#
#     url: 42.192.44.52:8000/search/result/
#
#     使用时间戳在数据库中查找搜索结果（result_timestamp），然后到 /static/search_result/result_timestamp/ 中读取excel文件，
#     最后形成json发送至前端
#     """
#     # 解包前端请求
#     if request.method == 'GET':
#         token = request.GET.get('token')
#         timestamp = request.GET.get('timestamp')
#         page_num = request.GET.get('page_num')
#     if request.method == 'POST':
#         token = request.POST.get('token')
#         timestamp = request.POST.get('timestamp')
#         page_num = request.POST.get('page_num')
#
#     # 请求合法性判断
#     # 从token中获取uuid
#     uuid_str = get_uuid_from_token(token)
#     # token时效性判断
#     if uuid_str == 'token expired':
#         json_rsp = {"message_type": "token_expired"}
#         cache = JsonResponse(json_rsp)
#         cache["Access-Control-Allow-Origin"] = "*"
#         return cache
#     else:
#         print("Loading data from excel files!")
#         uuid = int(uuid_str)
#         timestamp = int(timestamp)
#         # 使用 timestamp 到数据库中查找此条历史记录
#         history = DATABASE.get_result(timestamp)[0]
#         if uuid == int(history[4]):     # 身份验证通过
#             new_token = forge_token(uuid_str)
#             json_rsp = {
#                 "message_type": "result",
#                 "paper_info": [],
#                 "clue_info": [],
#                 "token": new_token
#             }
#             result_timestamp = history[1]
#             file_dir = 'static/search_result/' + str(result_timestamp) + '/'
#
#             # 读取 'paper_info.xlsx'，将信息放入 "paper_info" 字段
#             file_name = file_dir + 'paper_info.xlsx'
#             workbook = openpyxl.load_workbook(file_name)
#             worksheet = workbook.get_sheet_by_name("Sheet1")
#             row_max = worksheet.max_row
#             page_num = int(page_num)
#
#             # 每页显示的文章数目
#             papers_on_one_page = 10
#
#             row_start = (page_num - 1) * 10 + 2
#             row_end = row_start + papers_on_one_page
#
#             if row_start < row_max:
#                 if row_end > row_max:
#                     row_end = row_max
#                 for i in range(row_start, row_end):
#                     paper_info = {}
#                     paper_info['Pmid'] = worksheet.cell(i, 1).value
#                     paper_info['Journal'] = worksheet.cell(i, 2).value
#                     paper_info['Publication_Type'] = worksheet.cell(i, 3).value
#                     paper_info['Publication_Year'] = worksheet.cell(i, 4).value
#                     paper_info['Publication_Date'] = worksheet.cell(i, 5).value
#                     paper_info['Title'] = worksheet.cell(i, 6).value
#                     paper_info['First_Author'] = worksheet.cell(i, 7).value
#                     paper_info['Corresponding_Author'] = worksheet.cell(i, 8).value
#                     paper_info['Authors'] = worksheet.cell(i, 9).value
#                     paper_info['Affiliations'] = worksheet.cell(i, 10).value
#                     paper_info['Abstract'] = worksheet.cell(i, 11).value
#                     paper_info['Keywords'] = worksheet.cell(i, 12).value
#                     paper_info['Doi'] = worksheet.cell(i, 13).value
#                     paper_info['Journal_If'] = worksheet.cell(i, 14).value
#                     paper_info['Conclusion'] = worksheet.cell(i, 15).value
#                     paper_info['Chinese_Title'] = worksheet.cell(i, 16).value
#                     paper_info['Chinese_Abstract'] = worksheet.cell(i, 17).value
#                     paper_info['Sample_Size'] = worksheet.cell(i, 18).value
#                     paper_info['Location'] = worksheet.cell(i, 19).value
#                     paper_info['Organization'] = worksheet.cell(i, 20).value
#
#                     json_rsp["paper_info"].append(paper_info)
#
#             # 读取 'clue_info.xlsx'，将信息放入 "clue_info" 字段
#             file_name = file_dir + 'clue_info.xlsx'
#             workbook = openpyxl.load_workbook(file_name)
#             worksheet = workbook.get_sheet_by_name("Sheet1")
#             row_max = worksheet.max_row
#
#             for i in range(2, row_max):
#                 clue_info = {}
#                 clue_info['Node1'] = worksheet.cell(i, 1).value
#                 clue_info['Edge_Type'] = worksheet.cell(i, 2).value
#                 clue_info['Node2'] = worksheet.cell(i, 3).value
#                 clue_info['Weight'] = worksheet.cell(i, 4).value
#                 clue_info['Paper_List'] = worksheet.cell(i, 5).value
#                 clue_info['Original_Text'] = worksheet.cell(i, 6).value
#
#                 json_rsp["clue_info"].append(clue_info)
#
#             cache = JsonResponse(json_rsp)
#             cache["Access-Control-Allow-Origin"] = "*"
#             return cache
#
#         else:   # 发送请求的用户与历史记录所属用户不匹配
#             json_rsp = {"message_type": "invalid_request"}
#             cache = JsonResponse(json_rsp)
#             cache["Access-Control-Allow-Origin"] = "*"
#             return cache


def get_paper_info(request):
    """获取文献列表请求处理函数

    url: 42.192.44.52:8000/search/paper_info/

    使用时间戳在数据库中查找搜索结果（result_timestamp），然后到 /static/search_result/result_timestamp/ 中读取excel文件，
    最后形成json发送至前端
    """
    # 解包前端请求
    if request.method == 'GET':
        token = request.GET.get('token')
        timestamp = request.GET.get('timestamp')
        page_num = request.GET.get('page_num')
    if request.method == 'POST':
        token = request.POST.get('token')
        timestamp = request.POST.get('timestamp')
        page_num = request.POST.get('page_num')

    if DATABASE.emoji_status is True:
        print(emojize(':white_check_mark: 已收到 get_paper_info 请求', language='alias'))
        print(emojize(':snake: token: ' + token, language='alias'))
        print(emojize(':snake: timestamp: ' + timestamp, language='alias'))
        print(emojize(':snake: page_num: ' + page_num, language='alias'))

    # 请求合法性判断
    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
    else:
        uuid = int(uuid_str)
        timestamp = int(timestamp)
        # 使用 timestamp 到数据库中查找此条历史记录
        history = DATABASE.get_result(timestamp)[0]
        if uuid == int(history[4]):  # 身份验证通过
            new_token = forge_token(uuid_str)
            json_rsp = {
                "message_type": "paper_info",
                "paper_info": [],
                "token": new_token
            }

            # 获取结果数据的后端目录
            result_timestamp = history[1]
            file_dir = 'static/search_result/' + str(result_timestamp) + '/'

            # 每页显示的文章数目
            papers_on_one_page = 10

            # 使用excel文件作为数据源加载结果数据
            if DATABASE.data_source == 'excel':
                print("Loading data from excel files...")

                # 读取 'paper_info.xlsx'，将信息放入 "paper_info" 字段
                file_name = file_dir + 'paper_info.xlsx'
                workbook = openpyxl.load_workbook(file_name, read_only=True)
                worksheet = workbook["Sheet1"]
                row_max = worksheet.max_row
                page_num = int(page_num)

                json_rsp['total'] = row_max - 1

                row_start = (page_num - 1) * papers_on_one_page + 2
                row_end = row_start + papers_on_one_page

                if row_start <= row_max:
                    if row_end > row_max:
                        row_end = row_max + 1
                    for i in range(row_start, row_end):
                        paper_info = {}
                        paper_info['Pmid'] = worksheet.cell(i, 1).value
                        paper_info['Journal'] = worksheet.cell(i, 2).value
                        paper_info['Publication_Type'] = worksheet.cell(i, 3).value
                        paper_info['Publication_Year'] = worksheet.cell(i, 4).value
                        paper_info['Publication_Date'] = worksheet.cell(i, 5).value
                        paper_info['Title'] = worksheet.cell(i, 6).value
                        paper_info['First_Author'] = worksheet.cell(i, 7).value
                        paper_info['Corresponding_Author'] = worksheet.cell(i, 8).value
                        paper_info['Authors'] = worksheet.cell(i, 9).value
                        paper_info['Affiliations'] = worksheet.cell(i, 10).value
                        # paper_info['Abstract'] = worksheet.cell(i, 11).value
                        paper_info['Keywords'] = worksheet.cell(i, 12).value
                        paper_info['Doi'] = worksheet.cell(i, 13).value
                        paper_info['Journal_If'] = worksheet.cell(i, 14).value
                        paper_info['Conclusion'] = worksheet.cell(i, 15).value
                        paper_info['Chinese_Title'] = worksheet.cell(i, 16).value
                        paper_info['Chinese_Abstract'] = worksheet.cell(i, 17).value
                        paper_info['Sample_Size'] = worksheet.cell(i, 18).value
                        paper_info['Location'] = worksheet.cell(i, 19).value
                        paper_info['Organization'] = worksheet.cell(i, 20).value

                        json_rsp["paper_info"].append(paper_info)

            # 使用json文件作为数据源加载结果数据
            if DATABASE.data_source == 'json':
                print("Loading data from json files...")

                # 更改至测试用路径，部署到生产环境时须注释掉下面一行代码
                file_dir = 'static/json_data_test/'

                # 读取 file.list 获取包含结果文献信息的json文件目录
                file_list = open(file_dir + 'file.list', 'r')
                json_dir_list = file_list.readlines()
                # print(json_dir_list)
                row_max = len(json_dir_list)
                page_num = int(page_num)

                json_rsp['total'] = row_max

                row_start = (page_num - 1) * papers_on_one_page
                row_end = row_start + papers_on_one_page
                # print(row_start)
                # print(row_end)

                if row_start <= row_max:
                    if row_end > row_max:
                        row_end = row_max
                    for i in range(row_start, row_end):
                        json_dir = json_dir_list[i][:-1]    # 删除换行符 \n
                        raw_paper_info = json.load(open(json_dir, 'r'))
                        paper_info = {}
                        paper_info['Pmid'] = raw_paper_info['pmid']
                        paper_info['Journal'] = raw_paper_info['journal']
                        paper_info['Publication_Type'] = raw_paper_info['publication_type']
                        paper_info['Publication_Year'] = raw_paper_info['publication_year']
                        paper_info['Publication_Date'] = raw_paper_info['publication_date']
                        paper_info['Title'] = raw_paper_info['title']
                        paper_info['First_Author'] = raw_paper_info['first_author']
                        paper_info['Corresponding_Author'] = raw_paper_info['corresponding_author']
                        paper_info['Authors'] = raw_paper_info['authors']
                        paper_info['Affiliations'] = raw_paper_info['affiliations']
                        paper_info['Abstract'] = raw_paper_info['abstract']
                        paper_info['Keywords'] = raw_paper_info['keywords']
                        paper_info['Doi'] = raw_paper_info['doi']
                        paper_info['Journal_If'] = raw_paper_info['journal_if']
                        paper_info['Chinese_Title'] = raw_paper_info['title_zh']
                        paper_info['Chinese_Abstract'] = raw_paper_info['abstract_zh']
                        paper_info['Sample_Size'] = raw_paper_info['sample_size']
                        # 以下3个字段可能在原始json文件中不存在
                        try:
                            paper_info['Conclusion'] = raw_paper_info['conclusion']
                        except:
                            paper_info['Conclusion'] = ''
                        try:
                            paper_info['Location'] = raw_paper_info['location']
                        except:
                            paper_info['Location'] = ''
                        try:
                            paper_info['Organization'] = raw_paper_info['organization']
                        except:
                            paper_info['Organization'] = ''

                        json_rsp["paper_info"].append(paper_info)
                        # print(paper_info)

        else:   # 发送请求的用户与历史记录所属用户不匹配
            json_rsp = {"message_type": "invalid_request"}

    if DATABASE.emoji_status is True:
        print(emojize(':rocket: 已发送 rsp_get_paper_info 应答', language='alias'))
        print(json_rsp)

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache


def get_clue_info(request):
    """获取线索列表请求处理函数

    url: 42.192.44.52:8000/search/clue_info/

    使用时间戳在数据库中查找搜索结果（result_timestamp），然后到 /static/search_result/result_timestamp/ 中读取excel文件，
    最后形成json发送至前端
    """
    # 解包前端请求
    if request.method == 'GET':
        token = request.GET.get('token')
        timestamp = request.GET.get('timestamp')
        page_num = request.GET.get('page_num')
    if request.method == 'POST':
        token = request.POST.get('token')
        timestamp = request.POST.get('timestamp')
        page_num = request.POST.get('page_num')

    if DATABASE.emoji_status is True:
        print(emojize(':white_check_mark: 已收到 get_clue_info 请求', language='alias'))
        print(emojize(':snake: token: ' + token, language='alias'))
        print(emojize(':snake: timestamp: ' + timestamp, language='alias'))
        print(emojize(':snake: page_num: ' + page_num, language='alias'))

    # 请求合法性判断
    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
    else:
        print("Loading data from excel files...")
        uuid = int(uuid_str)
        timestamp = int(timestamp)
        # 使用 timestamp 到数据库中查找此条历史记录
        history = DATABASE.get_result(timestamp)[0]
        if uuid == int(history[4]):  # 身份验证通过
            new_token = forge_token(uuid_str)
            json_rsp = {
                "message_type": "clue_info",
                "clue_info": [],
                "token": new_token
            }
            result_timestamp = history[1]
            file_dir = 'static/search_result/' + str(result_timestamp) + '/'

            # 读取 'clue_info.xlsx'，将信息放入 "clue_info" 字段
            file_name = file_dir + 'clue_info.xlsx'
            workbook = openpyxl.load_workbook(file_name, read_only=True)
            worksheet = workbook.get_sheet_by_name("Sheet1")
            row_max = worksheet.max_row
            page_num = int(page_num)

            json_rsp['total'] = row_max - 1

            # 如果页号为 0 则代表返回所有条目
            if page_num == 0:
                row_start = 2
                row_end = row_max
            else:
                # 每页显示的线索数目
                papers_on_one_page = 20

                row_start = (page_num - 1) * papers_on_one_page + 2
                row_end = row_start + papers_on_one_page

            if row_start <= row_max:
                if row_end > row_max:
                    row_end = row_max + 1
                for i in range(row_start, row_end):
                    clue_info = {}
                    clue_info['Node1'] = worksheet.cell(i, 1).value
                    clue_info['Edge_Type'] = worksheet.cell(i, 2).value
                    clue_info['Node2'] = worksheet.cell(i, 3).value
                    clue_info['Weight'] = worksheet.cell(i, 4).value
                    clue_info['Paper_List'] = worksheet.cell(i, 5).value
                    clue_info['Original_Text'] = worksheet.cell(i, 6).value

                    json_rsp["clue_info"].append(clue_info)

        else:  # 发送请求的用户与历史记录所属用户不匹配
            json_rsp = {"message_type": "invalid_request"}

    if DATABASE.emoji_status is True:
        print(emojize(':rocket: 已发送 rsp_get_clue_info 应答', language='alias'))
        print(json_rsp)

    cache = JsonResponse(json_rsp)
    cache["Access-Control-Allow-Origin"] = "*"
    return cache

