import requests
import lxml
from bs4 import BeautifulSoup
import execjs
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
import pandas as pd
import re


class edu_admin(object):
    def __init__(self, accountant: str = r'学号（我怎么可能把我的给你看）', password: str = r'密码') -> None:
        self.sess = requests.session()
        self.url = 'http://jxgl.hainanu.edu.cn'
        self.sess.get(self.url + '/jsxsd/xk/null/logout')
        self.accountant = accountant
        self.password = password

    # 处理验证码图片
    def _image_handle(self, im: Image) -> Image:
        ls = [0 if i < 110 else 255 for i in range(256)]
        # 灰度处理
        im = im.convert('L')

        # 去除验证码四周黑框
        im = np.array(im)
        im[..., 0] = 255
        im[..., -1] = 255
        im[0, ...] = 255
        im[-1, ...] = 255
        im = Image.fromarray(im)

        # 二值化
        im = im.point(ls)
        # 高斯模糊
        im = im.filter(ImageFilter.GaussianBlur(0.6))
        # 二值化
        im = im.point(ls)
        return im

    # 获取验证码图片
    def _get_random_code(self, sess: requests.Session) -> str:
        img_content = sess.get(self.url + '/jsxsd/verifycode.servlet')
        img = Image.open(BytesIO(img_content.content))
        img = self._image_handle(img)
        img.show()
        code = input('请输入：')
        return code

    # 获取encoded值，执行某一js代码
    def _get_encoded(self, sess: requests.Session) -> str:
        with open('conwork.js') as f:
            js = execjs.compile(f.read())
            accountant = js.call('encodeInp', self.accountant)
            password = js.call('encodeInp', self.password)
        encoded = accountant + r"%%%" + password
        return encoded

    # 登录
    def login(self) -> None:
        data = {
            'encoded': self._get_encoded(self.sess),
            'RANDOMCODE': self._get_random_code(self.sess)
        }
        self.sess.post(self.url + '/jsxsd/xk/LoginToXk', data=data)

    # 解析成绩，返回成绩DataFrame和平均绩点
    def _parase_grade(self, html: BeautifulSoup) -> (pd.DataFrame, str):
        df = pd.DataFrame(columns=['课程名称', '成绩'])

        for list in html.find_all('tr')[1:]:
            i = list.find_all('td')
            df = df.append({'课程名称': re.search(r'\S+', i[3].string).group(
                0), '成绩': re.search(r'\S+', i[4]('a')[0].string).group(0)}, ignore_index=True)

        grade_sum = re.search(r'\S+', html('body')
                              [0]('div')[0]('div')[0].string).group(0)

        return df, grade_sum

    # 获取成绩部分并处理
    def grade(self, date: str = r'2019-2020-1') -> None:
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
