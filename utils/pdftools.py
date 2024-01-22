import fitz
import re
from collections import Counter
from utils.filterwords import filter_words
from utils.ai.Gemini import Gemini

g = Gemini()

class PDF():
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = fitz.open(file_path)
        self.file_name = self.doc.metadata['title']
        self.text = self.get_text()
        self.chapters = self.get_chapters()
        self.problem_name = self.get_problem_name()
        self.descript = self.get_descript()
        self.word_frequency = self.get_word_frequency(20)

    def get_text(self):
        full_text = ''
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            full_text += text
        return full_text

    def get_word_frequency(self, n=None):
        text = self.text
        text = re.sub(r'[^\w\s]', '', text)  # 去除标点符号
        text = re.sub(r'\d+', '', text)  # 去除数字
        text = text.lower()  # 转换为小写
        words = text.split()
        stop_words = filter_words  # 过滤词
        words = [word for word in words if word not in stop_words]
        word_counts = Counter(words)
        return dict(word_counts.most_common()[:n]) if n else dict(word_counts.most_common())

    def get_chapters(self):
        chapters = {}
        # pattern = r'\n[A-Z]\w*[ ]\n'
        chapter_names = re.findall(r'\n[A-Z]\w*[ ]\n', self.text)
        for i in range(len(chapter_names)):
            chapter_text = self.text[self.text.index(chapter_names[i]):self.text.index(chapter_names[i+1])] if i != len(chapter_names)-1 else self.text[self.text.index(chapter_names[i]):]
            chapters[chapter_names[i][1:-2]] = chapter_text
        return chapters

    def get_problem_name(self):
        problem_name = re.findall(r'(?<=Problem [A-Z]: ).*?(?= \n)', self.text)
        return problem_name

    def get_descript(self):
        descript = {}
        while True:
            try:
                descript['full_text'] = g.text(self.text + 'Please summarize the content of the article in one sentence')
                break
            except:
                print('查询full_text失败，正在更换API并重新查询')
                g.change_api()
        for i in self.chapters:
            while True:
                try:
                    descript[i] = g.text(self.chapters[i] + f'Please summarize the Requirement of the {i} in few points')
                    break
                except:
                    print(f'查询{i}失败，正在更换API并重新查询')
                    g.change_api()
        return descript

    def export(self):
        pass
