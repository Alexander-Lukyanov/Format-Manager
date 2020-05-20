# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QLabel, QProgressBar, QHBoxLayout, QVBoxLayout, QMessageBox, QInputDialog, QWidget)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pymorphy2
import sys
import csv
import json

# Функция для формирования в программе окон (QMessageBox) с различными сообщениями
def univ_message(tx_win, tx_mes, status):
    msg = QMessageBox()
    msg.setIcon(status)
    msg.setWindowTitle(tx_win)
    msg.setWindowIcon(QIcon('profile\logo.png'))
    msg.setText(tx_mes)
    msg.exec()

# Функция для подключения к общему диску с шаблонами таблиц, паспортами наборов и описаниями ресурсов
def connect_lib():
    try:
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SOURCE_ACCOUNT_FILE = 'profile\shared-disk-account.json'
        credentials = service_account.Credentials.from_service_account_file(SOURCE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        return service
    except:
        tx_win = 'Критична помилка програми'
        tx_mes = 'Один з основних конфігураційних файлів\nпрограми пошкоджений або відсутній.\nСпробуйте запустити програму ще раз'
        status = QMessageBox.Critical
        univ_message(tx_win, tx_mes, status)
        sys.exit ()

# Функция для подключения к индивидуальному хранилищу распорядителя данных
def connect_storage():
    try:
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SOURCE_ACCOUNT_FILE = 'profile\personal-vault-account.json'
        credentials = service_account.Credentials.from_service_account_file(SOURCE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        return service
    except:
        tx_win = 'Критична помилка програми'
        tx_mes = 'Один з основних конфігураційних файлів\nпрограми пошкоджений або відсутній.\nСпробуйте запустити програму ще раз'
        status = QMessageBox.Critical
        univ_message(tx_win, tx_mes, status)
        sys.exit()

# Функция для подключения к индивидуальному хранилищу с целью работы с данными таблиц наборов распорядителя
def work_sheet():
    try:
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SOURCE_ACCOUNT_FILE = 'profile\personal-vault-account.json'
        credentials = service_account.Credentials.from_service_account_file(SOURCE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except:
        tx_win = 'Критична помилка програми'
        tx_mes = 'Один з основних конфігураційних файлів\nпрограми пошкоджений або відсутній.\nСпробуйте запустити програму ще раз'
        status = QMessageBox.Critical
        univ_message(tx_win, tx_mes, status)
        sys.exit()

# Функция, формирующая список всех наборов данных, размещенных либо на общем диске либо в хранилище пользователя
def list_building(account):
    actual_sets = [] # Фактически имеющиеся наборы данных
    standard_sets = [] # Стандртные наборы данных, размещенные на общем диске
    isx_list = [] # Исходный список для последующего сравнения
    results = account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        actual_sets.append(dict(id=results.get('files', [])[f]['id'], folder=results.get('files', [])[f]['name']))
    with open('profile\standard_dataset_list.csv','r', encoding='utf-8') as f_csv:
        reader = csv.DictReader(f_csv, delimiter=',')
        for line in reader:
            standard_sets.append(dict(groups=line['groups'], folder=line['folder'], dataset=line['dataset']))
    l1 = len(actual_sets)
    l2 = len(standard_sets)
    for i in range(l1):
        for j in range(l2):
            if (actual_sets[i]['folder'] == standard_sets[j]['folder']):
                isx_list.append(dict(groups=standard_sets[j]['groups'], folder=standard_sets[j]['folder'], id=actual_sets[i]['id'], dataset=standard_sets[j]['dataset']))
    return isx_list

# Функция, выводящая из общего диска или из индивидуального хранилища пользователя список всех наборов данных
def sets_output(isx_list):
    full_list = []  # Полный список для вывода в окно
    list1 = []  # Список по выводу группы "Усі розпорядники інформації"
    list2 = []  # Список по выводу группы "Архітектура та містобудування"
    list3 = []  # Список по выводу группы "Бюджет та фінанси"
    list4 = []  # Список по выводу группы "Інфраструктура"
    list5 = []  # Список по выводу группы "Комунальна власність"
    list6 = []  # Список по выводу группы "Місцеві ради"
    list7 = []  # Список по выводу группы "Навколишнє середовище"
    list8 = []  # Список по выводу группы "Освіта"
    list9 = []  # Список по выводу группы "Охорона здоров’я"
    list10 = []  # Список по выводу группы "Торгівля"
    list11 = []  # Список по выводу группы "Громадський транспорт"
    list12 = []  # Список по выводу группы "Участь громадськості та інше"
    title1 = []
    title1.append(dict(metka='groups', name='ОРГАНИ МІСЦЕВОГО САМОВРЯДУВАННЯ'))
    l1 = len(isx_list)
    for j in range(l1):
        if (isx_list[j]['groups'] == '1'):
            list1.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '2'):
            list2.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '9'):
            list3.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '3'):
            list4.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '10'):
            list5.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '11'):
            list6.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '5'):
            list7.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '6'):
            list8.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '7'):
            list9.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '8'):
            list10.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '4'):
            list11.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        if (isx_list[j]['groups'] == '12'):
            list12.append(dict(metka=isx_list[j]['folder'], name=isx_list[j]['dataset'])); continue
        break
    if (len(list1) > 0):
        list1.sort(key=lambda i: i['metka']); list1.insert(0, dict(metka='groups', name='УСІ РОЗПОРЯДНИКИ ІНФОРМАЦІЇ'))
    if (len(list2) > 0):
        list2.sort(key=lambda i: i['name']); list2.insert(0, dict(metka='groups', name='Архітектура та містобудування'))
    if (len(list3) > 0):
        list3.sort(key=lambda i: i['name']); list3.insert(0, dict(metka='groups', name='Бюджет та фінанси'))
    if (len(list4) > 0):
        list4.sort(key=lambda i: i['name']); list4.insert(0, dict(metka='groups', name='Інфраструктура'))
    if (len(list5) > 0):
        list5.sort(key=lambda i: i['name']); list5.insert(0, dict(metka='groups', name='Комунальна власність'))
    if (len(list6) > 0):
        list6.sort(key=lambda i: i['name']); list6.insert(0, dict(metka='groups', name='Місцеві ради'))
    if (len(list7) > 0):
        list7.sort(key=lambda i: i['name']); list7.insert(0, dict(metka='groups', name='Навколишнє середовище'))
    if (len(list8) > 0):
        list8.sort(key=lambda i: i['name']); list8.insert(0, dict(metka='groups', name='Освіта'))
    if (len(list9) > 0):
        list9.sort(key=lambda i: i['name']); list9.insert(0, dict(metka='groups', name='Охорона здоров\'я'))
    if (len(list10) > 0):
        list10.sort(key=lambda i: i['name']); list10.insert(0, dict(metka='groups', name='Торгівля'))
    if (len(list11) > 0):
        list11.sort(key=lambda i: i['name']); list11.insert(0, dict(metka='groups', name='Громадський транспорт'))
    if (len(list12) > 0):
        list12.sort(key=lambda i: i['name']); list12.insert(0, dict(metka='groups', name='Участь громадськості та інше'))
    full_list = [*list1, *title1, *list2, *list3, *list4, *list5, *list6, *list7, *list8, *list9, *list10, *list11, *list12]
    return full_list

