import requests

url = 'https://laplace.live:443/api/ai-chat'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://laplace.live/ai-chat",
    "Content-Type": "application/json",
    "Origin": "https://laplace.live",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Te": "trailers"
}

def history_factory(question):
    history_dictionary = {
        'text': question,
        'context': [
            {
                'role': 'user',
                'content': 'You are now a professional analyst, and you are very good at summarizing and summarizing the content in the document,and just reply to me with the one sentence you need, no need to reply to other words'
            },
            {
                'role': 'system',
                'content': 'OK'
            }
        ],
        'type': 'askQuestion',
        'model': 'gpt-4-turbo-preview',
        'lang': 'Simplified Chinese',
        'custom_api': ''
    }
    return history_dictionary


class Gpt4Turbo():
    # 初始化模型
    def __init__(self):
        try:
            requests.post(url=url, headers=headers)
            print("Gpt4-turbo Connect Successfully!")
        except:
            print("Can't connect to Gpt4-turbo!!!")
    # 文字处理
    def text(self, question):
        history_processed = history_factory(question)
        response = requests.post(url=url, headers=headers, json=history_processed)
        result = response.text
        return result

if __name__ == '__main__':
    req = Gpt4Turbo()
    print(req.text(''))

