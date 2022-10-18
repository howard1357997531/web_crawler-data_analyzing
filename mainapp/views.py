from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Max, Min, Avg, Sum
from bs4 import BeautifulSoup
from .forms import StudentForm
from threading import Thread
from queue import Queue
from .utils import *
from .models import *
import time
import requests
import json
import re


def home(request):
    return render(request, 'home.html', locals())


def apple_news(request):
    url = 'https://tw.appledaily.com/realtime/recommend/'
    soup = get_soup(url)
    link = soup.find_all('div', class_='flex-feature')
    datas = [[i.find('img').get('data-src'), i.find('a').text.strip(),
              i.find('a').get('href')] for i in link]
    return render(request, 'web_crawler/apple_news.html', locals())


def get_url(request):
    url = 'https://tw.appledaily.com/realtime/' + request.GET.get('url')
    # print(url)
    soup = get_soup(url)
    link = soup.find_all('div', class_='flex-feature')
    datas = [[i.find('img').get('data-src'), i.find('a').text.strip(),
              i.find('a').get('href')] for i in link]
    t = render_to_string('web_crawler/ajax/apple_news.html', {'datas': datas})
    return JsonResponse({'datas': t})


def yahoo_movie(request):
    url = 'https://movies.yahoo.com.tw/chart.html'
    soup = get_soup(url)
    movie = soup.find('div', class_='rank_list table rankstyle1').find_all(
        'div', class_='tr')
    datas = []
    for tr in movie[1:]:
        data = []
        for i, td in enumerate(tr.find_all('div', class_='td')):
            if i == 1:
                continue
            elif i == 3:
                if td.find('a'):
                    data.extend([td.text.strip(), td.find('a').get('href')])
                    soup2 = get_soup(td.find('a').get('href'))
                    movie_img = soup2.find('div', class_='table').find(
                        'div', class_='movie_intro_foto')
                    movie_detail = soup2.find('div', class_='table').find(
                        'div', class_='movie_intro_info_r')
                    data.append(movie_img.find('img').get('src'))
                    data.append([i.text.strip()
                                for i in movie_detail.find_all('span')])
                else:
                    title = td.find('div', class_='rank_txt').text.strip()
                    data.extend([title, '', '', ''])
            elif i == 5:
                if td.find('a'):
                    data.append(td.find('a').get('href')
                                if td.find('a') else None)
                else:
                    data.append('')
            else:
                data.append(td.text.strip())
        datas.append(data)
    return render(request, 'web_crawler/yahoo_movie.html', {'datas': datas})


def ibon(request):
    url = 'https://www.ibon.com.tw/retail_inquiry.aspx#gsc.tab=0'
    api_url = 'https://www.ibon.com.tw/retail_inquiry_ajax.aspx'
    city = get_soup(url).find('select', id='Class1').find_all('option')
    citys = [i.text.strip() for i in city]
    country = '台北市'
    soup = get_ibon_data(api_url, country)
    table = soup.find('table', class_='font16').find_all('tr')
    titles = []
    datas = []
    for i, tr in enumerate(table):
        if i == 0:
            title = [i.text.strip() for i in tr.find_all('td')]
            titles.extend(title)
        else:
            content = [i.text.strip() for i in tr.find_all('td')]
            datas.append(content)
    return render(request, 'web_crawler/ibon.html', locals())


def get_city(request):
    api_url = 'https://www.ibon.com.tw/retail_inquiry_ajax.aspx'
    city = request.GET['city']
    soup = get_ibon_data(api_url, city)
    table = soup.find('table', class_='font16').find_all('tr')
    titles = []
    datas = []
    for i, tr in enumerate(table):
        if i == 0:
            title = [i.text.strip() for i in tr.find_all('td')]
            titles.extend(title)
        else:
            content = [i.text.strip() for i in tr.find_all('td')]
            datas.append(content)
    t = render_to_string('web_crawler/ajax/ibon_table.html',
                         {'datas': datas, 'titles': titles})
    return JsonResponse({'data': t})


def taiwan_railway(request):
    url = 'https://www.railway.gov.tw/tra-tip-web/tip'
    api_url = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime'
    times = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
             '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30', '23:59']
    endtimes = times[:-1]
    sta = get_soup(url).find('div', id='cityHot')
    stations = {btn.text.strip(): btn.get('title')
                for btn in sta.find_all('button')}

    return render(request, 'web_crawler/taiwan_railway.html', locals())


def get_taiwan_railway_data(request):
    api_url = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime'
    start_station = request.GET['start_station']
    end_station = request.GET['end_station']
    date = request.GET['date'].replace('-', '/')
    start_time = request.GET['start_time']
    end_time = request.GET['end_time']

    try:
        soup = get_railway_data(api_url, start_station,
                                end_station, date, start_time, end_time)
        trs = soup.find(
            'div', class_='search-trip').find('table').find_all('tr', class_='trip-column')
        titles = ['車種車次 (始發站 → 終點站)', '出發時間', '抵達時間', '行駛時間',
                  '經由', '全票', '孩童票', '敬老票', '是否有票']
        datas = []
        for tr in trs[1:]:    # trs[1] = '1' 這樣會error,要trs[1:2] = ['1'] ,因 tr.find_all() tr不能為字串，要為list
            data = []
            for j, td in enumerate(tr.find_all('td')):
                if j == 0:
                    data.extend([td.find('a').get('href'), td.text.strip()])
                elif j == 5:
                    continue
                else:
                    data.append(td.text.strip())
            datas.append(data)
    except Exception as e:
        text = '查無資料'
    t = render_to_string('web_crawler/ajax/taiwan_railway.html', locals())
    return JsonResponse({'data': t})
