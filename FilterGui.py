import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json


class FilterApp:
    def __init__(self):
        self.root = tk.Tk()  # 创建主窗口
        self.root.title("题目筛选器")  # 设置标题
        self.root.geometry("400x600")  # 设置窗口大小

        # 定义两个 StringVar 变量，保存用户选择的题目难度和关键词
        self.selected_difficulty = tk.StringVar()
        self.selected_keywords = tk.StringVar()
        self.inputted_keyword = tk.StringVar()

        self.create_widgets()  # 创建各种界面部件
        self.root.mainloop()  # 启动事件循环，等待用户交互

    def create_widgets(self):
        frame = tk.Frame(self.root)  # 创建框架
        frame.pack(pady=10)  # 设置边距

        # 创建题目难度选择菜单
        label_difficulty = tk.Label(frame, text="题目难度")
        label_difficulty.grid(row=0, column=0, padx=10, pady=10)
        difficulty_options = ["", "入门", "普及−", "普及/提高−",
                              "普及+/提高", "提高+/省选−", "省选/NOI−", "NOI/NOI+/CTSC"]
        dropdown_difficulty = ttk.Combobox(
            frame, textvariable=self.selected_difficulty, values=difficulty_options)
        dropdown_difficulty.current(0)
        dropdown_difficulty.grid(row=0, column=1, padx=10, pady=10)

        # 创建标签词选择菜单
        label_keywords = tk.Label(frame, text="标签项")
        label_keywords.grid(row=1, column=0, padx=10, pady=10)
        keywords_options = ["", "动态规划,dp", "贪心", "递归",
                            "字符串", "动态规划", "枚举", "高精度", "模拟", "02优化", "进制","数学"]
        dropdown_keywords = ttk.Combobox(
            frame, textvariable=self.selected_keywords, values=keywords_options)
        dropdown_keywords.current(0)
        dropdown_keywords.grid(row=1, column=1, padx=10, pady=10)

        # 创建关键词输入框
        label_input_keyword = tk.Label(frame, text="关键词")
        label_input_keyword.grid(row=2, column=0, padx=10, pady=10)
        self.entry_input_keyword = tk.Entry(
            frame, textvariable=self.inputted_keyword)
        self.entry_input_keyword.grid(row=2, column=1, padx=10, pady=10)

        # 创建返回主界面按钮
        return_button = tk.Button(
            frame, text="返回主界面", command=self.return_to_main)
        return_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # 创建提交筛选项按钮
        button_submit = tk.Button(
            frame, text="提交筛选项", command=self.show_selected)
        button_submit.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # 创建列表框，用于显示符合条件的题目文件名
        results_frame = tk.Frame(self.root)
        results_frame.pack(pady=10)
        scrollbar_results = tk.Scrollbar(results_frame)
        scrollbar_results.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_results = tk.Listbox(
            results_frame, height=8, width=40, yscrollcommand=scrollbar_results.set)
        self.listbox_results.pack(side=tk.LEFT, fill=tk.BOTH)
        # 点击列表框中的文件名，会在文本框中显示文件内容
        self.listbox_results.bind("<<ListboxSelect>>", self.show_file)
        scrollbar_results.config(command=self.listbox_results.yview)

        # 创建文本框，用于显示选中的题目内容
        text_frame = tk.Frame(self.root)
        text_frame.pack(pady=10)
        self.text_display = tk.Text(text_frame, height=15, width=40)
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar_text = tk.Scrollbar(text_frame)
        scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_display.config(yscrollcommand=scrollbar_text.set)
        scrollbar_text.config(command=self.text_display.yview)

    def return_to_main(self):
        # 关闭筛选界面窗口
        self.root.destroy()
        # 导入主界面类，创建主界面对象，启动主界面的事件循环
        from mainGui import MainGUI
        main_gui = MainGUI()
        main_gui.start()

    def show_selected(self):
        selected_difficulty = self.selected_difficulty.get()  # 获取用户选择的题目难度
        selected_keywords = self.selected_keywords.get()  # 获取用户选择的关键词
        inputted_keyword = self.inputted_keyword.get()  # 获取用户输入的关键词

        # 在文本框中显示所选条件
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, f"题目难度: {selected_difficulty}\n")
        self.text_display.insert(tk.END, f"标签项: {selected_keywords}\n")
        self.text_display.insert(tk.END, f"关键词: {inputted_keyword}\n")

        def get_problem_data():
            try:
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except FileNotFoundError:
                return []

        folder_path = "./luogu/"
        files = os.listdir(folder_path)

        target_keyword = selected_keywords
        similar_files = []

        # 遍历指定目录下所有文件，找出符合条件的文件
        Problem_data = get_problem_data()

        flag = False

        for P_data in Problem_data:
            selectone = selected_difficulty == "" or selected_difficulty == P_data["难度"]
            selecttwo = target_keyword == "" or any(
                tag in target_keyword for tag in P_data["标签"])
            selectthree = not inputted_keyword or inputted_keyword in P_data["题目"].lower() or any(
                tag in inputted_keyword for tag in P_data["标签"]) or inputted_keyword in P_data["题号"] or inputted_keyword in P_data["难度"]

            if selectone and selecttwo and selectthree:
                html = str(P_data["题号"])
                # print(html)
                flag = True
                # for file in files:
                #     file_path = os.path.join(folder_path, file)
                #     with open(file_path, "r", encoding="utf-8") as f:
                #         if html in file:
                #             similar_files.append(file)
                for folder in files:
                    folder_path = os.path.join("./luogu/", folder)
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            if html in file:  
                                similar_files.append(file)

        similar_files=list(set(similar_files))

        if not flag:
            messagebox.showinfo("未找到", "未找到匹配的题目。")

        # 在列表框中显示符合条件的文件名
        self.listbox_results.delete(0, tk.END)
        for file in similar_files:
            self.listbox_results.insert(tk.END, file)

    def show_file(self, event):
        selected_file = self.listbox_results.get(
            self.listbox_results.curselection())  # 获取用户选择的文件名

        one=selected_file.split(".")[0].split("-题解")[0]
        file_path = os.path.join("./luogu/"+f"{one}" + "/" + selected_file)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 在文本框中显示所选文件的内容
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, content)


if __name__ == "__main__":
    app = FilterApp()
