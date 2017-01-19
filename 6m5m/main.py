# -*- coding: UTF-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import bs4
import datetime, time
import hashlib
import json
import random
import urllib
import sys


def buildFormData():
    print('begin build form data ...')
    loginUrl = "http://www.6m5m.com/login.html"
    res = requests.get(loginUrl, headers={
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"
    })
    if res.status_code == 200:
        html = BeautifulSoup(res.content, 'html.parser')
        formhash = html.find('input', {'name': 'formhash'})['value']
        hdn_refer = html.find('input', {'name': 'hdn_refer'})['value']
        handlekey = html.find('input', {'name': 'handlekey'})['value']
        txt_account = 'm860'
        pwd_password = urllib.quote('abcd@123')
        txt_password = urllib.quote('密码不可以为空')
        return 'formhash={}&hdn_refer={}&handlekey={}&txt_account={}&txt_password={}&pwd_password={}'.format(
            formhash, hdn_refer, handlekey, txt_account, txt_password, pwd_password
        )
    print('build form data fail')
    return None


def getToken():
    url = 'http://www.6m5m.com/index.php?do=login&inajax=1'
    formData = buildFormData()
    print(formData)
    if formData:
        res = requests.post(url, data=formData, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7'
        })
        if res.status_code == 200:
            print(res.content)
            cookieValues = ['{}={}'.format(c.name, c.value) for c in res.cookies]
            cookies=';'.join(cookieValues)
            print(cookies)
            return cookies
    return None

def sign():
    url='http://www.6m5m.com/index.php?do=user_sign'
    cookies=getToken()
    if cookies:
        res=requests.post(url,headers={
            'Cookie':cookies,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7'
        },data='action=sign&ac_id=')
        if res.status_code==200:
            print(res.content)

sign()