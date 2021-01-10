from bs4 import BeautifulSoup
import pandas as pd
import re
import login


class edu_admin(object):
    def __init__(self, accountant = r'学号（我怎么可能把我的给你看）', password = r'密码'):
        self.url = r'https://jxgl.hainanu.edu.cn'
        self.accountant = accountant
        self.password = password

    # 登录
    def login(self):
        self.sess = login.Login(self.url + '/jsxsd/framework/xsMain.jsp', self.accountant, self.password).login()

    # 解析成绩，返回成绩DataFrame和平均绩点
    def _parase_grade(self, html):
        df = pd.DataFrame(columns=['课程名称', '成绩'])

        for list in html.find_all('tr')[1:]:
            i = list.find_all('td')
            df = df.append({'课程名称': re.search(r'\S+', i[3].string).group(
                0), '成绩': re.search(r'\S+', i[4]('a')[0].string).group(0)}, ignore_index=True)

        grade_sum = re.search(r'\S+', html('body')
                              [0]('div')[0]('div')[0].string).group(0)

        return df, grade_sum

    # 获取成绩部分并处理
    def grade(self, date = r'2019-2020-1'):
        params = {'kksj': date}
        grade_list = self.sess.get(
            self.url + '/jsxsd/kscj/cjcx_list', params=params)
        bf = BeautifulSoup(grade_list.text, 'lxml')
        grade_df, grade_sum = self._parase_grade(bf)
        print(grade_df)
        print(grade_sum)


if __name__ == '__main__':
    my = edu_admin()
    my.login()
    my.grade()
