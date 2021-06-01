# -*- coding: utf-8 -*-
import requests
from settings import WEB_SITE, LINKS_LIST, EXCEPTIONS, PROJ_FOLDER
from bs4 import BeautifulSoup
import time
import re
import os
from log_module import log



"""
Зайти на сайт
Собрать все ссылки в url.txt
Проверить на доступность (Статус 200)
Собрать все файлы, прикрепленные к сайту.
Проверить их доступность.
"""
time_day = time.strftime("%Y-%m-%d", time.localtime())

url = WEB_SITE
regular_expression = r'.*\.(pdf|docx|doc|xls|xlsx).*'
url_file = time_day + '_' + 'url.txt'
files_file = time_day + '_' + 'files.txt'
err_file = time_day + '_' + 'err.txt'


def create_fold_url(f_name):
    if not os.path.isdir(PROJ_FOLDER + "\\logs\\" + f_name + "\\"):
        os.makedirs(PROJ_FOLDER + "\\logs\\" + f_name + "\\")
    return PROJ_FOLDER + "\\logs\\" + f_name + "\\"


folder_url = create_fold_url("url")
folder_files = create_fold_url("files")


def create_file_name(folder_name, file_name):
    return folder_name + file_name


file_name_url = create_file_name(folder_url, url_file)
file_name_files = create_file_name(folder_files, files_file)


def get_html(url):  # получаем страницу
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError, TypeError):
        # print('Упал на {url}')
        return False


def get_links(html):  # получаем все линки со страницы
    LINKS_LIST = []
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'] not in EXCEPTIONS:
            if not 'http' in a['href']:
                a['href'] = WEB_SITE + a['href']
            if not 'static.mts.ru' in a['href'] and not 'www.irs.gov' in a['href'] and a['href'] not in LINKS_LIST:
                LINKS_LIST.append(a['href'])
    return LINKS_LIST


def link_building(links_list):
    tmp_list = []
    if __name__ == '__main__':
        html = get_html(WEB_SITE)
        if html:
            links_list = get_links(html)
    with open(file_name_url, 'w', encoding='utf-8') as f:
        with open(file_name_files, 'w', encoding='utf-8') as files:
            for link in links_list:
                html2 = get_html(link)
                if html2:
                    links_list2 = get_links(html2)
                    for link in links_list2:
                        if re.fullmatch(regular_expression, link):
                            # pass
                            if WEB_SITE in link:
                                try:
                                    response = requests.head(link, timeout=5)
                                    files.write(time_day + '_' + str(response) + '_' + link + '\n')
                                    # print(time_day + '_' + str(response) + '_' + link + '\n')
                                    log(time_day + '_' + str(response) + '_' + link + '\n')
                                except(ConnectionError, requests.exceptions.ConnectTimeout):
                                    files.write(time_day + '_' + "ConnectionError: " + link + '\n')
                                    # print(time_day + '_' + "ConnectionError: " + link + '\n')
                                    log(time_day + '_' + "ConnectionError: " + link + '\n')
                        else:
                            f.write(link + '\n')


def files_error():
    """""Открыть files.txt
         Перебрать все ссылки
         Найти не 200 и вывести в принт
         Записать в лог
    """""
    folder_err = create_fold_url("err")
    file_name_err = create_file_name(folder_err, err_file)
    folder_files = create_fold_url("files")
    file_name_files = create_file_name(folder_files, files_file)
    with open(file_name_files, 'r', encoding='utf-8') as f:
        with open(file_name_err, 'w', encoding='utf-8') as f_err:
            for line in f.readlines():
                OK_RESP = '<Response [200]>'
                if OK_RESP not in line:
                    f_err.write(time_day + '_' + 'file not found' + '_' + line + '\n')
                    # print(time_day + '_' + 'file not found' + '_' + line + '\n')
                    log(time_day + '_' + 'file not found' + '_' + line + '\n')
