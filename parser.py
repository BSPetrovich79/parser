# -*- coding: utf-8 -*-
from settings import WEB_SITE
import time
import core
from log_module import log

"""
Собрать все ссылки с сайта в файл url.txt,
перебрать все урлы из этого файла и проверить, 
что все файлы на сайте отдают 200.
Если не 200, записать в файл file_error и идти дальше.
"""

url = WEB_SITE
html = core.get_html(url)
links_list = core.get_links(html)
time_start = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

# print('start' + ' ' + time_start)

log('start' + ' ' + time_start)

core.link_building(links_list)

core.files_error()

# print('END: STATUS DONE')
log('END: STATUS DONE')
