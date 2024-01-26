import fitz
import re
from collections import Counter
from utils.filterwords import filter_words
from utils.ai.Gemini import Gemini
# from filterwords import filter_words
# from ai.Gemini import Gemini
import pandas as pd
import os

g = Gemini()

class PDF():
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
        self.doc = fitz.open(file_path+'/'+file_name)
        self.text = self.get_text()
        self.chapters = self.get_chapters()
        self.problem_name = self.get_problem_name()
        self.descripts = self.get_descripts()
        self.word_frequency = self.get_word_frequency(20)
        self.attachment = self.get_attachment()

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
        return problem_name[0]

    def get_descripts(self):
        err_n = 0
        descripts = {}
        while True:
            try:
                descripts['full_text'] = g.text(self.text + 'Please summarize the content of the article in one sentence')
                print(f'{self.file_name}的full_text查询成功')
                err_n = 0
                break
            except:
                err_n += 1
                if err_n == 3:
                    descripts['full_text'] = 'error!'
                    err_n = 0
                    print(f'查询full_text失败')
                    break
                print('查询full_text失败，正在更换API并重新查询')
                g.change_api()
        for i in self.chapters:
            while True:
                try:
                    descripts[i] = g.text(self.chapters[i] + f'Please summarize the content of the article in few points')
                    print(f'{self.file_name}的{i}查询成功')
                    err_n = 0
                    break
                except:
                    err_n += 1
                    if err_n == 3:
                        descripts[i] = 'error!'
                        err_n = 0
                        print(f'查询{i}失败!')
                        break
                    print(f'查询{i}失败，正在更换API并重新查询')
                    g.change_api()
        return descripts

    def export(self):
        df = pd.DataFrame()
        df['problem_name'] = self.problem_name
        for k, v in self.descripts.items():
            df[f'descripts_{k}'] = v
        df['word_frequency'] = ' '.join([k for k in self.word_frequency])
        df.T.to_excel(f'results/{self.file_name}.xlsx', index=True)

    def get_attachment(self):
        return [i for i in os.listdir(self.file_path) if '.pdf' not in i and '.' in i]

def pdf_scan(pdf_path='pdf'):
    pdfs = {}
    pdf_names = []
    for file_path, _, k in os.walk(pdf_path):
        print(file_path)
        for file_name in k:
            if '.pdf' in file_name:
                t = PDF(file_path, file_name)
                pdf_names.append(file_name)
                pdfs[file_name] = t
                t.export()
    return pdf_names, pdfs


if __name__ == '__main__':
    p = PDF('../pdf/2023_MCM_Problem_A.pdf')
    p.export()

