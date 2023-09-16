#题解爬虫
import re
import bs4
import time
import urllib.parse
import os
import requests
from fake_useragent import UserAgent


class SolutionSpider:
    def __init__(self, cookies, url_base, save_path, min_pid, max_pid):
        self.cookies = cookies
        self.url_base = url_base
        self.save_path = save_path
        self.min_pid = min_pid
        self.max_pid = max_pid
        self.callback = None  # 回调函数
        self.user_agent = UserAgent()
        self.headers = {'User-Agent': self.user_agent.random}

    def set_callback(self, callback):
        self.callback = callback

    def get_html(self, url):
        for key in self.cookies:
            c = {}
            c['name'] = key
            c['value'] = self.cookies[key]
            c['domain'] = ".luogu.com.cn"
            c['path'] = "/"
            c['httpOnly'] = False
            c['secure'] = False
        res = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        html = res.text
        if str(html).find("Exception") == -1:
            return html
        else:
            return "error"
    
    def get_md(self, html):
        bs = bs4.BeautifulSoup(html, "lxml")
        js_text = bs.find("script").get_text()
        r_text = re.search('(%[^"]+)(?=")', js_text)  # 题解的正则表达式
        python_text = urllib.parse.unquote(r_text.group(0))
        python_text = python_text.encode(
            'utf-8').decode('unicode_escape')  # 解码
        return python_text

    def Get_Problem_title(self,problemID):
        url = 'https://www.luogu.com.cn/problem/P' + str(problemID)
        r = requests.get(url, headers=self.headers)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        title = soup.find('title').text
        title = title.split('-')[0]
        title = title.strip()
        return title

    def save_data(self, data, filename):
        folder_name = os.path.splitext(filename)[0]
        folder_name = folder_name.split("-题解")[0]+ "/"
        folder_path = os.path.join(self.save_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        cfilename = folder_path + filename
        file = open(cfilename, "w", encoding="utf-8")
        for d in data:
            file.writelines(d)
        file.close()

    def solutions(self):
        self.log("爬取题解P{}".format(self.min_pid))
        for i in range(self.min_pid, self.max_pid+1):
            self.log("正在爬取P{}的题解...".format(i), end="")
            html = self.get_html(self.url_base + str(i))
            if html == "error":
                self.log("爬取失败...\n")
            else:
                problem_md = self.get_md(html)
                self.log("题解爬取成功！..", end="")
                self.save_data(problem_md, f"P{i}-"+self.Get_Problem_title(i)+"-题解"+".md")
                self.log("保存成功!\n")
        self.log("题解爬取完毕\n")

    def log(self, text, end="\n"):
        print(text, end=end)
        if self.callback:
            self.callback(text)  # 调用回调函数

if __name__ == '__main__':
    cookies = {
        "__client_id": "63e1d79c6956cb94a8b004f065e1ba46cf17d868",
        "login_referer": "https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000",
        "_uid": "1090731",
        "C3VK": "becbe2"
    }
    spider = LuoguSpider(cookies=cookies, url_base="https://www.luogu.com.cn/problem/solution/P",
                         save_path="./luogu/luogu/", min_pid=1000, max_pid=1002)
    spider.solutions()
