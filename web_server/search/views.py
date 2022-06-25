from threading import Thread
import sys

sys.path.append('..')

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
        token = request.GET.get('token')
        keywords = request.GET.get('keywords')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        filters = request.GET.get('filters')
    if request.method == 'POST':
        # print(request.POST)
        token = request.POST.get('token')
        keywords = request.POST.get('keywords')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        filters = request.POST.get('filters')

    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
        cache = JsonResponse(json_rsp)
        cache["Access-Control-Allow-Origin"] = "*"
        return cache
    else:
        uuid = int(uuid_str)

        # 拼接搜索语句
        robust_keywords = '(' + keywords + ') AND ("' + start_time + '"[Date - Publication]:' + '"' + end_time + '"[Date - Publication]) AND ('
        for f in filters['article_type']:
            robust_keywords += '(' + f + '[FILT]) OR ('
        robust_keywords = robust_keywords[:-5] + ') AND ('
        for f in filters['language']:
            robust_keywords += '(' + f + '[Language]) OR ('
        robust_keywords = robust_keywords[:-5] + ') AND ('
        for f in filters['species']:
            robust_keywords += '(' + f + '[FILT]) OR ('
        robust_keywords = robust_keywords[:-5] + ') AND ('
        for f in filters['sex']:
            robust_keywords += '(' + f + '[FILT]) OR ('
        robust_keywords = robust_keywords[:-5] + ') AND ('
        for f in filters['age']:
            robust_keywords += '(' + f + '[FILT]) OR ('
        robust_keywords = robust_keywords[:-5] + ')'

        print("Search keywords: ", robust_keywords)

        # 保存搜索记录
        timestamp = DATABASE.add_search_history(robust_keywords, uuid)

        # 开启一个单独的线程运行搜索服务并在搜索完成后执行善后处理
        search_thread = Thread(target=run_search, args=(robust_keywords, timestamp))
        search_thread.start()

        # 向前端返回响应
        new_token = forge_token(uuid_str)
        json_rsp = {
            'message_type': 'search_received',
            'token': new_token
        }
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

    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
        cache = JsonResponse(json_rsp)
        cache["Access-Control-Allow-Origin"] = "*"
        return cache
    else:
        uuid = int(uuid_str)
        # 使用uuid查找用户的历史记录。注意，这里查询到的不一定是全部记录，这取决于 Database.get_search_history 中设定的最大条数。
        history_list = DATABASE.get_search_history(uuid)
        # print(history_list)
        new_token = forge_token(uuid_str)
        json_rsp = {
            'message_type': 'history_list',
            'history': {},
            'token': new_token
        }
        # 将历史记录放入 'history' 字段
        for history in history_list:
            timestamp = history[0]
            keywords = history[2]
            json_rsp['history'][timestamp] = keywords
        cache = JsonResponse(json_rsp)
        cache["Access-Control-Allow-Origin"] = "*"
        return cache


def get_result(request):
    """获取搜索结果请求处理函数

    url: 42.192.44.52:8000/search/result/

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

    # 请求合法性判断
    # 从token中获取uuid
    uuid_str = get_uuid_from_token(token)
    # token时效性判断
    if uuid_str == 'token expired':
        json_rsp = {"message_type": "token_expired"}
        cache = JsonResponse(json_rsp)
        cache["Access-Control-Allow-Origin"] = "*"
        return cache
    else:
        print("Loading data from excel files!")
        uuid = int(uuid_str)
        timestamp = int(timestamp)
        # 使用 timestamp 到数据库中查找此条历史记录
        history = DATABASE.get_result(timestamp)[0]
        if uuid == int(history[4]):     # 身份验证通过
            new_token = forge_token(uuid_str)
            json_rsp = {
                "message_type": "result",
                "paper_info": [],
                "clue_info": [],
                "token": new_token
            }
            result_timestamp = history[1]
            file_dir = 'static/search_result/' + str(result_timestamp) + '/'

            # 读取 'paper_info.xlsx'，将信息放入 "paper_info" 字段
            file_name = file_dir + 'paper_info.xlsx'
            workbook = openpyxl.load_workbook(file_name)
            worksheet = workbook.get_sheet_by_name("Sheet1")
            row_max = worksheet.max_row
            page_num = int(page_num)

            # 每页显示的文章数目
            papers_on_one_page = 10

            row_start = (page_num - 1) * 10 + 2
            row_end = row_start + papers_on_one_page

            if row_start < row_max:
                if row_end > row_max:
                    row_end = row_max
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
                    paper_info['Abstract'] = worksheet.cell(i, 11).value
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

            # 读取 'clue_info.xlsx'，将信息放入 "clue_info" 字段
            file_name = file_dir + 'clue_info.xlsx'
            workbook = openpyxl.load_workbook(file_name)
            worksheet = workbook.get_sheet_by_name("Sheet1")
            row_max = worksheet.max_row

            for i in range(2, row_max):
                clue_info = {}
                clue_info['Node1'] = worksheet.cell(i, 1).value
                clue_info['Edge_Type'] = worksheet.cell(i, 2).value
                clue_info['Node2'] = worksheet.cell(i, 3).value
                clue_info['Weight'] = worksheet.cell(i, 4).value
                clue_info['Paper_List'] = worksheet.cell(i, 5).value
                clue_info['Original_Text'] = worksheet.cell(i, 6).value

                json_rsp["clue_info"].append(clue_info)

            cache = JsonResponse(json_rsp)
            cache["Access-Control-Allow-Origin"] = "*"
            return cache

        else:   # 发送请求的用户与历史记录所属用户不匹配
            json_rsp = {"message_type": "invalid_request"}
            cache = JsonResponse(json_rsp)
            cache["Access-Control-Allow-Origin"] = "*"
            return cache

