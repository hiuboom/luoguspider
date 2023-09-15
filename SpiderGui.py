import tkinter as tk
from threading import Thread
from LGSpider import LuoguSpider  # 导入题目的爬虫类
from SLSpider import SolutionSpider  # 导入题解的爬虫类
import requests
import bs4
import re
import urllib.parse
from fake_useragent import UserAgent

class LuoguSpiderGUI:
    def __init__(self):
        self.cookies = {
            "__client_id": "63e1d79c6956cb94a8b004f065e1ba46cf17d868",
            "login_referer": "https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000",
            "_uid": "1090731",
            "C3VK": "becbe2"
        }
        self.window = tk.Tk()
        self.window.title("Luogu Spider GUI")

        # 创建GUI控件
        self.start_label = tk.Label(self.window, text="开始题号:")
        self.start_entry = tk.Entry(self.window)
        self.end_label = tk.Label(self.window, text="结束题号:")
        self.end_entry = tk.Entry(self.window)
        self.start_button = tk.Button(
            self.window, text="爬取题目", command=self.start_spider)
        self.log_text = tk.Text(self.window, height=10, width=50)
        self.return_button = tk.Button(
            self.window, text="返回主页", command=self.return_to_main)
        self.second_button = tk.Button(
            self.window, text="爬取题解", command=self.second_spider)
        # 布局GUI控件
        self.start_label.grid(row=0, column=0, padx=5, pady=5)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)
        self.end_label.grid(row=1, column=0, padx=5, pady=5)
        self.end_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_button.grid(row=2, column=0,  padx=5, pady=5)
        self.second_button.grid(row=2, column=1,  padx=5, pady=5)
        self.log_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        self.return_button.grid(row=2, column=2,  padx=5, pady=5)

    def start_spider(self):
        start_pid = int(self.start_entry.get())
        end_pid = int(self.end_entry.get())
        spider = LuoguSpider(
            "https://www.luogu.com.cn/problem/P", "./luogu/", start_pid, end_pid)
        #爬题目
        spider.set_callback(self.update_log_text)
        t = Thread(target=self.run_spider, args=(spider,))
        t.start()

    def second_spider(self):
        start_pid = int(self.start_entry.get())
        end_pid = int(self.end_entry.get())
        cookies = self.cookies
        solutionSpider = SolutionSpider(cookies=cookies, url_base="https://www.luogu.com.cn/problem/solution/P", save_path="./luogu/", min_pid=start_pid, max_pid=end_pid)
        solutionSpider.set_callback(self.update_log_text)
        # 创建线程运行爬题解
        s = Thread(target=self.run_SolutionSpider, args=(solutionSpider,))
        s.start()

    def return_to_main(self):
        self.window.destroy()  # 关闭爬虫界面窗口
        from mainGui import MainGUI  # 导入主界面类
        main_gui = MainGUI()  # 创建主界面对象
        main_gui.start()  # 启动主界面的事件循环
    # def open_spider_gui(self):
    #     self.window.withdraw()  # 隐藏主界面窗口
    #     gui = MainGUI()
    #     gui.start()

    def run_spider(self, spider):
        # 运行爬虫
        spider.run()

    def run_SolutionSpider(self, solutionSpider):
        # 运行爬虫
        solutionSpider.solutions()

    def update_log_text(self, text):
        # 将新的输出追加到GUI文本框中
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)

    def start(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = LuoguSpiderGUI()
    gui.start()
