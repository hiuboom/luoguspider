#题目爬虫
import re
import bs4
import time
import os
import requests
from fake_useragent import UserAgent
import json
import jsonpath
import urllib.parse
from threading import Thread

class LuoguSpider:
    def __init__(self, base_url, save_path, min_pid, max_pid):
        self.base_url = base_url
        self.save_path = save_path
        self.min_pid = min_pid
        self.max_pid = max_pid
        self.callback = None  # 回调函数
        self.user_agent = UserAgent()
        self.headers = {'User-Agent': self.user_agent.random}

    def set_callback(self, callback):
        self.callback = callback

    def get_html(self, url):
        # self.driver = webdriver.PhantomJS(
        #     executable_path="D:\\DownloadsD\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
        # self.driver.get(url=url)
        # time.sleep(1)
        res=requests.get(url=url,headers=self.headers)
        html = res.text
        # html = self.driver.page_source
        # self.driver.close()
        if str(html).find("Exception") == -1:
            return html
        else:
            return "error"

    def get_problem_info(self,start_num, end_num):
        user_agent = UserAgent()
        headers = {'User-Agent': user_agent.random}
        tag_url = 'https://www.luogu.com.cn/_lfe/tags'
        tag_html = requests.get(url=tag_url, headers=headers).json()
        tags_dicts = [{'id': tag['id'], 'name': tag['name']} for tag in tag_html['tags'] if tag['type'] not in [1, 3, 4]]
        
        difficulty_map = {0: '暂无评定', 1: '入门', 2: '普及−', 3: '普及/提高−', 
                        4: '普及+/提高', 5: '提高+/省选−', 6: '省选/NOI−', 7: 'NOI/NOI+/CTSC'}
        
        problem_list = []
        page = 0
        while page < 10:
            url = 'https://www.luogu.com.cn/problem/list?page=f{page}'
            page += 1
            html = requests.get(url=url, headers=headers).text
            url_parse = re.findall('decodeURIComponent\((.*?)\)\)', html)[0]
            html_parse = json.loads(urllib.parse.unquote(url_parse)[1:-1])
            result_list = list(jsonpath.jsonpath(html_parse, '$.currentData.problems.result')[0])
            for result in result_list:
                problem_id = jsonpath.jsonpath(result, '$.pid')[0]
                problem_id_trimmed = problem_id[1:]
                
                if int(problem_id_trimmed) < start_num:
                    continue
                if int(problem_id_trimmed) > end_num:
                    break

                title = jsonpath.jsonpath(result, '$.title')[0]
                difficulty = difficulty_map[int(jsonpath.jsonpath(result, '$.difficulty')[0])]
                tags_s = list(jsonpath.jsonpath(result, '$.tags')[0])
                tags = [tag_dict['name'] for tag_dict in tags_dicts if tag_dict['id'] in tags_s]
                
                problem_info = {
                    "题号": problem_id,
                    "题目": title,
                    "标签": tags,
                    "难度": difficulty
                }
                problem_list.append(problem_info)
        problem_list = list(set(problemproblem_list))
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(problem_list, f, ensure_ascii=False, indent=4)

    def parse_html(self, html):
        bs = bs4.BeautifulSoup(html, "html.parser")
        core = bs.select("article")[0]
        title = bs.select("title")[0].get_text()
        md = str(core)
        md = re.sub("<h1>", "# ", md)
        md = re.sub("<h2>", "## ", md)
        md = re.sub("<h3>", "#### ", md)
        md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
        return md, title

    def save_data(self, data, filename):
        cfilename = self.save_path + filename
        file = open(cfilename, "w", encoding="utf-8")
        for d in data:
            file.writelines(d)
        file.close()

    def run(self):
        self.log(f"爬取P{self.min_pid}\n")
        for i in range(self.min_pid, self.max_pid + 1):
            self.log(f"正在爬取P{i}...", end="")
            html = self.get_html(self.base_url + str(i))

            if html == "error":
                self.log("爬取失败...\n")
            else:
                data, title = self.parse_html(html)
                self.log("爬取成功,正在保存...", end="")
                self.save_data(data, f"P{i}" + title + ".md")
                self.log("保存成功!\n")
        self.log("爬取完成!\n")
        self.get_problem_info(self.min_pid, self.max_pid)


    def log(self, text, end="\n"):
        print(text, end=end)
        if self.callback:
            self.callback(text)  # 调用回调函数
