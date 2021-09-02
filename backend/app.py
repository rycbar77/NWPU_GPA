# -*- coding: utf-8 -*-
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

from flask import Flask, request
from check import get_score

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['POST'])
def getscore():
    username = request.form['username']
    password = request.form['password']
    courses = get_score(username, password)
    # print(courses)
    return courses


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5590)