# Функция для загрузки в различные места программы общих сведений по распорядителю, которые были введены благодаря
def init_dil1():
    try:
        with open('profile\data_users.json', 'r', encoding='utf-8') as file:
            data_us = json.load(file)
        return data_us
    except:
        data = {
            'publisherName': 'Невідомий розпорядник інформації',
            'publisherIdentifier': '00000000',
            'publisherTerritory': 'Невідома',
            'license': 'Індивідуальне сховище',
            'baseLinkWebsite': 'https://demo.ckan.org',
            'contactPointFn': 'Невідома',
            'contactPointHasEmail': 'Невідомий',
            'publisherNameRod': 'Невідомого розпорядника інформації',
            'publisherNameTvor': 'Невідомим розпорядником інформації',
            'publisherNameDat': 'Невідомому розпоряднику інформації',
            'publisherNameVin': 'Невідомого розпорядника інформації',
            'publisherTerritoryRod': 'Невідомого',
            'key_api_steward': 'Невідомий',
            'organization_id': 'Невідомий'

        }
        data_us = json.dumps(data, indent=2, ensure_ascii=False)
        with open('profile\data_users.json', 'w', encoding='utf-8') as file:
            file.write(data_us)
            file.close()
        with open('profile\data_users.json', 'r', encoding='utf-8') as file:
            data_us = json.load(file)
        return data_us

# Универсальная функция для вывода прогресс-бара в главном окне программы
def start_pbar(self, st_ms):
    self.hbox_pb1 = QHBoxLayout()
    self.hbox_pb1.addStretch(1)
    self.lpb = QLabel(st_ms)
    self.hbox_pb1.addWidget(self.lpb)
    self.hbox_pb1.addStretch(1)
    self.hbox_pb2 = QHBoxLayout()
    self.hbox_pb2.addStretch(0)
    self.pbar = QProgressBar(self)
    self.hbox_pb2.addWidget(self.pbar)
    self.hbox_pb2.addStretch(0)
    self.sly.addStretch(1)
    self.sly.addLayout(self.hbox_pb1)
    self.sly.addLayout(self.hbox_pb2)
    self.sly.addStretch(1)
    self.pbar.setValue(1)
    self.pbar.show()
    self.sly.update()

# Функция для склонения слов по падежам для отдельных реквизитов общих сведений по распорядителю
def decl_words(text, padez):
    morph = pymorphy2.MorphAnalyzer(lang='uk')
    titl = ''
    name1 = text.split()
    for w in name1:
        word1 = morph.parse(w)[0]
        word2 = word1.inflect({padez}).word
        if (word2 == 'рада' and padez == 'gent'): word2 = 'ради'
        if (word2 == 'радом' and padez == 'ablt'): word2 = 'радою'
        if (word2 == 'радові' and padez == 'datv'): word2 = 'раді'
        if (word2 == 'рад' and padez == 'accs'): word2 = 'раду'
        if (w.istitle()):  word2 = word2.title()
        titl = titl + word2 + ' '
    titl = titl.rstrip()
    return titl

