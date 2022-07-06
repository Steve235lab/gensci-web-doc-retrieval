# run_search.py
# 使用一个常驻线程执行搜索任务
# Written by Steve D. J. on 2022/7/6.

import json
import time
import os
# from threading import Thread
# from multiprocessing import Process

from database_new import DATABASE
from email_sender import EmailSender
from controller import CONTROLLER


class Runner:
    """
    搜索任务队列：
    search_task_queue: (list) 待处理的搜索任务，其中每个元素为列表 [robust_keywords, result_dir]

    """
    def __init__(self):
        self.search_task_queue = []
        # self.thread = Thread(target=self.search_thread)
        # self.thread.start()
        # self.process = Process(target=self.search_thread)
        # self.process.start()

    def run_search(self, robust_keywords: str, timestamp: int, raw_keywords, start_time, end_time, filter_article_type, filter_age, filter_language, filter_species, filter_sex):
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

        # 查看结果文件是否已写入指定目录
        if os.path.exists(result_dir+'paper_info.xlsx') and os.path.exists(result_dir+'clue_info.xlsx') and os.path.exists(result_dir+'web_session.zip') and os.path.exists(result_dir+'clue_info.json') and os.path.exists(result_dir+'file.list'):
            # 从json文件中提取结果文献的 abstract_highlight 字段，生成HTML标签，保存至数据库 paper_abstract 表
            if CONTROLLER.test_mode is True:
                # 更改至测试用路径
                result_dir = 'static/json_data_test/'

            # 读取 file.list 获取包含结果文献信息的json文件目录
            file_list = open(result_dir + 'file.list', 'r')
            json_dir_list = file_list.readlines()
            for json_dir in json_dir_list:
                json_dir = json_dir[:-1]  # 删除换行符 \n
                raw_paper_info = json.load(open(json_dir, 'r'))
                pmid = int(raw_paper_info['pmid'])
                abstract_highlight_list = raw_paper_info['abstract_highlight']
                # 生成带有高亮的HTML字符串
                abstract_highlight_str = ''
                for i in range(len(abstract_highlight_list)):
                    word = abstract_highlight_list[i]
                    if word != '':
                        if word[0] == '<':
                            color_sp = word.find('font_color=') + 11
                            color_ep = word.find('>')
                            color = word[color_sp:color_ep]
                            abstract_highlight_str += '<span style="font-weight: bold; font-style: italic; color: ' + color + ';">'
                            abstract_highlight_str += abstract_highlight_list[i + 1] + '</span>'
                            try:
                                abstract_highlight_list[i + 1] = ''
                            except:
                                pass
                        else:
                            abstract_highlight_str += word
                # 写入数据库
                DATABASE.add_paper_highlight_abstract(pmid, abstract_highlight_str)

            # 将数据库中所有搜索该关键词的搜索记录标记为已完成搜索
            DATABASE.search_completed(raw_keywords, start_time, end_time, filter_article_type, filter_age, filter_language,
                                      filter_species, filter_sex)

            # 向发起搜索的用户发送提醒邮件
            # 生成验证码
            uuids = DATABASE.get_uuids_with_keywords(raw_keywords, start_time, end_time, filter_article_type, filter_age,
                                                     filter_language, filter_species, filter_sex)
            for uuid in uuids:
                uuid = uuid[0]
                user = DATABASE.get_user(uuid)
                email = user.email
                username = user.username
                email_sender = EmailSender(email, username)
                email_sender.generate_search_completed_content(robust_keywords)
                # 发送验证邮件
                email_sender.send()

    def search_thread(self):
        while True:
            if len(self.search_task_queue) > 0:
                search_task = self.search_task_queue[0]
                self.search_task_queue.pop(0)
                try:
                    self.run_search(search_task[0], search_task[1], search_task[2], search_task[3], search_task[4], search_task[5], search_task[6], search_task[7], search_task[8], search_task[9])
                except:
                    pass
            else:
                time.sleep(1)


SEARCH_RUNNER = Runner()
