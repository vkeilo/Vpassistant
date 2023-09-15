import subprocess
from pynput import keyboard
from agent_use import gpt_agent
import platform
import pyperclip


class assistant():
    
    def __init__(self):
        self.agent = gpt_agent('chatglm2-6b')
        self.agent.init_messages_by_json('assistant.json')
        self.tasks = {'translate':"翻译以下内容:\n",'explain':"介绍或者解释以下内容：\n"}
        self.know_reply = None
        # self.listener = keyboard.GlobalHotKeys({
        #     '<ctrl>+<alt>+1': self.run_task('translate'),
        #     '<ctrl>+<alt>+2': self.run_task('explain')
        # })
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+1': self.run_translate,
            '<ctrl>+<alt>+2': self.run_explain
        })

    def run_translate(self):
        self.agent.prompt_add(self.tasks['translate'] + self.get_selected_text())
        reply = self.agent.prompt_post()
        self.know_reply =  reply
        self.show_reply()
    
    def run_explain(self):
        self.agent.prompt_add(self.tasks['explain'] + self.get_selected_text())
        reply = self.agent.prompt_post()
        self.know_reply =  reply
        self.show_reply()

    def show_reply(self):
        print(self.know_reply)

    def start_work(self):
        print('start...')
        self.listener.start()
        # self.listener.join()

    # def get_selected_text(self):
    #     try:
    #         # 使用xsel命令获取鼠标当前选中的文本
    #         selected_text = subprocess.check_output(['xsel', '-o'], universal_newlines=True).strip()
    #         print(selected_text)
    #         return selected_text
    #     except subprocess.CalledProcessError:
    #         return None

    def get_selected_text(self):
        try:
            if platform.system() == 'Linux':
                # 在Linux上使用xsel命令获取鼠标当前选中的文本
                selected_text = subprocess.check_output(['xsel', '-o'], universal_newlines=True).strip()
                print(selected_text)
                return selected_text
            elif platform.system() == 'Windows':
                # 在Windows上使用pyperclip库获取剪贴板文本
                selected_text = pyperclip.paste()
                print(selected_text)
                return selected_text
            else:
                # 在其他操作系统上可能不支持此功能
                return None
        except subprocess.CalledProcessError:
            return None




if __name__ == "__main__":
    test_asis = assistant()
    try:
        test_asis.start_work()
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")


