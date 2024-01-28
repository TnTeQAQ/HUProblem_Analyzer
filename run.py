import os
from flask import Flask, render_template, jsonify, request
from utils.pdftools import pdf_scan

app = Flask(__name__, static_folder=os.getcwd()+'/static')

pdf_names = []
pdfs = {}

@app.before_first_request
def setup():
    try:
        global pdf_names, pdfs
        pdf_names, pdfs = pdf_scan()
        print('初始化成功')
    except:
        print('初始化出错')

@app.route('/', methods=['GET', 'POST'])
@app.route('/<pdf_name>', methods=['GET', 'POST'])
def index(pdf_name=''):
    # print(pdf_name)
    if pdf_name != '':
        try:
            global pdfs
            pdf = pdfs[pdf_name]
        except:
            return '路径出错'
        return render_template('pdf.html', pdf_names=pdf_names, pdf=pdf)
    return render_template('index.html', pdf_names=pdf_names)

if __name__ == '__main__':
    app.run(port='5000', host='127.0.0.1', debug=True)


