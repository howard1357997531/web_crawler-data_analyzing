from bs4 import BeautifulSoup
import json
import requests


def get_soup(url):
    try:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'lxml')  # 要pip install lxml
            return soup
    except Exception as e:
        print(e)
    return None


def get_ibon_data(api_url, country):
    form_data = {
        'strTargetField': 'COUNTY',
        'strKeyWords': country,
    }
    resp = requests.post(api_url, data=form_data)
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup


def get_railway_data(api_url, startStation, endStation, rideDate, startTime, endTime):
    soup = get_soup('https://www.railway.gov.tw/tra-tip-web/tip')
    csrf = soup.find(id="queryForm").find(
        'input', {'name': '_csrf'}).get('value')
    form_data = {
        '_csrf': csrf,
        'startStation': startStation,
        'endStation': endStation,
        'transfer': 'ONE',
        'rideDate': rideDate,
        'startOrEndTime': 'true',
        'startTime': startTime,
        'endTime': endTime,
        'trainTypeList': 'ALL',
        '_isQryEarlyBirdTrn': 'on',
        'query': '查詢',
    }

    resp = requests.post(api_url, data=form_data)
    soup = BeautifulSoup(resp.text, 'lxml')
    return soup


def get_data(x, y, num1, num2, a1=None):
    resp = get_soup(
        'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4051&limited=TWN')
    soup = json.loads(BeautifulSoup(resp.text, 'lxml').find('p').text.strip())
    datas = [{x: i[num1], y:int(i[num2])} for i in soup]
    if a1:
        a1.put(datas)
    return datas

def get_7days_data(x, y, num1, num2, b1=None):
    resp = get_soup(
        'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4051&limited=TWN')
    soup = json.loads(BeautifulSoup(resp.text, 'lxml').find('p').text.strip())
    datas_7 = [{x: i[num1], y:float(i[num2])} for i in soup]
    if b1:
        b1.put(datas_7)
    return datas_7


def get_country_data(x, y, num1, num2, c1=None, c2=None, c3=None, c4=None, c5=None):
    resp = get_soup(
        'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4049')
    soup = json.loads(BeautifulSoup(resp.text, 'lxml').find('p').text.strip())
    country = [{x: i[num1], y:int(float(i[num2]))} for i in soup]
    country.sort(key=lambda x: x.get(y), reverse=True)
    if c1:
        c1.put(country[1:16])
    if c2:
        c2.put(country[1:16])
    if c3:
        c3.put(country[1:16])
    if c4:
        c4.put(country[1:16])
    if c5:
        c5.put(country[1:16])
    return country[1:16]


def get_sick_data(num, d1=None, d2=None, d3=None, d4=None, d5=None, d6=None):
    resp = get_soup(
        'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4004')
    soup = json.loads(BeautifulSoup(resp.text, 'lxml').find('p').text.strip())
    datas = [i[num] for i in soup]
    if d1:
        d1.put(datas)
    if d2:
        d2.put(datas)
    if d3:
        d3.put(datas)
    if d4:
        d4.put(datas)
    if d5:
        d5.put(datas)
    if d6:
        d6.put(datas)
    return datas


def get_death_data(num, e1=None, e2=None, e3=None, e4=None):
    resp = get_soup(
        'https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4002')
    soup = json.loads(BeautifulSoup(resp.text, 'lxml').find('p').text.strip())
    datas = [i[num] for i in soup]
    if e1:
        e1.put(datas)
    if e2:
        e2.put(datas)
    if e3:
        e3.put(datas)
    if e4:
        e4.put(datas)
    return datas


def get_score_rank(datas):  # 各科分數排名
    subjects = ['chinese', 'english', 'math', 'society', 'science']
    for subject in subjects:
        datas.sort(key=lambda x: x.get(subject), reverse=True)

        current_score = 101
        current_index = 0

        for index, data in enumerate(datas, start=1):
            if data[subject] < current_score:
                current_index = index
            current_score = data[subject]
            data[subject] = current_index
    return datas
