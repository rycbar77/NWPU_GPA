# -*- coding:gbk -*-
import random
from time import sleep

import requests
from bs4 import BeautifulSoup


# from fake_useragent import UserAgent


class Score(object):
    def __init__(self, regular, semi, experiment, final, total):
        self.regular = regular
        self.semi = semi
        self.experiment = experiment
        self.final = final
        self.total = total


class Course(object):
    def __init__(self, id, name, semester, credit, score):
        self.id = id
        self.name = name
        self.semester = semester
        self.credit = credit
        self.score = score


# ua = UserAgent()


def get_score(username, password):
    payload = {'username': username, 'password': password}
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
    s = requests.session()
    s.post('http://us.nwpu.edu.cn/eams/login.action', data=payload, headers=headers)
    sleep(0.2 + random.random())
    response = s.get('http://us.nwpu.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR',
                     headers=headers)
    response.encoding = 'utf-8'
    content = response.text
    # print(content)
    soup = BeautifulSoup(content, 'lxml')
    li = []
    courses = []
    for tbody in soup.find_all(name='tbody'):
        # print(tbody.attrs)
        tbody.attrs.setdefault('id', '')
        if tbody.attrs['id'] != '':
            for td in tbody.find_all(name='td'):
                # print(td)
                li.append(td)
                # print(len(li))
                if len(li) == 13:
                    # print(li[4].string)
                    # print(li[3].a.string)
                    tmp_score = [li[6].string, li[7].string,
                                 li[8].string, li[9].string, li[10].string]
                    tmp_score = [i.strip() if i else i for i in tmp_score]
                    course = Course(li[4].string.strip() if li[4].string else li[4].string,
                                    li[3].a.string.strip(
                                    ) if li[3].a.string else li[3].a.string,
                                    li[0].string.strip(
                                    ) if li[0].string else li[0].string,
                                    li[5].string.strip() if li[5].string else li[5].string,
                                    Score(
                                        li[6].string.strip(
                                        ) if li[6].string else li[6].string,
                                        li[7].string.strip(
                                        ) if li[7].string else li[7].string,
                                        li[8].string.strip(
                                        ) if li[8].string else li[8].string,
                                        li[9].string.strip(
                                        ) if li[9].string else li[9].string,
                                        li[10].string.strip(
                                        ) if li[10].string else li[10].string
                                    ))
                    courses.append(course)
                    li.clear()
        else:
            continue
    courses_info = {}
    for i in range(len(courses)):
        course = courses[i]
        course_info = {'name': course.name,
                       'semester': course.semester, 'credit': course.credit}
        score_info = {'regular': course.score.regular, 'semi': course.score.semi, 'experiment': course.score.experiment,
                      'final': course.score.final, 'total': course.score.total}
        course_info['score'] = score_info
        courses_info[i + 1] = course_info
    # print(courses_info)
    return courses_info


if __name__ == '__main__':
    get_score('', '')
