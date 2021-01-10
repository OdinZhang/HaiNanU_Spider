import requests
import encrypt
from bs4 import BeautifulSoup


class Login(object):
    def __init__(self, url, username, password) -> None:
        self.sess = requests.session()
        self.url = url
        self.username = username
        self.password = password
        self.authurl = r'https://authserver.hainanu.edu.cn/authserver/login'

    def _get_params(self):
        html = self.sess.get(self.authurl)
        html = BeautifulSoup(html.text, 'lxml')
        table = html.find(id='casLoginForm')
        ls = ['lt', 'dllt', 'execution', '_eventId']
        self.dict = {str: table.find('input', {'name': str})[
            'value'] for str in ls}
        self.pwdDefaultEncryptSalt = table.find(
            'input', {'id': 'pwdDefaultEncryptSalt'})['value']

    def _get_auth(self):
        self.sess.get(self.authurl + '/needCaptcha.html',
                      data={'username': self.username, 'pwdEncrypt2': 'pwdEncryptSalt'})
        self.dict['username'] = self.username
        self.dict['password'] = encrypt.encryptAES(
            self.password, self.pwdDefaultEncryptSalt)
        self.dict['rememberMe'] = 'on'
        self.sess.post(self.authurl, data=self.dict)

    def login(self):
        self._get_params()
        self._get_auth()
        self.sess.get(self.authurl, params={'service': self.url})
        return self.sess


if __name__ == '__main__':
    url = r'https://jxgl.hainanu.edu.cn'
    url_login = url + '/jsxsd/framework/xsMain.jsp'

    username = 20181682310040
    password = 'B50@38de39@5b6c3'

    sess = Login(url_login, username, password).login()
    t = sess.get(url_login)
    t = BeautifulSoup(t.text, 'lxml')
    r = sess.get(url + '/jsxsd/kscj/cjcx_list', params={'kksj': r'2019-2020-1'})
    html = BeautifulSoup(r.text, 'lxml')

    print(html)
