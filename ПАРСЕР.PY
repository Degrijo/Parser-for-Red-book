import requests
from bs4 import BeautifulSoup
import re
from time import sleep

def get_html(url, useragent=None, proxy=None):
    print('get_html')
    r = requests.get(url, headers=useragent, proxies=proxy, cookies={'serverPW': '40ba9118730170106e6a8a2f0e316c88a2c55c2c6a4456e3979e2e3b7babce01a%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22serverPW%22%3Bi%3A1%3BN%3B%7D'})
    return r.text   

def get_and_set_data(html, year, temp_length_stem, temp_length_inf, districts, parts, template = template.read()): 
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('td', valign = 'top', style = 'padding-left:10px').text.strip().lower()
        names = []
        names.append(re.search(r'^[а-я, ,.,(,),,,=]+', name).group())
        name = name[re.search('^[а-я, ,.,(,),,,=]+', name).end():]
        names.append(re.search(r'[a-z, ,.,,,(,),=]+', name).group())
        name = name[re.search(r'[a-z, ,.,,,(,),=]+', name).end():]
        names.append(name)
        del name
        idtf = re.sub(' ', '_', names[1])
        print('get_pict')
        a = soup.find('img', style="border:1px solid #dedede;")['src']
        r = requests.get('http://redbook.minpriroda.gov.by'+a)
        open(idtf+'.jpg', 'wb').write(r.content)
        sec_cat = soup.find('a', href="/hints/cats.html", onclick='return _help("cats");', target="_blank").text
        paragraphs = soup.find_all('p')[6:8] +[soup.find_all('p')[9]] + soup.find_all('p')[11:16]
        paragraphs = [i.text.strip() for i in paragraphs]
        for i in range(len(paragraphs)):
            paragraphs[i] = re.sub("\n", '', paragraphs[i])
            paragraphs[i] = re.sub(':', ': ', paragraphs[i])
        template = re.sub("temp_idtf", idtf, template)
        template = re.sub("temp_name_ru", names[0], template)
        template = re.sub("temp_name_lat", names[1], template)
        template = re.sub("temp_name_bel", names[2], template)
        for i in range(len(paragraphs)):
            template = re.sub('temp_paragraph_'+str(i), paragraphs[i], template)
        for i in range(2):
            template = re.sub("temp_length_stem["+str(i)+"]", temp_length_stem[i], template)
            template = re.sub("temp_length_inf["+str(i)+"]", temp_length_inf[i], template)
        if len(districts) == 0:
            template = re.sub("temp_distr", "Republic_of_Belarus", template)
        else:
            template = re.sub("temp_distr", ';;->'.join(districs)+'_district', template)
        for part in range(len(parts)):  # должно быть 6
            if len(part[i]) == 0:
                template = re.sub("temp_part"+'['+str(i)+'];', '', template)
            else:
                template = re.sub("temp_part"+'['+str(i)+']', ';'.join(districs), template)
        template = re.sub("temp_year", year, template)
        template = re.sub("temp_pop", pop, template)
        file = open("concept_" + idtf + '.scs', 'w', encoding='utf-8')
        file.write(template)
        file.close()
        print('done')
    except:
        print('error')
    

template = open("template.scs", encoding='utf-8')
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=38'), '1981', ['40','60'], ['1,5', '2'], ['Витебский', 'Городокский', 'Лепельский', 'Лиозненский', 'Дятловский', 'Ивьевский', 'Ошмянский', 'Свислочский', 'Щучинский', 'Березовский', 'Брестский', 'Ганцевичский', 'Ивановский', 'Ивацевичский', 'Кобринский', 'Лунинецкий', 'Ляховичский', 'Малоритский', 'Пинский', 'Пружанский', 'Столинский', 'Житковичский', 'Калинковичский', 'Мозырский', 'Октябрьский', 'Светлогорский', 'Речицкий', 'Хойникский', 'Борисовский', 'Воложинский', 'Любанский', 'Пуховичский', 'Слуцкий', 'Стародорожский', 'Столбцовский', 'Узденский', 'Белыничский', 'Бобруйский', 'Кировский', 'Кличевский', 'Костюковичский', 'Осиповичский', 'Чериковский', 'Горецкий', 'Беловежская пуща', 'Гродненский', 'Мозырьский', 'Пинский', 'Ивановский', 'Светлогорский', 'Осиповичский', 'Хойникский', 'Могилевский'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=39'), '1981', ['100','120'], ['5', '10'], ['Борисовский', 'Вилейский', 'Воложинский', 'Логойский', 'Любанский', 'Минский', 'Мядельский', 'Солигорский', 'Бешенковичский', 'Витебский', 'Городокский', 'Докшицкий', 'Лиозненский', 'Оршанский', 'Сенненский', 'Ивацевичский', 'Столинский', 'Гродненский', 'Беловежская пуща', 'Могилевский', 'Горецкий'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=40'), '1993', ['30','80'], ['3,4', '7,2'], ['Брестский', 'Ивацевичский', 'Кобринский', 'Малоритский', 'Столинский', 'Браславский', 'Докшицкий', 'Лепельский', 'Лиозненский', 'Россонский', 'Шумилинский', 'Борисовский', 'Вилейский', 'Воложинский', 'Крупский', 'Минский', 'Мядельский', 'Калинковичский', 'Мозырский', 'Бобруйский', 'Кировский', 'Кличевский', 'Гродненский', 'Туровский', 'Жлобинский', 'Глусский', 'Кличевский', 'Лельчицкий'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=41'), '2006', ['10','30'], ['0,3', '0,6'], ['Столинский', 'Верхнедвинский', 'Витебский', 'Глубокский', 'Городокский', 'Лепельский', 'Миорский', 'Полоцкий', 'Россонский', 'Шумилинский', 'Свислочский', 'Борисовский', 'Мядельский', 'Слуцкий', 'Белыничский', 'Кличевский', 'Рогачевский', 'Кличевский', 'Кировский', 'Горецкий'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=42'), '1981', ['60','200'], ['5', '15'], ['Ельский', 'Житковичский', 'Лельчицкий', 'Ляховичский'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=43'), '2006', ['8','12'], ['0,12', '0,25'], ['Барановичский', 'Брестский', 'Ивацевичский', 'Каменецкий', 'Малоритский', 'Пружанский', 'Браславский', 'Докшицкий', 'Лепельский', 'Полоцкий', 'Россонский', 'Чашникский', 'Житковичский', 'Лельчицкий', 'Мозырский', 'Речицкий', 'Гродненский', 'Островецкий', 'Ошмянский', 'Слонимский', 'Сморгонский', 'Вилейский', 'Воложинский', 'Дзержинский', 'Крупский', 'Логойский', 'Минский', 'Мядельский', 'Смолевичский', 'Белыничский', 'Мстиславский', 'Осиповичский', 'Чериковский'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=44'), '1981', ['15','25'], ['5', '20'], ['Пуховичский', 'Витебский', 'Глубокский', 'Докшицкий', 'Лиозненский', 'Полоцкий', 'Шумилинский', 'Каменецкий'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=45'), '2006', ['45','120'], ['4,5', '10,5'], ['Житковичский', 'Горецкий'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=43'), '1981', ['15','30'], ['1,5', '5'], ['Лельчицкий'], [])
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=43'), '2006', ['20','35'], ['4', '10'], ['Хойникский', 'Брагинский'], [])
template.close()
