import subprocess
import platform
import keyboard
import pyperclip
import tkinter as tk
from agent_use import gpt_agent

class assistant():

    def __init__(self):
        self.agent = gpt_agent('chatglm2-6b')
        self.agent.init_messages_by_json('assistant.json')
        self.tasks = {'translate': "翻译以下内容到简体中文，尽可能连贯一些:\n", 'explain': "展开介绍或者解释以下内容，使用简体中文：\n"}
        self.know_reply = None
        self.current_tag = "user"  # 当前对话标签，开始为用户

        # 根据操作系统选择合适的键盘监听方式
        if platform.system() == "Linux":
            self.listener = keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+1': self.run_translate,
                '<ctrl>+<alt>+2': self.run_explain
            })
        elif platform.system() == "Windows":
            keyboard.add_hotkey('ctrl+alt+1', self.run_translate)
            keyboard.add_hotkey('ctrl+alt+2', self.run_explain)

        self.create_window()  # 创建显示窗口

    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Assistant Window")
        self.window.attributes('-topmost', True)  # 设置窗口总是在最上层
        self.text_widget = tk.Text(self.window, wrap=tk.WORD, font=("宋体", 12))  # 设置字体和文本框属性
        self.text_widget.pack(expand=tk.YES, fill=tk.BOTH)
        self.text_widget.config(state=tk.DISABLED)  # 文本框不可编辑
        self.text_widget.tag_configure("user", foreground="blue")  # 用户对话标签样式
        self.text_widget.tag_configure("assistant", foreground="green")  # 助手对话标签样式

    def run_translate(self):
        input_text = self.get_selected_text()
        if input_text:
            self.text_widget.config(state=tk.NORMAL)  # 使文本框可编辑
            self.text_widget.insert(tk.END, "用户要求翻译:\n" + input_text + "\n\n", self.current_tag)
            self.text_widget.config(state=tk.DISABLED)  # 恢复文本框为不可编辑状态

            self.agent.prompt_add(self.tasks['translate'] + input_text)
            reply = self.agent.prompt_post()
            self.know_reply = reply

            self.text_widget.config(state=tk.NORMAL)  # 使文本框可编辑
            self.text_widget.insert(tk.END, "来自助手的译文:\n" + reply + "\n\n", "assistant")
            self.text_widget.config(state=tk.DISABLED)  # 恢复文本框为不可编辑状态

    def run_explain(self):
        input_text = self.get_selected_text()
        if input_text:
            self.text_widget.config(state=tk.NORMAL)  # 使文本框可编辑
            self.text_widget.insert(tk.END, "用户要求展开解释:\n" + input_text + "\n\n", self.current_tag)
            self.text_widget.config(state=tk.DISABLED)  # 恢复文本框为不可编辑状态

            self.agent.prompt_add(self.tasks['explain'] + input_text)
            reply = self.agent.prompt_post()
            self.know_reply = reply

            self.text_widget.config(state=tk.NORMAL)  # 使文本框可编辑
            self.text_widget.insert(tk.END, "来自助手的详细解释:\n" + reply + "\n\n", "assistant")
            self.text_widget.config(state=tk.DISABLED)  # 恢复文本框为不可编辑状态

    def start_work(self):
        print('start...')

        if platform.system() == "Linux":
            self.listener.start()

        try:
            self.window.mainloop()  # 运行GUI主循环
        except KeyboardInterrupt:
            print("Ctrl+C pressed. Exiting...")

    def get_selected_text(self):
        try:
            # Windows上使用剪贴板获取选中的文本
            if platform.system() == "Windows":
                selected_text = pyperclip.paste()
                return selected_text
            # 使用xsel命令获取鼠标当前选中的文本
            elif platform.system() == "Linux":
                selected_text = subprocess.check_output(['xsel', '-o'], universal_newlines=True).strip()
                return selected_text
            else:
                return None
        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    test_asis = assistant()
    try:
        test_asis.start_work()
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")
