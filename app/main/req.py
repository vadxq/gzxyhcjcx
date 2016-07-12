# coding: utf-8

from bs4 import BeautifulSoup
import requests


def get_html(code, sfzh):
    url = "http://gkcf.jxedu.gov.cn/cjcx/LqQuerySelvet"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = 'dmlx=0&va=00000000&year=1636&ct=1&code=+{}&sfzh={}' \
        '&yzm=000000&action.x=00&action.y=00'.format(code, sfzh)
    resp = requests.post(url, headers=headers, data=data, timeout=4)
    return resp.content


def parse_html(html):
    # print html
    info_list = []
    soup = BeautifulSoup(html, 'html.parser')
    td = soup.find_all('td')
    validate = u'考生姓名' in soup.find('table',id='dlt',height='100%').get_text()
    if not validate:
        info_list = ['login fail']
    table = soup.find('table', id='dlt', height=60)
    for td in table.find_all('tr'):
        for tt in td.find_all('td'):
            ss = tt.string.strip().split(u'：')
            info_list.append(ss[-1].strip(' '))
    return info_list


def return_info(info_list):
    info = {'status': 1}
    if u'暂无录取信息' in info_list:
        info['data'] = {}
        info['message'] = u'暂无录取信息'
    elif len(info_list) == 11:
        info['data'] = {
            'name': info_list[0],
            'lqzt': info_list[1],
            'ksh': info_list[2],
            'zkzh': info_list[3],
            'jhxzmc': info_list[4],
            'lqzy': info_list[5],
            'lqpc': info_list[6],
            'lqkl': info_list[7],
            'lqsj': info_list[8],
            'jxdh': info_list[9],
            'lqyx': info_list[10]
        }
        info['message'] = u'获取录取信息成功'
    elif 'timeout' in info_list:
        info['data'] = {}
        info['message'] = u'timeout'
        info['status'] = 0
    elif 'login fail' in info_list:
        info['status'] = 0
        info['data'] = {}
        info['message'] = u'考生号和身份证号不匹配'
    else:
        info['status'] = 0
        info['data'] = {}
        info['message'] = u'获取录取信息失败'
    return info


def get_info(code, sfzh):
    try:
        html = get_html(code, sfzh)
        info_list = parse_html(html.decode('gbk'))
    except requests.exceptions.Timeout:
        info_list = ['timeout']
    except Exception:
        info_list = ['connect error']
    info = return_info(info_list)
    return info
