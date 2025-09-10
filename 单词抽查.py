
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse

# ====== 爬虫函数：获取单词释义 ======
def get_definitions(word):
    url = f"https://dict.youdao.com/result?word={urllib.parse.quote(word)}&lang=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = "utf-8"
    except Exception as e:
        return f"网络错误: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    # 英文释义
    definition_elements = soup.find_all("span", class_="trans")
    pos_elements = soup.find_all("span", class_="pos")

    result = ""
    if definition_elements:
        definitions = [elem.text.strip() for elem in definition_elements]
        pos = [p.text.strip() for p in pos_elements]
        for p, d in zip(pos, definitions):
            result += f"{p}: {d}\n"

    # 中文翻译（页面结构可能要调整）
    chinese_elements = soup.select("div.trans-container ul li")
    if chinese_elements:
        result += "\n中文释义：\n"
        for li in chinese_elements:
            result += li.text.strip() + "\n"

    if not result:
        result = "未找到翻译，请检查单词是否正确。"

    return result.strip()


# ====== 数据准备：读取单词表 ======
df = pd.read_csv("words.csv", encoding="utf-8-sig")
words = df["word"].tolist()

current_word = ""  # 当前单词


# ====== GUI 界面 ======
root = tk.Tk()
root.title("考研单词抽查")
root.geometry("600x450")

# 单词显示
word_label = tk.Label(root, text="", font=("Arial", 24))
word_label.pack(pady=20)

# 输出框
output_text = scrolledtext.ScrolledText(root, width=70, height=12, font=("Arial", 12))
output_text.pack(pady=10)


# ====== 功能函数 ======
def pick_word():
    """随机抽取一个单词"""
    global current_word
    current_word = random.choice(words)
    word_label.config(text=current_word)
    output_text.delete(1.0, tk.END)


def query_translation():
    """统一的查询功能：优先查询输入框，否则查询随机单词"""
    global current_word
    word = entry.get().strip()

    if word:  # 输入框优先
        current_word = word
    elif current_word:  # 如果没有输入，就查抽取的单词
        word = current_word
    else:
        messagebox.showwarning("提示", "请先输入单词或抽取一个单词！")
        return

    result = get_definitions(word)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)


# 输入框 + 标签
label = tk.Label(root, text="输入要翻译的词汇:")
label.pack(padx=10, pady=5)

entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=5)
entry.bind("<Return>", lambda event: query_translation())  # 回车触发统一查询


# 按钮区域
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

pick_btn = tk.Button(btn_frame, text="抽一个单词", command=pick_word, font=("Arial", 12))
pick_btn.grid(row=0, column=0, padx=10)

query_btn = tk.Button(btn_frame, text="查询翻译", command=query_translation, font=("Arial", 12))
query_btn.grid(row=0, column=1, padx=10)

# 运行主循环
root.mainloop()





