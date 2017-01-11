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

cookie = None

conf = None
with open('wxappunion.json') as f:
    conf = json.load(f)


def md5pwd(pwd):
    m = hashlib.md5()
    m.update(pwd)
    return m.hexdigest()


def genHeaders(headers={}):
    headers["User-Agent"] = random.choice(conf['userAgents'])
    headers["Origin"] = conf['wxappunion']['host']
    if not cookie == None:
        headers['Cookie'] = cookie
    return headers


def getFormHash():
    url = 'http://www.wxapp-union.com/member.php?mod=logging&action=login'
    res = requests.get(url, headers=genHeaders())
    if res.status_code == 200:
        html = BeautifulSoup(res.content, 'html.parser')
        formHash = html.find('input', {'name': 'formhash'})
        loginUrl = html.find('form', {'name': 'login'})
        return (formHash['value'], conf['wxappunion']['host'] + loginUrl['action'])
    else:
        return None


def getCookie(id, pwd):
    formhash, loginurl = getFormHash()
    if not formhash == None:
        res = requests.post(loginurl,
                            headers=genHeaders({
                                'Content-Type': 'application/x-www-form-urlencoded'
                            }),
                            data='formhash={}&referer=http%3A%2F%2Fwww.wxapp-union.com%2Fhome.php%3Fmod%3Dspacecp&username={}&password={}&questionid=0&answer='.format(
                                formhash, urllib.quote(id), md5pwd(pwd)))
        if res.status_code == 200:
            cookieValues = ['{}={}'.format(c.name, c.value) for c in res.cookies]
            return ';'.join(cookieValues)
        else:
            print 'login fail'


def connect():
    global cookie
    account = random.choice(conf['wxappunion']['users'])
    print('connecting with {} / {}'.format(account['id'].encode('utf-8'), account['pwd']))
    cookie = getCookie(account['id'].encode('utf-8'), account['pwd'])
    print('connected')


def getArtical(id):
    url = 'http://www.wxapp-union.com/forum.php?mod=viewthread&tid={}'.format(id)
    res = requests.get(url, headers=genHeaders())
    if res.status_code == 200:
        return res.content
    else:
        return None


def getCommentUrl(tid):
    html = BeautifulSoup(getArtical(tid), 'html.parser')
    links = html.find_all("a")
    result = {
        'commentUrl': '',
        'formHash': ''
    }
    for link in links:
        if hasattr(link, 'href'):
            try:
                href = link['href']
                if 'action=reply' in href and 'page' not in href:
                    result['commentUrl'] = href
                if 'formhash' in href:
                    result['formHash'] = href[-8:]
            except:
                pass
    return result


def comment(tid, message='666666666666666'):
    commentUrl = getCommentUrl(tid)
    url = conf['wxappunion']['host'] + commentUrl[
        'commentUrl'] + '&extra=&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'
    res = requests.post(url,
                        data='message={}&posttime={}&formhash={}&usesig=1&subject=++'.format(message, time.mktime(
                            datetime.datetime.today().timetuple()), commentUrl['formHash']),
                        headers=genHeaders({
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Referer': 'http://www.wxapp-union.com/forum.php?mod=viewthread&tid={}'.format(tid)
                        }))
    if res.status_code == 200:
        print('comment success')
    else:
        print('comment fail')


def fetchAllArticleTitle(breakLimit=20):
    begin = 0
    nothingCount = 0
    titles = []
    while nothingCount < breakLimit:
        sys.stdout.write('\r fetch %s ' % (begin))
        cnt = getArtical(begin)
        if not cnt == None:
            html = BeautifulSoup(getArtical(begin), 'html.parser')
            begin += 1
            messagetext = html.find('div', {'id': 'messagetext'})
            if messagetext == None:
                title = html.find('span', {'id': 'thread_subject'})
                if not title == None:
                    titlestr = title.a.contents[0].encode('utf-8')
                    titles.extend([titlestr])
                    nothingCount = 0
            else:
                nothingCount += 1
                sys.stdout.write(' empty \n')
    with open('output/wxappunion-titles.txt', 'w+') as f:
        f.write('\n'.join(titles))


connect()
comment(1605)
# fetchAllArticleTitle()
