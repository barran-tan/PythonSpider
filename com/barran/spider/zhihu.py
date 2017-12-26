# encoding=utf-8
from bs4 import BeautifulSoup
import requests
import time

__author__ = 'tanwei'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
    # 'Referer':'https://www.zhihu.com/',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'Origin':'https://www.zhihu.com'
}


def login(username, pwd, get_captcha):
    session = requests.session()
    _xsrf = BeautifulSoup(session.get('https://www.zhihu.com/#signin', headers=headers).content, "lxml").find('input', attrs={
    'name': '_xsrf'})['value']
    session.headers.update({'_xsrf': str(_xsrf)})

    captcha_content = session.get('http://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000),
                                  headers=headers).content
    data = {
        '_xsrf': _xsrf,
        'password': pwd,
        'captcha': get_captcha(captcha_content),
        # 'captcha_type': 'cn',
        'email': username,
    }
    print(data)
    resp = session.post('http://www.zhihu.com/login/email', data=data, headers=headers).content
    # 登录成功
    print('resp\n', resp)
    if b'\u767b\u5f55\u6210\u529f' in resp:
        print('login success')
    return session


def kill_captcha(content):
    with open('1.gif', 'wb') as fp:
        fp.write(content)
    return input('captcha : ')


if __name__ == '__main__':
    session = login('*********', '*********', kill_captcha)
    print(BeautifulSoup(session.get("https://www.zhihu.com", headers=headers).content, "lxml").find('span',
                                                                                            class_='name').getText())

    # print('\u767b\u5f55\u6210\u529f')