from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Max, Min, Avg, Sum
from .forms import StudentForm
from threading import Thread
from queue import Queue
from .utils import *
from .models import *
import time
import json
import re


def covid(request):  # 不能這樣寫 a,b=[Queue()]*2，Queue裡面會一樣
    # st=time.time() # a=<queue.Queue object at 0x0000022FF89E9688> b=<queue.Queue object at 0x0000022FF89E9688>
    a1, b1, c1, c2, c3, c4, c5 = Queue(), Queue(
    ), Queue(), Queue(), Queue(), Queue(), Queue()
    d1, d2, d3, d4, d5, d6, e1, e2, e3, e4 = Queue(), Queue(), Queue(
    ), Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue()
    threads = [
        Thread(target=get_data, args=(1, 2, 'a04', 'a06', a1)), Thread(
            target=get_7days_data, args=(1, 2, 'a04', 'a07', b1)),
        Thread(target=get_country_data, args=(1, 2, 'a03', 'a07', c1)), Thread(
            target=get_country_data, args=(3, 4, 'a03', 'a05', c2)),
        Thread(target=get_country_data, args=(5, 6, 'a03', 'a08', c3)), Thread(
            target=get_country_data, args=(7, 8, 'a03', 'a09', c4)),
        Thread(target=get_country_data, args=(9, 10, 'a03', 'a10', c5)),
        Thread(target=get_sick_data, args=('a06', d1)), Thread(
            target=get_sick_data, args=('a04', d2)),
        Thread(target=get_sick_data, args=('a07', d3)), Thread(
            target=get_sick_data, args=('a09', d4)),
        Thread(target=get_sick_data, args=('a11', d5)), Thread(
            target=get_sick_data, args=('a08', d6)),
        Thread(target=get_death_data, args=('a03', e1)), Thread(
            target=get_death_data, args=('a05', e2)),
        Thread(target=get_death_data, args=('a06', e3)), Thread(
            target=get_death_data, args=('a04', e4))
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # 台灣COVID-19每日新增確診
    datas = a1.get()
    datas_7 = b1.get()

    # 各國COVID-19 七日平均確診數
    cty_data1 = c1.get()
    cty_data2 = c2.get()
    cty_data3 = c3.get()
    cty_data4 = c4.get()
    cty_data5 = c5.get()

    country = []
    for i, data in enumerate(cty_data1):
        data.update(cty_data2[i])
        data.update(cty_data3[i])
        data.update(cty_data4[i])
        data.update(cty_data5[i])
        country.append(data)

    # 台灣COVID-19 疫情分項統計圖
    # Pie1
    sex = ['男', '女']
    data1 = d1.get()
    a = [data1.count('男'), data1.count('女')]

    # Pie2
    is_domestic = ['本國籍', '非本國籍']
    data2 = d2.get()
    data2 = [i for i in data2 if i != '']
    temp = []
    for i in data2:
        x = re.findall(r'本國籍', i)
        temp.extend(x)
    b = [temp.count('本國籍'), len(data2)-temp.count('本國籍')]

    # Stacked1
    data3 = d3.get()
    ages = ['10多歲', '20多歲', '30多歲', '40多歲', '50多歲', '60多歲']
    c = []
    c.append(data3.count('未滿5歲')+data3.count('未滿10歲'))
    for i in ages:
        c.append(data3.count(i))
    c.append(data3.count('70多歲')+data3.count('80多歲')+data3.count('90多歲'))
    age = ['未滿10歲', '10-20歲', '20-30多歲', '30-40多歲',
           '40-50多歲', '50-60多歲', '60-70多歲', '70歲以上']

    # Pie3
    data4 = d4.get()
    vax = ['已接種', '無', '調查中']
    d = [len(data4)-data4.count('x')-data4.count('無') -
         data4.count('調查中'), data4.count('無'), data4.count('調查中')]

    # Pie4
    data5 = d5.get()
    symptom = ['有症狀', '無', '調查中']
    data5 = [i for i in data5 if i != '']
    e = [len(data5)-data5.count('無症狀')-data5.count('調查中'),
         data5.count('無症狀'), data5.count('調查中')]

    # Pie5
    data6 = d6.get()
    infect = ['是', '否', '調查中']
    f = [data6.count('是'), data6.count('否'), data6.count('調查中')]

    # 台灣COVID-19 新增死亡個案表
    # Pie1
    data7 = e1.get()
    death_a = [data7.count('男'), data7.count('女')]
    print(data7)
    # Pie2
    data8 = e2.get()
    history = ['有慢性病史', '無']
    death_b = [len(data8)-data8.count('無慢性病史'), data8.count('無慢性病史')]

    # Stacke1
    data9 = e3.get()
    injection = ['無', '1劑', '2劑', '3劑', '4劑']
    death_c = [data9.count('無'), data9.count('1劑'), data9.count(
        '2劑'), data9.count('3劑'), data9.count('4劑')]

    # Stacke2
    data10 = e4.get()
    death_age = ['0-29歲', '30-49歲', '50-64歲', '65-74歲', '>75歲']
    temp_a = [i for i in data10 if 0 <= int(i) < 29]
    temp_b = [i for i in data10 if 30 <= int(i) < 49]
    temp_c = [i for i in data10 if 50 <= int(i) <= 64]
    temp_d = [i for i in data10 if 65 <= int(i) <= 74]
    temp_e = [i for i in data10 if 75 <= int(i)]
    death_d = [len(temp_a), len(temp_b), len(temp_c), len(temp_d), len(temp_e)]
    context = {'datas': datas, 'datas_7': datas_7, 'country': country, 'sex': sex, 'a': a, 'is_domestic': is_domestic, 'b': b,
               'age': age, 'c': c, 'vax': vax, 'd': d, 'symptom': symptom, 'e': e, 'infect': infect, 'f': f, 'death_a': death_a,
               'history': history, 'death_b': death_b, 'injection': injection, 'death_c': death_c, 'death_age': death_age, 'death_d': death_d}
    # print(time.time()-st)
    # 用 locals(所有變數都傳) 會慢4秒
    return render(request, 'data_analyzing/covid.html', context)


def student_grade(request):
    std_datas = Student.objects.all()
    std_count = Student.objects.count()
    boy_count = Student.objects.filter(sex='男').count()
    girl_count = Student.objects.filter(sex='女').count()

    # 全班各科及格率
    grades = list(Student.objects.values_list(
        'chinese', 'english', 'math', 'society', 'science'))
    chinese = len(list(filter(lambda x: x >= 60, [i[0] for i in grades])))
    english = len(list(filter(lambda x: x >= 60, [i[1] for i in grades])))
    math = len(list(filter(lambda x: x >= 60, [i[2] for i in grades])))
    society = len(list(filter(lambda x: x >= 60, [i[3] for i in grades])))
    science = len(list(filter(lambda x: x >= 60, [i[4] for i in grades])))
    score_pass = [chinese, english, math, society, science]
    score_fail = [len(grades)-chinese, len(grades)-english,
                  len(grades)-math, len(grades)-society, len(grades)-science]

    # 男女各科平均比較
    boyavg = Student.objects.filter(sex='男').aggregate(
        Avg('chinese'), Avg('english'), Avg('math'), Avg('society'), Avg('science'))
    boyavg = [round(value, 1) for key, value in boyavg.items()]
    girlavg = Student.objects.filter(sex='女').aggregate(
        Avg('chinese'), Avg('english'), Avg('math'), Avg('society'), Avg('science'))
    girlavg = [round(value, 1) for key, value in girlavg.items()]

    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_grade')
    else:
        form = StudentForm()
    return render(request, 'data_analyzing/student_grade.html', locals())


def get_grade(request):
    # 各科成績與全班各科平均比較
    avg = Student.objects.aggregate(Avg('chinese'), Avg(
        'english'), Avg('math'), Avg('society'), Avg('science'))
    avg_score = [round(j, 1) for i, j in avg.items()]
    std_name = request.GET.get('std_name').strip()
    total = {i[0]: i[1]
             for i in list(Student.objects.values_list('name', 'total_score'))}
    total = [i[0]
             for i in sorted(total.items(), key=lambda x:x[1], reverse=True)]
    all_name = [i['name'] for i in list(Student.objects.values('name'))]
    try:
        if std_name in all_name:
            statue = True
            std_scorelist = list(Student.objects.filter(name=std_name).values_list(
                'chinese', 'english', 'math', 'society', 'science'))
            # print(std_scorelist)   ex: [(80, 77, 85, 94, 62)]
            std_score = [i for i in std_scorelist[0]]
            std_avg = sum(std_score)/len(std_score)
            std_rank = total.index(std_name) + 1
    except Exception as e:
        statue = False

    # 各科班排
    std_allscore = Student.objects.values(
        'name', 'chinese', 'english', 'math', 'society', 'science')
    std_allscore = get_score_rank(list(std_allscore))
    for std in std_allscore:
        if std['name'] == std_name:
            score_rank = [value for i, value in enumerate(
                std.values()) if i > 0]
    num_of_std = Student.objects.count()
    score_rank2 = [num_of_std-i for i in score_rank]
    score_rank_title = [score_rank]
    print(std_scorelist)
    t = render_to_string(
        'data_analyzing/ajax/student_gradedata.html', locals())
    return JsonResponse({'data': t})


def get_rank(request):
    std_datas = list(Student.objects.values_list('name', 'code', 'sex', 'chinese',
                                                 'english', 'math', 'society', 'science', 'total_score', 'average_score'))
    std_datas = sorted(std_datas, key=lambda x: x[8], reverse=True)
    std_datas = [[j for j in i] for i in std_datas]
    current_score = 501
    current_index = 0
    for index, std in enumerate(std_datas, start=1):
        if std[8] < current_score:
            current_index = index
        std.insert(0, current_index)
        current_score = std[9]
    # print(std_datas)
    t = render_to_string(
        'data_analyzing/ajax/student_get_rank.html', {'std_datas': std_datas})
    return JsonResponse({'data': t})


def edit_grade(request):
    st_id = request.GET.get('st_id')
    student = Student.objects.get(id=int(st_id))
    form = StudentForm(instance=student)
    t = render_to_string('data_analyzing/ajax/edit_grade.html', locals())
    return JsonResponse({'data': t})


def save_grade(request, pk):
    student = Student.objects.get(id=pk)
    student.name = request.POST['name']
    student.code = request.POST['code']
    student.sex = request.POST['sex']
    # 這裡要加int(),不然 model 裡的 save 會 return 字串連接
    student.chinese = int(request.POST['chinese'])
    student.english = int(request.POST['english'])
    student.math = int(request.POST['math'])
    student.society = int(request.POST['society'])
    student.science = int(request.POST['science'])
    student.save()
    return JsonResponse({'bool': True})


def delete_grade(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
    return JsonResponse({'bool': True})
