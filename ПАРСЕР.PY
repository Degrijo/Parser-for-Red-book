import requests # получение html кода страницы по url
from bs4 import BeautifulSoup # модуль для парсинга
import re
from time import sleep

def get_html(url, useragent=None, proxy=None):
    print('get_html')
    r = requests.get(url, headers=useragent, proxies=proxy, cookies={'serverPW': '40ba9118730170106e6a8a2f0e316c88a2c55c2c6a4456e3979e2e3b7babce01a%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22serverPW%22%3Bi%3A1%3BN%3B%7D'})
    return r.text

def get_ip(html):
    print('get_ip')
    print('New Proxy & User-Agent:')
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_= 'ip').text.strip()   


def get_and_set_data(html,f):
    soup = BeautifulSoup(html, 'lxml')
    try:
        
        name = soup.find('td', valign = 'top', style = 'padding-left:10px').text.strip().lower()
        name = []
        names.append(re.search(r'^[а-я, ,.,(,),,,=]+', name).group())
        name = name[re.search('^[а-я, ,.,(,),,,=]+', name).end():]
        names.append(re.search(r'[a-z, ,.,,,(,),=]+', name).group())
        name = name[re.search(r'[a-z, ,.,,,(,),=]+', name).end():]
        names.append(name)
        del name
        idtf = re.sub(' ', '_', names[1])
        sec_cat = soup.find('a', href="/hints/cats.html", onclick='return _help("cats");', target="_blank").text
        print(sec_cat)
        paragraphs = soup.find_all('p')[6:8] +[soup.find_all('p')[9]] + soup.find_all('p')[11:16]
        paragraphs = [i.text.strip() for i in paragraphs]
        for i in range(len(paragraphs)):
            paragraphs[i] = re.sub("\n", '', paragraphs[i])
            paragraphs[i] = re.sub(':', ': ', paragraphs[i])
        file = open("concept_" + idtf, 'w')
        
        file.close()
    except:
        print('error in '+name_ru)
    

template = open("template.scs")
print(get_and_set_data(get_html('http://redbook.minpriroda.gov.by/plantsinfo.html?id=38')), template)
template.close()
