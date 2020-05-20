# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem,
                             QMessageBox)
from univ_func import (connect_storage, list_building, sets_output, work_sheet, out_resource1, univ_message,
                       trans_name, init_dil1, str_valid)
import requests
import json
from apiclient import errors
import csv

# Функция, формирующая окна, открываемые по таким командм меню, как «Создание наборов данных» и «Обновление паспортов
# наборов данных»
def win2_1(metka):
    pers_account = connect_storage()  # Функция подключения к индивидуальному хранилищу
    isx_list = list_building(pers_account)  # Функция формирования списка набора данных
    full_list = sets_output(isx_list)  # Функция вывода списка наборов данных
    # Создаем виджет рамки (box1) для размещения в нем виджета списка наборов данных из индивидуального диска
    if (metka == 'p1' or metka == 'p3'):
        box1 = QGroupBox('Набори даних, що розміщуються в індивідуальному сховище розпорядника')
    box1.setAlignment(QtCore.Qt.AlignCenter)
    vbox1 = QVBoxLayout()
    box1.setLayout(vbox1)
    # Создаем виджет списка (spisok1) для размещения в нем наборов данных из индивидуального диска
    spisok1 = QListWidget()
    # Добавляем в spisok1 элементы из имеющегося массива full_list
    l = len(full_list)
    for i in range(l):
        if (full_list[i]['metka'] == 'groups'):
            item = QListWidgetItem(full_list[i]['name'])
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
        else:
            item = QListWidgetItem(full_list[i]['name'])
            item.setCheckState(QtCore.Qt.Unchecked)
        spisok1.addItem(item)
    vbox1.addWidget(spisok1)
    # Создаем виджет рамки (box2) для размещения в нем виджета списка наборов, которые хотим разместить на data.gov.ua
    if (metka == 'p1'):
        box2 = QGroupBox('Набори даних, паспорта і ресурси яких зі сховища розпорядника будуть перенесені'
                         ' в новостворені набори на порталі відкритих даних data.gov.ua')
    if (metka == 'p3'):
        box2 = QGroupBox('Набори даних, зміст паспортів яких зі сховища розпорядника буде перенесений в паспорти таких'
                         ' же наборів, розміщених на Єдиному порталі відкритих даних  data.gov.ua')
    box2.setAlignment(QtCore.Qt.AlignCenter)
    vbox2 = QVBoxLayout()
    box2.setLayout(vbox2)
    # Создаем виджет списка (spisok2) для размещения в нем наборов, которые хотим разместить на data.gov.ua
    spisok2 = QListWidget()
    vbox2.addWidget(spisok2)
    # Создаем кнопку "Создать наборы на портале" ("Обновить паспорта наборов"), а также кнопку "Закрити це вікно"
    if (metka == 'p1'): but1 = QPushButton(' Створити набори на порталі ')
    if (metka == 'p3'): but1 = QPushButton(' Оновити паспорта наборів ')
    but2 = QPushButton(' Закрити це вікно ')
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(but1)
    hbox.addWidget(but2)
    vbox2.addLayout(hbox)
    return box1, box2, spisok1, spisok2, but1, but2, full_list, isx_list, pers_account

# Функция, формирующая окна, открываемые по таким командам меню, как «Публикация ресурсов к наборам данных» и
# «Обновление описаний ресурсов наборов»
def win2_2(metka):
    # stand_fil = [] Список стандартных файлов, присущих наборам данных в индивидуальном хранилище
    sp_res = [] # Список с характеристиками списка из наборов и их ресурсов
    pers_account = connect_storage()  # Функция подключения к индивидуальному хранилищу
    isx_list = list_building(pers_account)  # Функция формирования списка набора данных
    full_list = sets_output(isx_list)  # Функция вывода списка наборов данных
    # Создаем виджет рамки (box1) для размещения в нем списка ресурсов для наборов данных из индивидуального диска
    if (metka == 'p2' or metka == 'p4'):
        box1 = QGroupBox('Набори даних та їх, сформовані на основі таблиць Форматорів, ресурси розміщені в'
                         ' індивідуальному сховище розпорядника')
    box1.setAlignment(QtCore.Qt.AlignCenter)
    vbox1 = QVBoxLayout()
    box1.setLayout(vbox1)
    # Создаем виджет списка (spisok1) для размещения в нем списка ресурсов для наборов данных из индивидуального диска
    spisok1 = QListWidget()
    # Добавляем в spisok1 элементы из имеющегося массива full_list
    stand_fil = out_resource1(full_list)
    for dset in full_list:
        if (dset['metka'] == 'groups'):
            item = QListWidgetItem(dset['name'])
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            sp_res.append(dict(folder='groups', file='absent', description=dset['name']))
            spisok1.addItem(item)
        else:
            item = QListWidgetItem(dset['name'].upper())
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable)
            sp_res.append(dict(folder=dset['metka'], file='absent', description=dset['name'].upper()))
            spisok1.addItem(item)
            for resorce in stand_fil:
                if (resorce['folder'] == dset['metka']):
                    res1 = resorce['file']; res1 = res1[0:(len(res1)-9)]
                    name1 = res1 + ' - ' + resorce['description']
                    item = QListWidgetItem(name1)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    sp_res.append(dict(folder=dset['metka'], file=res1, description=name1))
                    spisok1.addItem(item)
    vbox1.addWidget(spisok1)
    # Создаем виджет рамки (box2) для размещения в нем списка ресурсов соответствующих наборов, которые клонируем на data.gov.ua
    if (metka == 'p2'): box2 = QGroupBox('Ресурси відповідних наборів даних, які будуть перенесені в свої аналоги, що'
                                         ' розміщені на Єдиному державному порталі відкритих даних data.gov.ua')
    if (metka == 'p4'): box2 = QGroupBox('Ресурси відповідних наборів даних, описи  яких зі сховища розпорядника будуть'
                                         ' перенесені в такі ж описи ресурсів, розміщені на порталі data.gov.ua')
    box2.setAlignment(QtCore.Qt.AlignCenter)
    vbox2 = QVBoxLayout()
    box2.setLayout(vbox2)
    # Создаем виджет списка (spisok2) для размещения в нем ресурсов соответствующих наборов, которые клонируем на data.gov.ua
    spisok2 = QListWidget()
    vbox2.addWidget(spisok2)
    # Создаем кнопку "Опубликовать ресурсы на портале" ("Обновить описания ресурсов на портале") и кнопку "Закрити це вікно"
    if (metka == 'p2'): but1 = QPushButton(' Опублікувати ресурси на порталі ')
    if (metka == 'p4'): but1 = QPushButton(' Оновити описи ресурсів на порталі ')
    but2 = QPushButton(' Закрити це вікно ')
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(but1)
    hbox.addWidget(but2)
    vbox2.addLayout(hbox)
    return box1, box2, spisok1, spisok2, but1, but2, sp_res, isx_list, pers_account

