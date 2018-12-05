import requests # получение html кода страницы по url
from bs4 import BeautifulSoup # модуль для парсинга
import re
from time import sleep

def get_html(url, useragent=None, proxy=None):
    print('get_html')
    r = requests.get(url, headers=useragent, proxies=proxy, cookies={'serverPW': '40ba9118730170106e6a8a2f0e316c88a2c55c2c6a4456e3979e2e3b7babce01a%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22serverPW%22%3Bi%3A1%3BN%3B%7D'})
    return r.text   

def get_and_set_data(html,template, pop, year, temp_length_stem, temp_length_inf, districts, parts):  # 4 последних аргумента - списки 
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
            template = re.sub("temp_distr", ';;->'.join(districs), template)
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
get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=38'), template.read())
template.close()
