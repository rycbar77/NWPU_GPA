# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask, request, make_response, jsonify
from check import get_score
from flask_cors import CORS

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')


@app.route('/', methods=['POST'])
def getscore():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    courses = get_score(username, password)
    print(courses, file=sys.stderr)
    response = make_response(jsonify(courses), 200)
    # print(response)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