# Функция создающая сообщение о необходимости актуализации реестра наборов данных перед их созданием на портале
def create_msg2_1():
    msg2 = QMessageBox()
    msg2.setIcon(QMessageBox.Information)
    msg2.setWindowTitle('Повідомлення щодо необхідності актуалізації реєстру наборів даних')
    msg2.setWindowIcon(QIcon('profile\logo.png'))
    msg2.setInformativeText('Тому, якщо Ви ще не сформували даний реєстр, або в разі, коли Ви вносили зміни в'
                            ' паспорти деяких наборів даних, Вам необхідно попередньо заново сформувати або оновити цей'
                            ' реєстр.\nЦе слід зробити за допомогою команди «Формування реєстру наборів даних» у меню'
                            ' «Налаштування програми».')
    okButton2 = msg2.addButton(' Продовжувати виконання команди ', QMessageBox.AcceptRole)
    msg2.addButton(' Вийти з команди і оновити реєстр ', QMessageBox.RejectRole)
    return msg2, okButton2

# Функция создающая сообщение о необходимости актуализации реестра ресурсов наборов данных перед их публикацией на портале
def create_msg2_2():
    msg2 = QMessageBox()
    msg2.setIcon(QMessageBox.Information)
    msg2.setWindowTitle('Повідомлення щодо необхідності актуалізації реєстру ресурсів наборів даних')
    msg2.setWindowIcon(QIcon('profile\logo.png'))
    msg2.setInformativeText('Тому, якщо Ви ще не сформували даний реєстр, або в разі, коли Ви вносили зміни в'
                            ' описи деяких ресурсів наборів даних, Вам необхідно попередньо заново сформувати або оновити цей'
                            ' реєстр.\nЦе слід зробити за допомогою команди «Формування реєстру ресурсів» у меню'
                            ' «Налаштування програми».')
    okButton2 = msg2.addButton(' Продовжувати виконання команди ', QMessageBox.AcceptRole)
    msg2.addButton(' Вийти з команди і оновити реєстр ', QMessageBox.RejectRole)
    return msg2, okButton2

# Функция загрузки значений из реестра наборов данных в словарь (массив)
def check_emptiness(self, fold_id):
    # fold - имя папки, по которой нам необходимо собрать данные
    # fold_id - ID папки, по которой нам необходимо найти данные
    dset_reg = []  # Сведения о наборах данных, которые находятся в реестре
    self.msg2, self.okButton2 = create_msg2_1()
    self.msg2.setText('Для того, щоб аналоги паспортів обраних Вами наборів даних можна було створити (оновити) на порталі'
                      ' використовується інформація, розміщена в спеціальному реєстрі цих наборів.')
    self.msg2.exec()
    if (self.msg2.clickedButton() != self.okButton2):  return -1, dset_reg, '0'
    self.pbar.setValue(10)
    searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    results = self.pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        f_name = results.get('files', [])[f]['name']
        if (f_name == 'registerFormatter'):
            id_reg = results.get('files', [])[f]['id']; name_reg = f_name; break
    # Формируем массив со сведениями об уже имеющихся данных в реестре наборов данных
    cell_range = 'Register!A2:N'
    pers_sheet = work_sheet()
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=id_reg, range=cell_range).execute()
    values = result.get('values', [])
    for st in values:
        dset_reg.append(dict(A=st[0], B=st[1], C=st[2], D=st[3], E=st[4], F=st[5], G=st[6], H=st[7], I=st[8], J=st[9],
                             K=st[10], L=st[11], M=st[12], N=st[13]))
    self.pbar.setValue(20)
    return 0, dset_reg, id_reg

