import google.generativeai as genai
import PIL.Image
from io import BytesIO
import base64
from random import choice
import os

HTTP_PROXY = 'http://localhost:7890'

GEMINI_API_KEY = ['AIzaSyBf1eFP8q-tl7z1lpioS14jHYHA9MONIKU', 'AIzaSyCd5RueqsN7QzvcBGFlnqDthTQOnVkU6A0',
                  'AIzaSyB6nalkyK1cWISBPoD2147mC4O5vik-6yg', 'AIzaSyA5GJGE88MvEAGzgHZTgM5Ly1w1ofT5D1o',
                  'AIzaSyAt1L9q4SMxs_44SDn8nWw0u6TokvhHUhc']

# 模型设置
GENERATION_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 3000,
}

SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

def bs64_to_PIL(data):
    return PIL.Image.open(BytesIO(base64.b64decode(data.split(',')[1])))

def history_factory(question):
    history_dictionary = [{
        'role': 'user',
        'parts': 'You are now a professional analyst, and you are very good at summarizing and summarizing the content in the document'
    }, {
        'role': 'model',
        'parts': 'OK'
    }, {
        'role': 'user',
        'parts': 'and just reply to me with the one sentence you need, no need to reply to other words'
    }, {
        'role': 'model',
        'parts': 'OK'
    }, {
        'role': 'user',
        'parts': question
    }]
    return history_dictionary


class Gemini():
    # 初始化模型
    def __init__(self):
        os.environ["http_proxy"] = HTTP_PROXY
        os.environ["https_proxy"] = HTTP_PROXY
        self.api = choice(GEMINI_API_KEY)
        genai.configure(api_key=self.api)
        try:
            self.model_pro = genai.GenerativeModel('gemini-pro', safety_settings={'HARASSMENT': 'block_none'})
            self.model_vision = genai.GenerativeModel('gemini-pro-vision')
            print("Gemini Connect Successfully!")
        except:
            print("Can't connect to Gemini Please check your Proxy and API Key!!!")
    # 文字处理
    def text(self, question):
        history_processed = history_factory(question)
        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=GENERATION_CONFIG,
                                      safety_settings=SAFETY_SETTINGS)
        response = model.generate_content(history_processed)
        result = response.text
        return result
    # 图片处理
    def version(self, question, imgs):
        model = genai.GenerativeModel('gemini-pro-vision')
        true_question = [question]
        for img in imgs:
            true_question.append(bs64_to_PIL(img))
        response = model.generate_content(true_question, stream=True)
        response.resolve()
        return response.text

    def change_api(self):
        filtered_api = [api for api in GEMINI_API_KEY if api != self.api]
        self.api = choice(filtered_api)
        genai.configure(api_key=self.api)
        try:
            self.model_pro = genai.GenerativeModel('gemini-pro', safety_settings={'HARASSMENT': 'block_none'})
            self.model_vision = genai.GenerativeModel('gemini-pro-vision')
            print("Gemini Connect Successfully!")
        except:
            print("Can't connect to Gemini Please check your Proxy and API Key!!!")

if __name__ == '__main__':
    m = Gemini()
    print(m.text('what you can do'))
