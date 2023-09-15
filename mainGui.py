import tkinter as tk
from threading import Thread
from LGSpider import LuoguSpider

'''
    在SpiderGui.py中更换你的cookies
'''

class MainGUI:
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("主界面")
        self.window.geometry("400x300")

        self.spider_button = tk.Button(self.window, text="进入爬虫界面", command=self.open_spider_gui ,width=10, height=2)
        self.filter_button = tk.Button(self.window, text="进入搜题界面", command=self.open_filter_gui ,width=10, height=2)

        self.spider_button.pack(anchor=tk.CENTER, expand=tk.YES)
        self.filter_button.pack(anchor=tk.CENTER, expand=tk.YES)

    def open_spider_gui(self):
        self.window.destroy()  # 销毁主界面窗口
        from SpiderGui import LuoguSpiderGUI  # 导入爬虫界面类
        gui = LuoguSpiderGUI()
        gui.start()

    def open_filter_gui(self):
        self.window.destroy()  # 销毁主界面窗口
        from FilterGui import FilterApp  # 导入爬虫界面类
        gui = FilterApp()
        gui.start()

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    main_gui = MainGUI()
    main_gui.start()