# Функция создания наборов данных на портале для онлайн доступа
def onlay_dset(self, dset_reg, id_reg):
    s_set = [] # список для выбранных наборов данны
    st_files = []  # Список стандартных файлов, размещенных на общем диске
    dataset = [] # Массив сведений для создания на портале выбранных наборв данных
    dset_new = [] # Массив обновленных значений реестра наборов данных
    # Формируем список из тех наборов данных, которые были выбраны для создания их аналогов на портале
    n = len(self.isx_list)
    for i in range(self.spisok2.count()):
        name1 = self.spisok2.item(i).text()
        l1 = len(self.full_list)
        for i1 in range(l1):
            if ((self.full_list[i1]['name'] == name1) and (self.full_list[i1]['metka'] != 'groups')):
                s_set.append(dict(folder=self.full_list[i1]['metka']))
                break
    # Формируем все необходимые сведения для создания выбранных наборов данных на портале
    for st in s_set:
        metka1 = 0
        for rec in dset_reg:
            if (st['folder'] == rec['A']):
                if (rec['B'] != 'null'):
                    tx_win = 'Попередження про неможливість виконання запущеної команди'
                    tx_mes = 'У вас вже існує набір даних:\n\n - ' + rec['C'] + '\n\nТому дана команда не може бути виконана.'
                    univ_message(tx_win, tx_mes, QMessageBox.Warning)
                    return
                name_str = trans_name(rec['C'])
                title_str = rec['C']
                if (len(title_str)>254): title_str = title_str[0:253]
                notes_str = rec['D']
                if (len(notes_str) > 400): notes_str = notes_str[0:399]
                tag_str = rec['F']
                if (len(tag_str) > 400): tag_str = notes_str[0:399]
                purp_coll = rec['G']
                if (len(purp_coll) > 400): purp_coll = notes_str[0:399]
                up_fr = rec['E']
                if (up_fr == 'Щодня'): up_fr = 'once a day'
                if (up_fr == 'Щотижня'): up_fr = 'once a week'
                if (up_fr == 'Щомісяця'): up_fr = 'once a month'
                if (up_fr == 'Щокварталу'): up_fr = 'once a quarter'
                if (up_fr == 'Кожні півроку'): up_fr = 'once a half year'
                if (up_fr == 'Щороку'): up_fr = 'once a year'
                if (up_fr == 'Відразу після внесення змін'): up_fr = 'immediately after making changes'
                if (up_fr == 'Більше одного разу на день'): up_fr = 'more than once a day'
                if (up_fr == 'Позапланово'): up_fr = 'unscheduled'
                lang = rec['J'];
                if (lang == 'Українська'): lang = 'ua'
                if (lang == 'Російська'): lang = 'ru'
                if (lang == 'Англійська'): lang = 'en'
                if (lang == 'Румунська'): lang = 'ro'
                if (lang == 'Угорська'): lang = 'hu'
                if (lang == 'Болгарська'): lang = 'bg'
                if (lang == 'Польська'): lang = 'pl'
                dataset.append(dict(folder=rec['A'], name=name_str, title=title_str, notes=notes_str, tag=tag_str, maintainer=rec['M'],
                                    m_email=rec['N'], purpose_collecting=purp_coll, up_frequency=up_fr, language=lang,
                                    publisherIdentifier=rec['L']))
                metka1 = 1; break
        if (metka1 == 0):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Деякі вибрані Вами набори даних відсутні у відповідному реєстрі.\nТому, Вам слід попередньо оновити' \
                     ' цей реєстр за допомогою команди «Формування реєстру наборів даних» у меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            return
    # Создаем на портале ноборы данных и публикуем подготовленные для этих наборов паспорта
    pb_step = round(80 / len(dataset))
    pb = pb_step
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    key_api = mas1['key_api_steward']
    organization = mas1['organization_id']
    path1 = mas1['baseLinkWebsite'] + '/api/3/action/package_create'
    path2 = mas1['baseLinkWebsite'] + '/dataset/'
    path3 = mas1['baseLinkWebsite'] + '/api/3/action/resource_create'
    l1 = len(dset_reg)
    with open('profile\standard_dataset_files.csv', 'r', encoding='utf-8') as f_csv:
        reader = csv.DictReader(f_csv, delimiter=',')
        for line in reader:
            st_files.append(dict(folder=line['folder'], type=line['file_type'], file=line['file_name'],
                                 description=line['file_description']))
    pers_sheet = work_sheet()
    for d_st in dataset:
        pb = pb + pb_step
        self.pbar.setValue(pb)
        data_dict = {
            'name': d_st['name'],
            'title': d_st['title'],
            'notes': d_st['notes'],
            'tag_string': str_valid(d_st['tag']),
            'owner_org': organization,
            'maintainer': d_st['maintainer'],
            'maintainer_email': d_st['m_email'],
            'extras': [
                {'key': 'purpose_of_collecting_information', 'value': d_st['purpose_collecting']},
                {'key': 'update_frequency', 'value': d_st['up_frequency']},
                {'key': 'language', 'value': d_st['language']},
                {'key': 'publisherIdentifier', 'value': d_st['publisherIdentifier']}]
        }
        data = str(json.dumps(data_dict))
        headers = {'Authorization': key_api,
                   'Content-Type': 'application/json'}
        response = requests.post(path1, headers=headers, data=data)
        response_dict = json.loads(response.content)
        flag = response_dict['success']
        if (flag):
            for i in range(l1):
                if (dset_reg[i]['A'] == d_st['folder']):
                    dset_reg[i]['B'] = d_st['name']
                    dset_reg[i]['H'] = path2 + d_st['name']
                    dset_reg[i]['I'] = 'CSV'
        for row1 in st_files:
            if ((row1['folder'] == d_st['folder']) and row1['type'] == 'структура ресурсів'):
                fold = row1['folder']; fil_name = row1['file']; fil_descr = row1['description']
                for row2 in self.isx_list:
                    if (row2['folder'] == fold):
                        fold_id = row2['id']
                        searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
                        results = self.pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
                        fnumb = len(results.get('files', []))
                        for f in range(fnumb):
                            f_n = results.get('files', [])[f]['name']
                            if (f_n == fil_name):
                                file_id = results.get('files', [])[f]['id']
                                sh_met = pers_sheet.spreadsheets().get(spreadsheetId=file_id).execute()
                                properties = sh_met.get('sheets')
                                sheet_id = properties[0].get("properties").get('sheetId')
                                st_url = 'https://docs.google.com/spreadsheets/d/' + file_id + '/export?format=csv&id=' + \
                                         file_id + '&gid=' + str(sheet_id)
                                data = {
                                    'package_id': d_st['name'],
                                    "url": st_url,
                                    'name': fil_name,
                                    'description': fil_descr,
                                    'format': 'CSV',
                                }
                                headers = {'X-CKAN-API-Key': key_api}
                                response1 = requests.post(path3, data=data, headers=headers)
                                break
    for ds in dset_reg:
        if (ds['B'] == 'null'): ds['B'] = ''
        if (ds['C'] == 'null'): ds['C'] = ''
        if (ds['D'] == 'null'): ds['D'] = ''
        if (ds['E'] == 'null'): ds['E'] = ''
        if (ds['F'] == 'null'): ds['F'] = ''
        if (ds['G'] == 'null'): ds['G'] = ''
        if (ds['H'] == 'null'): ds['H'] = ''
        if (ds['I'] == 'null'): ds['I'] = ''
        if (ds['J'] == 'null'): ds['J'] = ''
        if (ds['K'] == 'null'): ds['K'] = ''
        if (ds['L'] == 'null'): ds['L'] = ''
        if (ds['M'] == 'null'): ds['M'] = ''
        if (ds['N'] == 'null'): ds['N'] = ''
        ds1 = [ds['A'], ds['B'], ds['C'], ds['D'], ds['E'], ds['F'], ds['G'], ds['H'], ds['I'], ds['J'], ds['K'], ds['L'],
               ds['M'], ds['N']]
        dset_new.append(ds1)
    self.pbar.setValue(100)
    cell_range = 'Введення даних!A3:N'
    response = pers_sheet.spreadsheets().values().clear(spreadsheetId=id_reg, range=cell_range).execute()
    cell_range = 'Введення даних!A3:N' + str(2 + len(dset_new))
    zn = {'values': dset_new}
    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_reg, range=cell_range,
                                                         valueInputOption='RAW', body=zn).execute()

