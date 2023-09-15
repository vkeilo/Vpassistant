import openai
import json

class gpt_agent():
    def __init__(self,model_name,key="none"):
        self.model = model_name
        self.messages = []
        self.origin_memery = []
        openai.api_key = key
        if model_name == "chatglm2-6b":
            openai.api_base = "http://localhost:8000/v1"
    
    # 角色回滚
    def init_role(self):
        self.messages = self.origin_memery.copy()

    # 根据目标json对话中的内容进行角色扮演
    def init_messages_by_json(self,json_path):
        with open(json_path, 'r',encoding='utf-8') as json_file:
            data = json.load(json_file)
        self.messages = data["dialogues"]
        self.origin_memery = self.messages.copy()

    # 在对话历史中额外增加一句
    def history_add_one(self,role,text):
        self.messages.append({"role":role, "content": text})   
         

    # 根据一段文本描述进行角色扮演
    def init_messages_by_roleplay(self,task):
        self.messages=None
        self.history_add_one("user",task)
        self.origin_memery = self.messages.copy()

    # 用户发问/出题    
    def prompt_add(self,text):
        self.history_add_one("user",text)

    # 获取回答，并更新对话历史    
    def prompt_post(self,T = 0,maxtokens = 200):
        # 调用API进行对话生成
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            max_tokens=maxtokens,
            temperature=T
        )
        # 提取生成的回复文本
        reply = response.choices[0].message.content
        self.history_add_one("assistant", reply)
        return reply