# Функция восстановления главного окна программы после выполнения какой-либо команды меню
def main_screen(self):
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)
    self.sly = QVBoxLayout(self.central_widget)
    self.statusBar().showMessage('')
    self.hbox_main = QHBoxLayout()
    self.hbox_main.addStretch(0)
    self.img1 = QLabel(self)
    self.pixmap = QPixmap('profile\program_logo.png')
    self.img1.setPixmap(self.pixmap)
    self.hbox_main.addWidget(self.img1)
    self.hbox_main.addStretch(0)
    self.sly.addLayout(self.hbox_main)
    self.show()

# Функция, проверяющая наличие в индивидуальном хранилище базового набора с файлами реестров остальных наборов данных
# и их ресурсов
def check_007(fold):
    # fold - имя папки, по которой нам необходимо собрать данные
    # fold_id - ID папки, по которой нам необходимо найти данные
    fold_id = '0'
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        if (results.get('files', [])[f]['name']== fold):
            fold_id = results.get('files', [])[f]['id']; break
    return fold_id

# Функция, загружает в массив значения из заданного диапозона ячеек в заданной Google таблице
def load_dat(folder, file, cell_range):
    file_id = ''
    fold_id = check_007(folder)
    searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        if (results.get('files', [])[f]['name'] == file):
            file_id = results.get('files', [])[f]['id']
    pers_sheet = work_sheet()
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=file_id, range=cell_range).execute()
    values = result.get('values', [])
    return values

# Универсальная функция простого диалогового окна для ввода пользователем дополнительных значений
def univ_dialog(self, tx_win, tx_mes):
    text, ok = QInputDialog.getText(self, tx_win, tx_mes)
    return  text, ok

# Функция для транслетерации имени набора данных и формирования такого реквизита, как name
def trans_name(string):
    letters = {u'А': u'a',
               u'Б': u'b',
               u'В': u'v',
               u'Г': u'g',
               u'Ґ': u'g',
               u'Д': u'd',
               u'Е': u'e',
               u'Є': u'e',
               u'Ж': u'zh',
               u'З': u'z',
               u'И': u'i',
               u'І': u'i',
               u'Ї': u'i',
               u'Й': u'y',
               u'К': u'k',
               u'Л': u'l',
               u'М': u'm',
               u'Н': u'n',
               u'О': u'o',
               u'П': u'p',
               u'Р': u'r',
               u'С': u's',
               u'Т': u't',
               u'У': u'u',
               u'Ф': u'f',
               u'Х': u'h',
               u'Ц': u'ts',
               u'Ч': u'ch',
               u'Ш': u'sh',
               u'Щ': u'sch',
               u'Ь': u'',
               u'Ю': u'yu',
               u'Я': u'ya',
               u'\'': u'',
               u' ': u'-',
               u'а': u'a',
               u'б': u'b',
               u'в': u'v',
               u'г': u'g',
               u'ґ': u'g',
               u'д': u'd',
               u'е': u'e',
               u'є': u'e',
               u'ж': u'zh',
               u'з': u'z',
               u'и': u'i',
               u'і': u'i',
               u'ї': u'i',
               u'й': u'y',
               u'к': u'k',
               u'л': u'l',
               u'м': u'm',
               u'н': u'n',
               u'о': u'o',
               u'п': u'p',
               u'р': u'r',
               u'с': u's',
               u'т': u't',
               u'у': u'u',
               u'ф': u'f',
               u'х': u'h',
               u'ц': u'ts',
               u'ч': u'ch',
               u'ш': u'sh',
               u'щ': u'sch',
               u'ь': u'',
               u'ю': u'yu',
               u'я': u'ya'}
    mas1 = init_dil1()
    kod = mas1['publisherIdentifier']
    tr_str = ""
    if (len(string)>50):
        string = string[0:50]+' '
    for index, char in enumerate(string):
        if char in letters.keys():
            char = letters[char]
            tr_str += char
    tr_str = kod + '-' + tr_str
    return tr_str

# Функция, которая выводит сведения о ресурсах, размещенных в индивидуальном хранилище распорядителя
def out_resource1(full_list):
    stand_fil = []  # Список стандартных файлов, присущих наборам данных в индивидуальном хранилище
    for el1 in full_list:
        if (el1['metka'] != 'groups'):
            name_set = el1['metka']
            with open('profile\standard_dataset_files.csv', 'r', encoding='utf-8') as f_csv:
                reader = csv.DictReader(f_csv, delimiter=',')
                for st in reader:
                    if ((st['folder'] == name_set) and (st['file_type'] == 'ресурси')):
                        stand_fil.append(dict(folder=st['folder'], file=st['file_name'], description=st['file_description']))
    return stand_fil

# Функция, которая для позиции "ключевые слова" в паспортах наборов данных заменяет апостроф на мягкий знак
def str_valid(st):
    tr_str = ''
    for ch in st:
        if (ch == "'"): ch = 'ь'
        if (ch == "’"): ch = 'ь'
        tr_str += ch
    return tr_str