# Функция проверки и загрузки значений из реестра ресурсов наборов данных в словарь с последующей публикацией ресурсов на портале
def onlay_resource(self, fold_id):
    # fold_id - ID папки, по которой нам необходимо найти данные
    # id1_reg - ID файла registerFormatter
    # id2_reg - ID файла resourceRegistryFormatter
    # res_reg - Массив информации из реестра ресурсов наборов данных
    # fin_res - Массив информации по выбранным ресурсам, которые следует опубликовать на портале
    res_new = []  # Массив обновленных значений реестра ресурсов наборов данных
    m_ds = [] # Массив для папок и ID наборов данных, уже созданных на портале
    res_reg = [] # Сведения о ресурсах наборах данных, которые находятся в реестре
    fin_res = [] # Итоговый результат данных, которые будут использованы для публикации ресурсов
    self.msg2, self.okButton2 = create_msg2_2()
    self.msg2.setText('Для того, щоб вибрані Вами ресурси наборів даних можна було опублікувати на відповідному порталі'
                      ' використовується інформація, розміщена в спеціальному реєстрі цих ресурсів.')
    self.msg2.exec()
    if (self.msg2.clickedButton() != self.okButton2): return
    self.pbar.setValue(10)
    searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    results = self.pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        f_name = results.get('files', [])[f]['name']
        if (f_name == 'registerFormatter'):
            id1_reg = results.get('files', [])[f]['id']; name1_reg = f_name
        if (f_name == 'resourceRegistryFormatter'):
            id2_reg = results.get('files', [])[f]['id']; name2_reg = f_name
    # Формируем массив со сведениями об уже имеющихся ID в реестре наборов данных
    pers_sheet = work_sheet()
    cell_range = 'Register!A2:C'
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=id1_reg, range=cell_range).execute()
    values = result.get('values', [])
    for st in values:
        m_ds.append(dict(A=st[0], B=st[1], C=st[2]))
    # Формируем массив со сведениями об уже имеющихся данных в реестре ресурсов наборов данных
    cell_range = 'ResourceRegistry!A2:G'
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=id2_reg, range=cell_range).execute()
    values = result.get('values', [])
    for st in values:
        res_reg.append(dict(A=st[0], B=st[1], C=st[2], D=st[3], E=st[4], F=st[5], G=st[6]))
    if (len(res_reg) == 0):
        tx_win = 'Попередження про неможливість виконання запущеної команди'
        tx_mes = 'Для опублікування ресурсів наборів даних на відповідному порталі Ви маєте спочатку сформувати' \
                 ' спеціальний реєстр ресурсів всіх тих наборів даних, які зараз знаходяться у Вашому індивідуальному' \
                 ' сховище.\nЦе слід зробити за допомогою виконання команди «Формування реєстру ресурсів» в меню' \
                 ' «Налаштування програми».'
        univ_message(tx_win, tx_mes, QMessageBox.Warning)
        return
    for sp1 in self.act_l:
        for sp2 in m_ds:
            if (sp2['A'] == sp1['folder']):
                if (sp2['B'] == 'null'):
                    tx_win = 'Попередження про неможливість виконання запущеної команди'
                    tx_mes = 'На жаль, обрані Вами ресурси для набору даних:\n\n- ' + sp2['C'] +\
                             '\n\nне можуть бути опубліковані через відсутність набору на порталі, або через те, що у' \
                             ' реєстрі наборів даних немає його ID.\n\nДля вирішення проблеми Вам необхідно за допомогою' \
                             ' відповідних команд даної програми або клонувати потрібний набір на портал, або відредагувати' \
                             ' реєстр наборів даних, внісши в нього ID для необхідного набору'
                    univ_message(tx_win, tx_mes, QMessageBox.Warning)
                    return
                for sp3 in res_reg:
                    if ((sp3['A'] == sp2['A']) and (sp1['file'] == sp3['D'])):
                        if (sp3['C'] != 'null'):
                            msg2 = QMessageBox()
                            msg2.setIcon(QMessageBox.Information)
                            w_titl = 'УВАГА! Визначтесь, що робити з ресурсом: ' + sp3['E']
                            msg2.setWindowTitle(w_titl)
                            msg2.setWindowIcon(QIcon('profile\logo.png'))
                            text1 = 'На порталі у Вас вже існує ресурс:\n- ' + sp3['E'] + \
                                    '\nТому, якщо Ви виконаєте дану команду без спеціальних попередніх дій, то просто' \
                                    ' отримаєте дублікат вже існуючого ресурсу.'
                            msg2.setText(text1)
                            text2 = 'Щоб цього не сталося, Вам за допомогою команди «Експорт шаблонів» в меню «Формування' \
                                    ' даних» слід спочатку клонувати набір з вищезгаданим ресурсом, змінити стандартну назву' \
                                    ' ресурсу на бажану, а потім тільки публікувати його на порталі за допомогою даної команди.'
                            msg2.setInformativeText(text2)
                            okButton2 = msg2.addButton(' Скасовуємо цю команду ', QMessageBox.AcceptRole)
                            msg2.addButton(' Вже зроблено. Продовжуємо далі ', QMessageBox.RejectRole)
                            msg2.exec()
                            if (msg2.clickedButton() == okButton2): return
                        st1 = sp3['D'] + 'Formatter'
                        fin_res.append(dict(A=sp3['A'], B=sp2['B'], C=sp3['C'], D1=sp3['D'], D2=st1,
                                            E=sp3['E'], F=sp3['F'], G=sp3['G'], url='url'))
    self.pbar.setValue(20)
    l1 = len(fin_res); fold1 = 'fold'
    pb_step = round(60 / l1)
    pb = 20
    for i in range(l1):
        pb = pb + pb_step
        self.pbar.setValue(pb)
        fold = fin_res[i]['A']; fil_name = fin_res[i]['D2']
        if (fold != fold1):
            for f in self.isx_list:
                if (f['folder'] == fold):
                    fold_id = f['id'];
                    fold1 = fold; break
        searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
        results = self.pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
        fnumb = len(results.get('files', []))
        for f in range(fnumb):
            f_n = results.get('files', [])[f]['name']
            if (f_n == fil_name):
                file_id = results.get('files', [])[f]['id']
                sh_met = pers_sheet.spreadsheets().get(spreadsheetId=file_id).execute()
                properties = sh_met.get('sheets')
                for item in properties:
                    title = item.get("properties").get('title')
                    titl1 = title.lower(); titl2 = fin_res[i]['D1'].lower()
                    if (titl1 == titl2):
                        sheet_id = item.get("properties").get('sheetId')
                        st_url = 'https://docs.google.com/spreadsheets/d/' + file_id + '/export?format=csv&id=' + \
                                 file_id + '&gid=' + str(sheet_id)
                        fin_res[i]['url'] = st_url
                        break
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    key_api = mas1['key_api_steward']
    path = mas1['baseLinkWebsite'] + '/api/3/action/resource_create'
    l1 = len(fin_res)
    self.pbar.setValue(90)
    for i in range(l1):
        data = {
            'package_id': fin_res[i]['B'],
            'url': fin_res[i]['url'],
            'name': fin_res[i]['E'],
            'description': fin_res[i]['F'],
            'format': 'CSV',
        }
        headers = {'X-CKAN-API-Key': key_api}
        response = requests.post(path, data=data, headers=headers)
        response_dict = json.loads(response.content)
        flag = response_dict['success']
        if (flag):
            l2 = len(res_reg)
            for j in range(l2):
                if ((res_reg[j]['A'] == fin_res[i]['A']) and (res_reg[j]['D'] == fin_res[i]['D1'])):
                    rs1 = response_dict['result']
                    res_reg[j]['B'] = fin_res[i]['B']
                    res_reg[j]['C'] = rs1['id']
    for rs2 in res_reg:
        if (rs2['B'] == 'null'): rs2['B'] = ''
        if (rs2['C'] == 'null'): rs2['C'] = ''
        if (rs2['D'] == 'null'): rs2['D'] = ''
        if (rs2['E'] == 'null'): rs2['E'] = ''
        if (rs2['F'] == 'null'): rs2['F'] = ''
        if (rs2['G'] == 'null'): rs2['G'] = ''
        m_rs = [rs2['A'], rs2['B'], rs2['C'], rs2['D'], rs2['E'], rs2['F'], rs2['G']]
        res_new.append(m_rs)
    cell_range = 'Введення даних!A3:G'
    self.pbar.setValue(100)
    # pers_sheet = work_sheet()
    response = pers_sheet.spreadsheets().values().clear(spreadsheetId=id2_reg, range=cell_range).execute()
    cell_range = 'Введення даних!A3:G' + str(2 + len(res_new))
    zn = {'values': res_new}
    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id2_reg, range=cell_range,
                                                         valueInputOption='RAW', body=zn).execute()
    return

# Функция обновления наборов данных, размещенных на портале для онлайн доступа
def upd_dset(self, dset_reg, id_reg):
    s_set = [] # список для выбранных наборов данны
    dataset = [] # Массив сведений для создания на портале выбранных наборв данных
    dset_new = [] # Массив обновленных значений реестра наборов данных
    # Формируем список из тех наборов данных, которые были выбраны для дальнейшего их обновления на портале
    n = len(self.isx_list)
    for i in range(self.spisok2.count()):
        name1 = self.spisok2.item(i).text()
        l1 = len(self.full_list)
        for i1 in range(l1):
            if ((self.full_list[i1]['name'] == name1) and (self.full_list[i1]['metka'] != 'groups')):
                s_set.append(dict(folder=self.full_list[i1]['metka']))
                break
    # Формируем все необходимые сведения для обновления выбранных наборов данных на портале
    for st in s_set:
        metka1 = 0
        for rec in dset_reg:
            if (st['folder'] == rec['A']):
                if (rec['B'] == 'null'):
                    tx_win = 'Попередження про неможливість виконання запущеної команди'
                    tx_mes = 'У Вас поки що немає на порталі такого набору даних, як:\n\n - ' + rec['C']\
                             + '\n\nТому, оновлення вищеназваного набору зараз неможливо.'
                    univ_message(tx_win, tx_mes, QMessageBox.Warning)
                    return
                name_str = rec['B']
                title_str = rec['C']
                if (len(title_str)>254): title_str = title_str[0:253]
                notes_str = rec['D']
                if (len(notes_str) > 400): notes_str = notes_str[0:399]
                tag_str = rec['F']
                if (len(tag_str) > 400): tag_str = notes_str[0:399]
                purp_coll = rec['G']
                if (len(purp_coll) > 400): purp_coll = notes_str[0:399]
                up_fr = rec['E']
                if (up_fr == 'Щодня'): up_fr = 'once a day'
                if (up_fr == 'Щотижня'): up_fr = 'once a week'
                if (up_fr == 'Щомісяця'): up_fr = 'once a month'
                if (up_fr == 'Щокварталу'): up_fr = 'once a quarter'
                if (up_fr == 'Кожні півроку'): up_fr = 'once a half year'
                if (up_fr == 'Щороку'): up_fr = 'once a year'
                if (up_fr == 'Відразу після внесення змін'): up_fr = 'immediately after making changes'
                if (up_fr == 'Більше одного разу на день'): up_fr = 'more than once a day'
                if (up_fr == 'Позапланово'): up_fr = 'unscheduled'
                lang = rec['J'];
                if (lang == 'Українська'): lang = 'ua'
                if (lang == 'Російська'): lang = 'ru'
                if (lang == 'Англійська'): lang = 'en'
                if (lang == 'Румунська'): lang = 'ro'
                if (lang == 'Угорська'): lang = 'hu'
                if (lang == 'Болгарська'): lang = 'bg'
                if (lang == 'Польська'): lang = 'pl'
                dataset.append(dict(folder=rec['A'], name=name_str, title=title_str, notes=notes_str, tag=tag_str, maintainer=rec['M'],
                                    m_email=rec['N'], purpose_collecting=purp_coll, up_frequency=up_fr, language=lang,
                                    publisherIdentifier=rec['L']))
                metka1 = 1; break
        if (metka1 == 0):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Деякі вибрані Вами набори даних відсутні у відповідному реєстрі, тому попередньо Вам слід:\n1. Створити' \
                     ' відповідні набори даних за допомогою команди «Створення наборів даних» в меню «Публікація даних».\n2.' \
                     ' Внести бажані зміни в ті паспорта необхідних Вам наборів даних, які розміщені у Вашому індивідуальному' \
                     ' сховище.\n3. Сформувати спеціальний реєстр всіх наборів даних, розміщених у Вас в вищеназваному сховищі' \
                     ' за допомогою команди «Формування реєстру наборів даних» в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            return
    # Обновляем выбранные наборы данных на портале
    pb_step = round(80 / len(dataset))
    pb = pb_step
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    key_api = mas1['key_api_steward']
    organization = mas1['organization_id']
    path1 = mas1['baseLinkWebsite'] + '/api/3/action/package_update'
    path2 = mas1['baseLinkWebsite'] + '/dataset/'
    l1 = len(dset_reg)
    pers_sheet = work_sheet()
    for d_st in dataset:
        pb = pb + pb_step
        self.pbar.setValue(pb)
        data_dict = {
            'name': d_st['name'],
            'title': d_st['title'],
            'notes': d_st['notes'],
            'tag_string': str_valid(d_st['tag']),
            'owner_org': organization,
            'maintainer': d_st['maintainer'],
            'maintainer_email': d_st['m_email'],
            'extras': [
                {'key': 'purpose_of_collecting_information', 'value': d_st['purpose_collecting']},
                {'key': 'update_frequency', 'value': d_st['up_frequency']},
                {'key': 'language', 'value': d_st['language']},
                {'key': 'publisherIdentifier', 'value': d_st['publisherIdentifier']}]
        }
        data = str(json.dumps(data_dict))
        headers = {'Authorization': key_api,
                   'Content-Type': 'application/json'}
        response = requests.post(path1, headers=headers, data=data)
        response_dict = json.loads(response.content)
        flag = response_dict['success']
        if (flag):
            for i in range(l1):
                if (dset_reg[i]['A'] == d_st['folder']):
                    dset_reg[i]['B'] = d_st['name']
                    dset_reg[i]['H'] = path2 + d_st['name']
                    dset_reg[i]['I'] = 'CSV'
    for ds in dset_reg:
        if (ds['B'] == 'null'): ds['B'] = ''
        if (ds['C'] == 'null'): ds['C'] = ''
        if (ds['D'] == 'null'): ds['D'] = ''
        if (ds['E'] == 'null'): ds['E'] = ''
        if (ds['F'] == 'null'): ds['F'] = ''
        if (ds['G'] == 'null'): ds['G'] = ''
        if (ds['H'] == 'null'): ds['H'] = ''
        if (ds['I'] == 'null'): ds['I'] = ''
        if (ds['J'] == 'null'): ds['J'] = ''
        if (ds['K'] == 'null'): ds['K'] = ''
        if (ds['L'] == 'null'): ds['L'] = ''
        if (ds['M'] == 'null'): ds['M'] = ''
        if (ds['N'] == 'null'): ds['N'] = ''
        ds1 = [ds['A'], ds['B'], ds['C'], ds['D'], ds['E'], ds['F'], ds['G'], ds['H'], ds['I'], ds['J'], ds['K'], ds['L'],
               ds['M'], ds['N']]
        dset_new.append(ds1)
    self.pbar.setValue(100)
    cell_range = 'Введення даних!A3:N'
    response = pers_sheet.spreadsheets().values().clear(spreadsheetId=id_reg, range=cell_range).execute()
    cell_range = 'Введення даних!A3:N' + str(2 + len(dset_new))
    zn = {'values': dset_new}
    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_reg, range=cell_range,
                                                         valueInputOption='RAW', body=zn).execute()

# Функция проверки и загрузки значений из реестра ресурсов наборов данных в словарь с последующим обновлением описаний
# этих ресурсов на портале
def upd_resource(self, fold_id):
    # fold_id - ID папки, по которой нам необходимо найти данные
    # id1_reg - ID файла registerFormatter
    # id2_reg - ID файла resourceRegistryFormatter
    # res_reg - Массив информации из реестра ресурсов наборов данных
    # fin_res - Массив информации по выбранным ресурсам, которые следует опубликовать на портале
    res_new = []  # Массив обновленных значений реестра ресурсов наборов данных
    m_ds = [] # Массив для папок и ID наборов данных, уже созданных на портале
    res_reg = [] # Сведения о ресурсах наборах данных, которые находятся в реестре
    fin_res = [] # Итоговый результат данных, которые будут использованы для публикации ресурсов
    msg2 = QMessageBox()
    msg2.setIcon(QMessageBox.Information)
    msg2.setWindowTitle('Інформація про призначення команди щодо оновлення ресурсів наборів даних')
    msg2.setWindowIcon(QIcon('profile\logo.png'))
    msg2.setText('Слід мати на увазі, що дана команда оновлює лише описи вибраних ресурсів, але не змінює самі ресурси,'
                      ' Тому, якщо Ви хочете розмістити в наборі додатковий ресурс, наприклад, з даними за новий період, то'
                      ' Вам слід вскористатися командою «Публікація ресурсів з Форматорів» в меню «Публікація даних».')
    msg2.setInformativeText('Якщо ж Ви хочете змінити назву будь-якого ресурсу (наприклад, поміняти List2019 на List2019-2020)'
                            ' або змінити його опис, то дана команда якраз для цього і призначена. Але, потрібно пам\'ятати,'
                            ' що попередньо, крім зміни опису ресурсу необхідно ще й оновити відповідний реєстр за допомогою'
                            ' команди «Формування реєстру ресурсів» в меню «Налаштування програми».')
    okButton2 = msg2.addButton(' Продовжувати виконання команди ', QMessageBox.AcceptRole)
    msg2.addButton(' Вийти з команди ', QMessageBox.RejectRole)
    msg2.exec()
    if (msg2.clickedButton() != okButton2): return
    self.pbar.setValue(10)
    searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    results = self.pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        f_name = results.get('files', [])[f]['name']
        if (f_name == 'registerFormatter'):
            id1_reg = results.get('files', [])[f]['id']; name1_reg = f_name
        if (f_name == 'resourceRegistryFormatter'):
            id2_reg = results.get('files', [])[f]['id']; name2_reg = f_name
    # Формируем массив со сведениями об уже имеющихся ID в реестре наборов данных
    pers_sheet = work_sheet()
    cell_range = 'Register!A2:C'
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=id1_reg, range=cell_range).execute()
    values = result.get('values', [])
    for st in values:
        m_ds.append(dict(A=st[0], B=st[1], C=st[2]))
    # Формируем массив со сведениями об уже имеющихся данных в реестре ресурсов наборов данных
    cell_range = 'ResourceRegistry!A2:G'
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=id2_reg, range=cell_range).execute()
    values = result.get('values', [])
    for st in values:
        res_reg.append(dict(A=st[0], B=st[1], C=st[2], D=st[3], E=st[4], F=st[5], G=st[6]))
    if (len(res_reg) == 0):
        tx_win = 'Попередження про неможливість виконання запущеної команди'
        tx_mes = 'Для оновлення ресурсів наборів даних на порталі Ви маєте спочатку:\n1. Опублікувати відповідні' \
                 ' ресурси наборів даних за допомогою команди «Публікація ресурсів з Форматорів» в меню «Публікація даних».\n2.' \
                 ' Внести бажані зміни в ті описи ресурсів наборів даних, які розміщені у Вашому індивідуальному сховище.\n3.' \
                 ' Сформувати спеціальний реєстр всіх ресурсів наборів даних, розміщених у Вас в вищеназваному сховищі за допомогою' \
                 ' команди «Формування реєстру ресурсів» в меню «Налаштування програми».'
        univ_message(tx_win, tx_mes, QMessageBox.Warning)
        return
    for sp1 in self.act_l:
        for sp2 in m_ds:
            if (sp2['A'] == sp1['folder']):
                if (sp2['B'] == 'null'):
                    tx_win = 'Попередження про неможливість виконання запущеної команди'
                    tx_mes = 'На жаль, обрані Вами ресурси для набору даних:\n\n- ' + sp2['C'] +\
                             '\n\nне можуть бути опубліковані через відсутність набору на порталі, або через те, що у' \
                             ' реєстрі наборів даних немає його ID.\n\nДля вирішення проблеми Вам необхідно за допомогою' \
                             ' відповідних команд даної програми або клонувати потрібний набір на портал, або відредагувати' \
                             ' реєстр наборів даних, внісши в нього ID для необхідного набору'
                    univ_message(tx_win, tx_mes, QMessageBox.Warning)
                    return
                for sp3 in res_reg:
                    if ((sp3['A'] == sp2['A']) and (sp1['file'] == sp3['D'])):
                        if (sp3['C'] == 'null'):
                            tx_win = 'Попередження про неможливість виконання запущеної команди'
                            tx_mes = 'У Вас поки що немає на порталі такого ресурсу, як:\n\n - ' + sp3['E'] +\
                                     '\n\nТому, оновлення вищеназваного ресурсу зараз неможливо.'
                            univ_message(tx_win, tx_mes, QMessageBox.Warning)
                            return
                        st1 = sp3['D'] + 'Formatter'
                        fin_res.append(dict(A=sp3['A'], B=sp2['B'], C=sp3['C'], D1=sp3['D'], D2=st1,
                                            E=sp3['E'], F=sp3['F'], G=sp3['G'], url='url'))
    self.pbar.setValue(20)
    l1 = len(fin_res); fold1 = 'fold'
    pb_step = round(60 / l1)
    pb = 20
    for i in range(l1):
        pb = pb + pb_step
        self.pbar.setValue(pb)
        fold = fin_res[i]['A']; fil_name = fin_res[i]['D2']
        if (fold != fold1):
            for f in self.isx_list:
                if (f['folder'] == fold):
                    fold_id = f['id'];
                    fold1 = fold; break
        searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
        results = self.pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
        fnumb = len(results.get('files', []))
        for f in range(fnumb):
            f_n = results.get('files', [])[f]['name']
            if (f_n == fil_name):
                file_id = results.get('files', [])[f]['id']
                sh_met = pers_sheet.spreadsheets().get(spreadsheetId=file_id).execute()
                properties = sh_met.get('sheets')
                for item in properties:
                    title = item.get("properties").get('title')
                    titl1 = title.lower(); titl2 = fin_res[i]['D1'].lower()
                    if (titl1 == titl2):
                        sheet_id = item.get("properties").get('sheetId')
                        st_url = 'https://docs.google.com/spreadsheets/d/' + file_id + '/export?format=csv&id=' + \
                                 file_id + '&gid=' + str(sheet_id)
                        fin_res[i]['url'] = st_url
                        break
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    key_api = mas1['key_api_steward']
    path = mas1['baseLinkWebsite'] + '/api/3/action/resource_update'
    l1 = len(fin_res)
    self.pbar.setValue(90)
    for i in range(l1):
        data = {
            'id': fin_res[i]['C'],
            'url': fin_res[i]['url'],
            'name': fin_res[i]['E'],
            'description': fin_res[i]['F'],
            'format': 'CSV',
        }
        headers = {'X-CKAN-API-Key': key_api}
        response = requests.post(path, data=data, headers=headers)
        response_dict = json.loads(response.content)
        flag = response_dict['success']
        if (flag):
            l2 = len(res_reg)
            for j in range(l2):
                if ((res_reg[j]['A'] == fin_res[i]['A']) and (res_reg[j]['D'] == fin_res[i]['D1'])):
                    rs1 = response_dict['result']
                    res_reg[j]['B'] = fin_res[i]['B']
                    res_reg[j]['C'] = rs1['id']
    for rs2 in res_reg:
        if (rs2['B'] == 'null'): rs2['B'] = ''
        if (rs2['C'] == 'null'): rs2['C'] = ''
        if (rs2['D'] == 'null'): rs2['D'] = ''
        if (rs2['E'] == 'null'): rs2['E'] = ''
        if (rs2['F'] == 'null'): rs2['F'] = ''
        if (rs2['G'] == 'null'): rs2['G'] = ''
        m_rs = [rs2['A'], rs2['B'], rs2['C'], rs2['D'], rs2['E'], rs2['F'], rs2['G']]
        res_new.append(m_rs)
    cell_range = 'Введення даних!A3:G'
    self.pbar.setValue(100)
    # pers_sheet = work_sheet()
    response = pers_sheet.spreadsheets().values().clear(spreadsheetId=id2_reg, range=cell_range).execute()
    cell_range = 'Введення даних!A3:G' + str(2 + len(res_new))
    zn = {'values': res_new}
    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id2_reg, range=cell_range,
                                                         valueInputOption='RAW', body=zn).execute()
    return
