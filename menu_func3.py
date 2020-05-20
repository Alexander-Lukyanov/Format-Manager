# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMessageBox, QGroupBox, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton)
from univ_func import (connect_lib, connect_storage, list_building, init_dil1, univ_message, work_sheet, decl_words,
                       main_screen, load_dat, univ_dialog)
from menu_func1 import klon_set
import webbrowser
import json
import csv

# Функция создающая сообщение о необходимости клонирования базового набора данных с реестрами и основными сведениями
# по распорядителю
def create_msg3():
    msg3 = QMessageBox()
    msg3.setIcon(QMessageBox.Information)
    msg3.setWindowTitle('Повідомлення щодо необхідності клонування конфігураційних файлів')
    msg3.setWindowIcon(QIcon('profile\logo.png'))
    msg3.setInformativeText('Без цих файлів неможлива подальша робота даної програми, тому настійливо рекомендується'
                            ' натиснути кнопку «Клонувати файли» та почекати поки до Вашого сховища клонуються'
                            ' відповідні файли.')
    okButton3 = msg3.addButton(' Клонувати файли ', QMessageBox.AcceptRole)
    msg3.addButton(' Здійснити дію пізніше ', QMessageBox.RejectRole)
    return msg3, okButton3

# Функция, которая позволяет организовать либо клонирование базового набора с реестрами либо ввести в соответствующий
# файл этого набора основные сведения по распорядителю
def works_007(self, fold, fold_id):
    # fold - имя папки, по которой нам необходимо собрать данные
    # fold_id - ID папки, по которой нам необходимо найти данные
    stand_fil = []  # Список стандартных файлов, присущих выбранному набору данных
    act_file = []  # Фактические сведения о файлах, имеющихся в папке выбранного набор данных
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    root_folder = mas1['license']  # Определяем корневую папку индивидуального хранилища пользователя
    # root_id - ID для корневой папки индивидуального хранилища польователя
    s_set = []  # сведения о наборе данных с конфигурационными файлами на общем диске
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    if (fold_id == '0'):
        self.msg3, self.okButton3 = create_msg3()
        self.msg3.setText('У вашому індивідуальному сховище поки ще відсутні файли, що містять відомості про Вашу'
                          ' організацію , а також реєстри з інформацією про її набори даних та ресурси.')
        self.msg3.exec()
        if (self.msg3.clickedButton() == self.okButton3):  # Клонируем конфигурационные файлы
            for f in range(fnumb):
                if (results.get('files', [])[f]['name'] == root_folder):
                    root_id = results.get('files', [])[f]['id']; break
            shared_disk = connect_lib()  # Функция подключения к общему диску
            isx_list = list_building(shared_disk)  # Функция формирования списка набора данных
            n = len(isx_list)
            for j in range(n):
                if (fold == isx_list[j]['folder']):
                    s_set.append(dict(id=isx_list[j]['id'], folder=isx_list[j]['folder'], set='')); break
            self.pbar.setValue(50)
            klon_set(shared_disk, pers_account, root_id, s_set[0])
            self.pbar.setValue(100)
            results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
            fnumb = len(results.get('files', []))
            for f in range(fnumb):
                if (results.get('files', [])[f]['name'] == fold):
                    fold_id = results.get('files', [])[f]['id']; break
        if (self.msg3.clickedButton() != self.okButton3): return 'відмова'

    # Собираем нормативные сведения о файлах искомого набора данных
    with open('profile\standard_dataset_files.csv', 'r', encoding='utf-8') as f_csv:
        reader = csv.DictReader(f_csv, delimiter=',')
        for st in reader:
            if (st['folder'] == fold):
                stand_fil.append(dict(folder=st['folder'], type=st['file_type'], file=st['file_name'], description=st['file_description']))
    searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    # Собираем фактические сведения о файлах выбранного набора данных
    for f in range(fnumb):
        act_file.append(dict(id=results.get('files', [])[f]['id'], name=results.get('files', [])[f]['name']))
    # Находим нужный нам файл и запускаем его в браузере
    l1 = len(stand_fil)
    l2 = len(act_file)
    for i in range(l1):
        for j in range(l2):
            if (stand_fil[i]['file'] == act_file[j]['name'] and act_file[j]['name'] == 'identificationData'):
                file_id = act_file[j]['id']
                url1 = 'https://docs.google.com/spreadsheets/d/' + file_id
                break
    webbrowser.open_new_tab(url1)
    # Выводим серию сообщений для того, чтобы организовать надлежащий ввод данных в нужный нам файл
    tx_win = 'Будь ласка, заповніть таблицю з відомостями щодо розпорядника'
    tx_mes = 'Заповніть або відкоригуйте в браузері, що відкрився, всі необхідні відомості по розпоряднику' \
             ' інформації і, тільки потім перейдіть назад в дану програму та натисніть в цьому вікні' \
             ' повідомлень кнопку «OK».'
    univ_message(tx_win, tx_mes, QMessageBox.Information)
    cell_range = 'Дані розпорядника інформації!C2:C15'
    pers_sheet = work_sheet()
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=file_id, range=cell_range).execute()
    values = result.get('values', [])
    tx_win = 'Попередження про не до кінця заповнені відомості про розпорядника'
    j = 1; j1 = 1
    while j == 1:
        j = 0
        tx_mes = 'УВАГА! У таблицю з основними відомостями про розпорядники інформації Ви не внесли следеющіе дані:\n'
        tx_m = ''
        for i in range(11): # перебираем значения в дапозоне нужных нам ячеек
            if (not values[i]):
                if (i == 0): j = 1; tx_m = tx_m + '- Назва установи розпорядника інформації\n'
                if (i == 1): j = 1; tx_m = tx_m + '- Код ЄДРПОУ\n'
                if (i == 2): j = 1; tx_m = tx_m + '- Код КОАТУУ\n'
                if (i == 3): j = 1; tx_m = tx_m + '- Територія, де функціонує установа\n'
                if (i == 4): j = 1; tx_m = tx_m + '- Тип установи розпорядника інформації\n'
                if (i == 5): j = 1; tx_m = tx_m + '- Код економічної діяльності\n'
                if (i == 6): j = 1; tx_m = tx_m + '- ПІБ Керівника структури, яка є розпорядником інформації\n'
                if (i == 7): j = 1; tx_m = tx_m + '- ПІБ відповідальної особи розпорядника інформації\n'
                if (i == 9): j = 1; tx_m = tx_m + '- Email установи розпорядника інформації\n'
                if (i == 10): j = 1; tx_m = tx_m + '- Email відповідальної особи\n'
        if (j == 1):
            tx_mes = tx_mes + '\n' + tx_m + '\n' + 'Поверніться, будь ласка, назад в браузер і заповніть відповідні' \
                                                   ' комірки необхідними значеннями. Після цього перейдіть знову в' \
                                                   ' програму і натисніть в даному вікні повідомлень кнопку «ОК».\n\n' \
                                                   'У разі відмови від процесу внесення основних відомостей щодо' \
                                                   ' розпорядника інформації, натисніть кнопку «Відміна».'
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle(tx_win)
            msg.setWindowIcon(QIcon('profile\logo.png'))
            msg.setInformativeText(tx_mes)
            okButton = msg.addButton(' OK ', QMessageBox.AcceptRole)
            msg.addButton(' Відміна ', QMessageBox.RejectRole)
            msg.exec()
            if (msg.clickedButton() != okButton):
                j = 0; j1 = 0; continue
            result = pers_sheet.spreadsheets().values().get(spreadsheetId=file_id, range=cell_range).execute()
            values = result.get('values', [])
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    if (j1 == 1):
        mas1['publisherName'] = values[0][0]
        mas1['publisherIdentifier'] = values[1][0]
        mas1['publisherTerritory'] = values[3][0]
        mas1['contactPointFn'] = values[7][0]
        mas1['contactPointHasEmail'] = values[10][0]
        tx1 = mas1['publisherName']
        tx = decl_words(tx1, 'gent')
        mas1['publisherNameRod'] = tx
        tx = decl_words(tx1, 'ablt')
        mas1['publisherNameTvor'] = tx
        tx = decl_words(tx1, 'datv')
        mas1['publisherNameDat'] = tx
        tx = decl_words(tx1, 'accs')
        mas1['publisherNameVin'] = tx
        tx1 = mas1['publisherTerritory']
        tx = decl_words(tx1, 'gent')
        mas1['publisherTerritoryRod'] = tx
        data_us = json.dumps(mas1, indent=2, ensure_ascii=False)
        with open('profile\data_users.json', 'w', encoding='utf-8') as file:
            file.write(data_us)
            file.close()
    tx = mas1['publisherNameTvor']
    titl_win = 'Менеджер з оприлюднення відкритих даних наданих «' + tx + '»'
    return titl_win

def win3_2(self):
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    # Создаем рамку с полями для ввода кодов, обеспечивающих обнародование наборов распорядителя на портале data.gov.ua
    font = QtGui.QFont()
    font.setPointSize(10)
    self.box1 = QGroupBox('ОСНОВНІ КОДИ РОЗПОРЯДНИКА ІНФОРМАЦІЇ, ЩО ДАЮТЬ ЙОМУ МОЖЛИВІСТЬ ОПРИЛЮДНЕННЯ НАБОРІВ ДАНИХ'
                          ' НА ПОРТАЛІ DATA.GOV.UA')
    self.box1.setFont(font)
    self.box1.setAlignment(QtCore.Qt.AlignCenter)
    self.vbox1 = QVBoxLayout()
    self.box1.setLayout(self.vbox1)
    # Создаем необходимые пояснения, метки и поля для ввода кодов, обеспечивающих обнародование данных на портале
    self.help1 = QLabel(self)
    self.help1.setText('Вкажіть в двох ніжеразмещенних полях цієї групи наступні дані:\n - Для поля «API ключ розпорядника'
                       ' інформації» вказується код, який можна знайти в нижній частині лівої колонки сторінки з Вашими'
                       ' наборами даних на порталі data.gov.ua\n   Наприклад, 8717cb76-d55c-466d-9d2f-aaf5abd9c26c\n'
                       ' - Для поля «ID установи розпорядника інформації» вказується код або транслітерована назва установи,'
                       ' які можна знайти на сторінці з Вашим профілем на порталі data.gov.ua\n   Наприклад, odeska-oblasna-rada')
    self.hhbox1 = QHBoxLayout()
    self.hhbox1.addStretch(1)
    self.hhbox1.addWidget(self.help1)
    self.hhbox1.addStretch(1)
    self.vbox1.addSpacing(15)
    self.vbox1.addLayout(self.hhbox1)
    self.vbox1.addSpacing(15)
    self.metka1 = QLabel(self)
    self.metka1.setText('API ключ розпорядника інформації')
    self.linEd1 = QLineEdit(self)
    self.linEd1.setText(mas1['key_api_steward'])
    self.hbox0 = QHBoxLayout()
    self.hbox0.addSpacing(25)
    self.hbox0.addWidget(self.metka1)
    self.hbox0.addSpacing(17)
    self.hbox0.addWidget(self.linEd1)
    self.hbox0.addSpacing(25)
    self.vbox1.addLayout(self.hbox0)
    self.metka2 = QLabel(self)
    self.metka2.setText('ID установи розпорядника інформації')
    self.linEd2 = QLineEdit(self)
    self.linEd2.setText(mas1['organization_id'])
    self.hbox1 = QHBoxLayout()
    self.hbox1.addSpacing(25)
    self.hbox1.addWidget(self.metka2)
    self.hbox1.addWidget(self.linEd2)
    self.hbox1.addSpacing(25)
    self.vbox1.addLayout(self.hbox1)
    # Создаем рамку с вариантами склонения названия учреждения распорядителя информации
    self.box2 = QGroupBox('ВАРІАНТИ ВІДМІНЮВАННЯ НАЗВИ УСТАНОВИ РОЗПОРЯДНИКА ІНФОРМАЦІЇ З МЕТОЮ ЇХ МОЖЛИВОГО КОРЕКТУВАННЯ'
                          ' ДЛЯ НАЛЕЖНОГО ФОРМУВАННЯ ПАСПОРТІВ НАБОРІВ ДАНИХ ТА ЇХ РЕСУРСІВ')
    self.box2.setFont(font)
    self.box2.setAlignment(QtCore.Qt.AlignCenter)
    self.vbox2 = QVBoxLayout()
    self.box2.setLayout(self.vbox2)
    # Создаем необходимые пояснения, метки и поля для корректировки вариантов склонения названия учреждения распорядителя
    self.help2 = QLabel(self)
    self.help2.setText('У разі виявлення можливих помилок в варіантах програмного (автоматичного) відмінювання назви'
                       ' установи розпорядника інформації, внесіть, будь ласка,\nу відповідні поля з варіантами'
                       ' п\'ятьох відмінкових відмінювань необхідні корегування.')
    self.hhbox2 = QHBoxLayout()
    self.hhbox2.addStretch(1)
    self.hhbox2.addWidget(self.help2)
    self.hhbox2.addStretch(1)
    self.vbox2.addSpacing(15)
    self.vbox2.addLayout(self.hhbox2)
    self.vbox2.addSpacing(15)
    self.metka3 = QLabel(self)
    self.metka3.setText('Назва установи розпорядника інформації у НАЗИВНОМУ ВІДМІНКУ')
    self.linEd3 = QLineEdit(self)
    self.linEd3.setText(mas1['publisherName'])
    self.hbox2 = QHBoxLayout()
    self.hbox2.addSpacing(25)
    self.hbox2.addWidget(self.metka3)
    self.hbox2.addSpacing(12)
    self.hbox2.addWidget(self.linEd3)
    self.hbox2.addSpacing(25)
    self.vbox2.addLayout(self.hbox2)
    self.metka4 = QLabel(self)
    self.metka4.setText('Назва установи розпорядника інформації у РОДОВОМУ ВІДМІНКУ')
    self.linEd4 = QLineEdit(self)
    self.linEd4.setText(mas1['publisherNameRod'])
    self.hbox3 = QHBoxLayout()
    self.hbox3.addSpacing(25)
    self.hbox3.addWidget(self.metka4)
    self.hbox3.addSpacing(16)
    self.hbox3.addWidget(self.linEd4)
    self.hbox3.addSpacing(25)
    self.vbox2.addLayout(self.hbox3)
    self.metka5 = QLabel(self)
    self.metka5.setText('Назва установи розпорядника інформації в ОРУДНОМУ ВІДМІНКУ')
    self.linEd5 = QLineEdit(self)
    self.linEd5.setText(mas1['publisherNameTvor'])
    self.hbox4 = QHBoxLayout()
    self.hbox4.addSpacing(25)
    self.hbox4.addWidget(self.metka5)
    self.hbox4.addSpacing(16)
    self.hbox4.addWidget(self.linEd5)
    self.hbox4.addSpacing(25)
    self.vbox2.addLayout(self.hbox4)
    self.metka6 = QLabel(self)
    self.metka6.setText('Назва установи розпорядника інформації у ДАВАЛЬНОМУ ВІДМІНКУ')
    self.linEd6 = QLineEdit(self)
    self.linEd6.setText(mas1['publisherNameDat'])
    self.hbox5 = QHBoxLayout()
    self.hbox5.addSpacing(25)
    self.hbox5.addWidget(self.metka6)
    self.hbox5.addWidget(self.linEd6)
    self.hbox5.addSpacing(25)
    self.vbox2.addLayout(self.hbox5)
    self.metka7 = QLabel(self)
    self.metka7.setText('Назва установи розпорядника інформації у ЗНАХІДНОМУ ВІДМІНКУ')
    self.linEd7 = QLineEdit(self)
    self.linEd7.setText(mas1['publisherNameVin'])
    self.hbox6 = QHBoxLayout()
    self.hbox6.addSpacing(25)
    self.hbox6.addWidget(self.metka7)
    self.hbox6.addSpacing(12)
    self.hbox6.addWidget(self.linEd7)
    self.hbox6.addSpacing(25)
    self.vbox2.addLayout(self.hbox6)
    # Создаем рамку с вариантами склонения названия территории, где будут собираться сведения для формирования наборов данных
    self.box3 = QGroupBox('ВАРІАНТИ ВІДМІНЮВАННЯ НАЗВИ ТЕРИТОРІЇ, ДЕ ФУНКЦІОНУЄ УСТАНОВА РОЗПОРЯДНИКА ІНФОРМАЦІЇ ТА В'
                          ' МЕЖАХ ЯКОЇ ПОВИННІ БУДУТЬ ФОРМУВАТИСЯ НАБОРИ ДАНИХ')
    self.box3.setFont(font)
    self.box3.setAlignment(QtCore.Qt.AlignCenter)
    self.vbox3 = QVBoxLayout()
    self.box3.setLayout(self.vbox3)
    # Создаем необходимые пояснения, метки и поля для ввода кодов, обеспечивающих обнародование данных на портале
    self.help3 = QLabel(self)
    self.help3.setText('З метою належного формування паспортів наборів даних і їх ресурсів та у разі виявлення можливих'
                       ' помилок в варіантах програмного (автоматичного) відмінювання назви\nтериторі, в межах якої'
                       ' повинні будуть формуватися набори даних, внесіть, будь ласка, у відповідні поля з варіантами'
                       ' двох відмінкових відмінювань необхідні корегування.')
    self.hhbox3 = QHBoxLayout()
    self.hhbox3.addStretch(1)
    self.hhbox3.addWidget(self.help3)
    self.hhbox3.addStretch(1)
    self.vbox3.addSpacing(15)
    self.vbox3.addLayout(self.hhbox3)
    self.vbox3.addSpacing(15)
    self.metka8 = QLabel(self)
    self.metka8.setText('Назва території, де розпорядник інформації формує набори даних у НАЗИВНОМУ ВІДМІНКУ')
    self.linEd8 = QLineEdit(self)
    self.linEd8.setText(mas1['publisherTerritory'])
    self.hbox7 = QHBoxLayout()
    self.hbox7.addSpacing(25)
    self.hbox7.addWidget(self.metka8)
    self.hbox7.addWidget(self.linEd8)
    self.hbox7.addSpacing(25)
    self.vbox3.addLayout(self.hbox7)
    self.metka9 = QLabel(self)
    self.metka9.setText('Назва території, де розпорядник інформації формує набори даних у РОДОВОМУ ВІДМІНКУ')
    self.linEd9 = QLineEdit(self)
    self.linEd9.setText(mas1['publisherTerritoryRod'])
    self.hbox8 = QHBoxLayout()
    self.hbox8.addSpacing(25)
    self.hbox8.addWidget(self.metka9)
    self.hbox8.addSpacing(7)
    self.hbox8.addWidget(self.linEd9)
    self.hbox8.addSpacing(25)
    self.vbox3.addLayout(self.hbox8)
    # Создаем кнопку "Зберегти" и кнопку "Відмінити"
    font = QtGui.QFont()
    font.setPointSize(9)
    self.but1 = QPushButton(' Зберегти ')
    self.but1.setFont(font)
    self.but2 = QPushButton(' Відмінити ')
    self.but2.setFont(font)
    self.hbox9 = QHBoxLayout()
    self.hbox9.addStretch(1)
    self.hbox9.addWidget(self.but1)
    self.hbox9.addWidget(self.but2)
    self.hbox9.addSpacing(33)
    # Выводим группы с полями ввода в главное окно программы
    self.sly.addSpacing(35)
    self.sly.addWidget(self.box1)
    self.sly.addSpacing(20)
    self.sly.addWidget(self.box2)
    self.sly.addSpacing(20)
    self.sly.addWidget(self.box3)
    self.sly.addSpacing(5)
    self.sly.addLayout(self.hbox9)

# Функция, которая проверяет заполнение полей в рамках выполнения команды «Сведения для обнародования данных»
def check3_2(self):
    tx0 = 'Заповніть, будь ласка, наступні поля:\n\n'
    tx1 = ''
    j = 0
    if (len(self.linEd1.text()) == 0):
        tx1 = tx1 + '- API ключ розпорядника інформації\n'
    if (len(self.linEd2.text()) == 0):
        tx1 = tx1 + ' - ID установи розпорядника інформації\n'
    if (len(self.linEd3.text()) == 0):
        tx1 = tx1 + ' - Назва установи розпорядника інформації у НАЗИВНОМУ ВІДМІНКУ\n'
    if (len(self.linEd4.text()) == 0):
        tx1 = tx1 + ' - Назва установи розпорядника інформації у РОДОВОМУ ВІДМІНКУ\n'
    if (len(self.linEd5.text()) == 0):
        tx1 = tx1 + ' - Назва установи розпорядника інформації в ОРУДНОМУ ВІДМІНКУ\n'
    if (len(self.linEd6.text()) == 0):
        tx1 = tx1 + ' - Назва установи розпорядника інформації у ДАВАЛЬНОМУ ВІДМІНКУ\n'
    if (len(self.linEd7.text()) == 0):
        tx1 = tx1 + ' - Назва установи розпорядника інформації у МІСЦЕВОМУ ВІДМІНКУ\n'
    if (len(self.linEd8.text()) == 0):
        tx1 = tx1 + ' - Назва території, де розпорядник інформації формує набори даних у НАЗИВНОМУ ВІДМІНКУ\n'
    if (len(self.linEd9.text()) == 0):
        tx1 = tx1 + ' - Назва території, де розпорядник інформації формує набори даних у РОДОВОМУ ВІДМІНКУ\n'
    tx_mes = tx0 + tx1 + '\nНатисніть кнопку «ОК» для продовження заповнення (редагування) полів, або виберіть кнопку' \
                         ' «Відміна» для виходу з цієї функції програми без збереження даних'
    if (len(tx1) != 0):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Попередження про незаповнених полях для введення значень')
        msg.setWindowIcon(QIcon('profile\logo.png'))
        msg.setInformativeText(tx_mes)
        okButton = msg.addButton('OK', QMessageBox.AcceptRole)
        msg.addButton('Відміна', QMessageBox.RejectRole)
        msg.exec()
        if (msg.clickedButton() != okButton):
            main_screen(self)
        j = 1
    return j

# Функция, которая формирует реестр наборов данных с учетом сведений, имеющихся в файлах их паспортов
def dset_registr(self, fold):
    # fold - имя папки, по которой находиться реестр наборов данных
    # act_reg - ID файла реестра набора данных
    act_fold = [] # Сведения о папках наборов данных, размещенных в индивидуальном хранилище
    act_pasp = []  # Сведения о файлах паспортов, размещенных в индивидуальном хранилище
    dset_old = [] # Сведения о наборах данных, которые были в реестре до его обновления
    dset_new = []  # Сведения о наборах данных, которые будут в реестре после его обновления
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    # Собираем ID папок в индивидуальном хранилище, а также размещенные в них имена паспортов
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle('Попередження щодо тривалого процесу формування реєстру наборів даних')
    msg.setWindowIcon(QIcon('profile\logo.png'))
    msg.setText('Через періодичну завантаженість сервісів «Google» та, можливу, велику кількість наборів даних, що були'
                 ' розміщені у Вашому індивідуальному сховище, процес формування реєстру для цих наборів даних може бути'
                ' досить тривалим.')
    okButton = msg.addButton(' Зрозуміло ', QMessageBox.AcceptRole)
    msg.exec()
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        f_act = results.get('files', [])[f]['name']
        f_id_act = results.get('files', [])[f]['id']
        act_fold.append(dict(folder=f_act, id=f_id_act))
    with open('profile\content_config.csv', 'r', encoding='utf-8') as f_csv:
        reader = csv.DictReader(f_csv, delimiter=',')
        for st_n in reader:
            for st_a in act_fold:
                if (st_n['folder'] == st_a['folder']):
                    if (st_n['data_type'] == 'паспорт'):
                        searh1 = "'" + st_a['id'] + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
                        results = pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
                        fnumb = len(results.get('files', []))
                        # Собираем фактические сведения о паспотах, размещенных в индивидуальном хранилище
                        for f in range(fnumb):
                            act_name = results.get('files', [])[f]['name']
                            if (st_n['file_name'] == act_name):
                                act_pasp.append(dict(folder=st_a['folder'], id=results.get('files', [])[f]['id'],
                                                     file = st_n['file_name'], code_text = st_n['code_text'])); continue
                            if (st_n['folder'] == fold and act_name == 'registerFormatter'):
                                act_reg = results.get('files', [])[f]['id']

    # Формируем массив со сведениями об уже имеющихся данных в реестре наборов данных
    cell_range = 'Register!A2:N'
    pers_sheet = work_sheet()
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=act_reg, range=cell_range).execute()
    values = result.get('values', [])
    for st in values:
        dset_old.append(dict(A=st[0], B=st[1], C=st[2], D=st[3], E=st[4], F=st[5], G=st[6], H=st[7], I=st[8], J=st[9],
                            K=st[10], L=st[11], M=st[12], N=st[13]))

    self.pbar.setValue(10)
    pb_step = round(100 / len(act_pasp))
    pb = pb_step
    # Формируем массив с обновленными данными в реестре
    for ps in act_pasp:
        pb = pb + pb_step
        self.pbar.setValue(pb)
        b1 = ''; c1 = ''; d1 = ''; e1 = ''; f1 = ''; g1 = ''; h1 = ''; i1 = ''; j1 = ''; k1 = ''; l1 = ''; m1 = ''; n1 = ''
        # В массиве с обновленными данными учитываем данные, которые уже имелись в реестре
        for reg in dset_old:
            if (reg['A'] == ps['folder']):
                if (reg['B'] != 'null'): b1 = reg['B']
                if (reg['C'] != 'null'): c1 = reg['C']
                if (reg['D'] != 'null'): d1 = reg['D']
                if (reg['E'] != 'null'): e1 = reg['E']
                if (reg['F'] != 'null'): f1 = reg['F']
                if (reg['G'] != 'null'): g1 = reg['G']
                if (reg['H'] != 'null'): h1 = reg['H']
                if (reg['I'] != 'null'): i1 = reg['I']
                if (reg['J'] != 'null'): j1 = reg['J']
                if (reg['K'] != 'null'): k1 = reg['K']
                if (reg['L'] != 'null'): l1 = reg['L']
                if (reg['M'] != 'null'): m1 = reg['M']
                if (reg['N'] != 'null'): n1 = reg['N']
        # Формируем новые данные в реестре с учетом уже имеющихся в нем данных
        B2 = ''; B3 = ''
        if (c1 == '' or d1 == ''):
            if (ps['code_text'] == '1'): B2 = mas1['publisherNameRod']
            if (ps['code_text'] == '2'): B2 = mas1['publisherNameTvor']
            if (ps['code_text'] == '3'): B2 = mas1['publisherTerritoryRod']
            if (ps['code_text'] == '4'): B2 = mas1['publisherNameDat']
            if (ps['code_text'] == '5'): B2 = mas1['publisherNameVin']
            if (ps['code_text'] == '7'): B2 = mas1['publisherTerritoryRod']; B3 = mas1['publisherNameTvor']
            if (ps['code_text'] == '11'):
                B2 = mas1['publisherTerritoryRod']
                folder = 'all-007'; file = 'identificationData'; cell_range = 'Дані розпорядника інформації!C18'
                str1= load_dat(folder, file, cell_range); B3 = str1[0][0]
        id_pasp = ps['id']
        # Заполняем файл паспорта или же берем из этого файла значения (в приоритете) для заполнения реестра
        if (B2 != ''):
            cell_range = ps['file'] + '!B2'; zn = {'values': [[B2]]}
            response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                 valueInputOption='RAW', body=zn).execute()
        if (B3 != ''):
            cell_range = ps['file'] + '!B3'; zn = {'values': [[B3]]}
            response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                 valueInputOption='RAW', body=zn).execute()
        cell_range = ps['file'] + '!B6:B13'
        result = pers_sheet.spreadsheets().values().get(spreadsheetId=id_pasp, range=cell_range).execute()
        values = result.get('values', [])
        ln1 = len(values)
        for i in range(ln1):
            if (not values[i]): values[i] = ''
        if (ln1 < 8):
            for i in range(len(values),8):
                values.append('')
        for i in range(8):
            if (values[i] != ''):
                if (i == 0 and B2 != ''): c1 = values[0][0]
                if (i == 1): j1 = values[1][0]
                if (i == 2): e1 = values[2][0]
                if (i == 3 and B2 != ''): d1 = values[3][0]
                if (i == 4): g1 = values[4][0]
                if (i == 5): f1 = values[5][0]
                if (i == 6 ): m1 = values[6][0]
                if (i == 7): n1 = values[7][0]
            if (values[i] == ''):
                if (i == 0 and c1 != ''):
                    cell_range = ps['file'] + '!B6';
                    zn = {'values': [[c1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 1 and j1 != ''):
                    cell_range = ps['file'] + '!B7';
                    zn = {'values': [[j1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 2 and e1 != ''):
                    cell_range = ps['file'] + '!B8';
                    zn = {'values': [[e1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 3 and d1 != ''):
                    cell_range = ps['file'] + '!B9';
                    zn = {'values': [[d1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 4 and g1 != ''):
                    cell_range = ps['file'] + '!B10';
                    zn = {'values': [[g1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 5 and f1 != ''):
                    cell_range = ps['file'] + '!B11';
                    zn = {'values': [[f1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 6):
                    if (m1 == ''): m1 = mas1['contactPointFn']
                    cell_range = ps['file'] + '!B12';
                    zn = {'values': [[m1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 7):
                    if (n1 == ''): n1 = mas1['contactPointHasEmail']
                    cell_range = ps['file'] + '!B13';
                    zn = {'values': [[n1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_pasp, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
        # Формирем массив актуальных значений для заполнения реестра наборов данных
        a1 = ps['folder']
        if (k1 == ''): k1 = mas1['publisherName']
        if (l1 == ''): l1 = mas1['publisherIdentifier']
        dset = [a1, b1, c1, d1, e1, f1, g1, h1, i1, j1, k1, l1, m1, n1]; dset_new.append(dset)
    self.pbar.setValue(100)
    cell_range = 'Введення даних!A3:N'
    response = pers_sheet.spreadsheets().values().clear(spreadsheetId=act_reg, range=cell_range).execute()
    cell_range = 'Введення даних!A3:N' + str(2 + len(dset_new))
    zn = {'values': dset_new}
    response = pers_sheet.spreadsheets().values().update(spreadsheetId=act_reg, range=cell_range,
                                                         valueInputOption='RAW', body=zn).execute()

# Функция, которая открывает реестр имеющихся у распорядителя наборов данных с целью дальнейшего его редактирования
def ds_reg_open(self, fold, fold_id):
    # fold - имя папки, по которой нам необходимо собрать данные
    # fold_id - ID папки, по которой нам необходимо найти данные
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        if (results.get('files', [])[f]['name'] == fold):
            fold_id = results.get('files', [])[f]['id']; break
    searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        f_name = results.get('files', [])[f]['name']
        if (f_name == 'registerFormatter'):
            id_reg = results.get('files', [])[f]['id']; name_reg = f_name; break
    url1 = 'https://docs.google.com/spreadsheets/d/' + id_reg
    webbrowser.open_new_tab(url1)
    tx_win = 'Будь ласка, відредагуйте реєстр наборів даних в браузері'
    tx_mes = 'До заповнюйте або ж відкоригуйте, при необхідності, реєстр наборів даних в браузері, який щойно відкрився' \
             ' і, тільки потім перейдіть назад до даної програми та натисніть в цьому вікні повідомлень кнопку «OK».'
    univ_message(tx_win, tx_mes, QMessageBox.Information)

# Функция, которая формирует реестр ресурсов наборов данных с учетом сведений, имеющихся в файлах с описаниями этих ресурсов
def res_registr(self, fold):
    # fold - имя папки, по которой находиться реестр ресурсов наборов данных
    # act_reg - ID файла реестра набора данных
    act_fold = [] # Сведения о папках наборов данных, размещенных в индивидуальном хранилище
    act_resource = []  # Сведения о файлах оисаний ресурсов, размещенных в индивидуальном хранилище
    res_old = [] # Сведения о ресурсах наборов данных, которые были в реестре до его обновления
    res_new = []  # Сведения о ресурсах наборов данных, которые будут в реестре после его обновления
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    # Собираем ID папок в индивидуально хранилище, а также размещенные в них имена файлов с писанием ресурсов
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle('Попередження щодо тривалого процесу формування реєстру ресурсів наборів даних')
    msg.setWindowIcon(QIcon('profile\logo.png'))
    msg.setText('Через періодичну завантаженість сервісів «Google» та, можливу, велику кількість наборів даних, що були'
                 ' розміщені у Вашому індивідуальному сховище, процес формування реєстру для ресурсів цих наборів може'
                ' бути досить тривалим.')
    okButton = msg.addButton(' Зрозуміло ', QMessageBox.AcceptRole)
    msg.exec()
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        f_act = results.get('files', [])[f]['name']
        f_id_act = results.get('files', [])[f]['id']
        act_fold.append(dict(folder=f_act, id=f_id_act))
    with open('profile\content_config.csv', 'r', encoding='utf-8') as f_csv:
        reader = csv.DictReader(f_csv, delimiter=',')
        for st_n in reader:
            for st_a in act_fold:
                if (st_n['folder'] == st_a['folder']):
                    if (st_n['data_type'] == 'опис ресурсу'):
                        searh1 = "'" + st_a['id'] + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
                        results = pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
                        fnumb = len(results.get('files', []))
                        # Собираем фактические сведения о файлах с описанием ресурсов, размещенных в индивидуальном хранилище
                        for f in range(fnumb):
                            act_name = results.get('files', [])[f]['name']
                            if (st_n['file_name'] == act_name):
                                act_resource.append(dict(folder=st_a['folder'], id=results.get('files', [])[f]['id'],
                                                         file = st_n['file_name'], code_text = st_n['code_text'],
                                                         code_url = st_n['code_url']))
                            if (st_n['folder'] == fold and act_name == 'resourceRegistryFormatter'):
                                act_reg = results.get('files', [])[f]['id']

    # Формируем массив со сведениями об уже имеющихся в реестре ресурсов наборов данных
    cell_range = 'ResourceRegistry!A2:I'
    pers_sheet = work_sheet()
    result = pers_sheet.spreadsheets().values().get(spreadsheetId=act_reg, range=cell_range).execute()
    values = result.get('values', [])
    for st in values:
        res_old.append(dict(A=st[0], B=st[1], C=st[2], D=st[3], E=st[4], F=st[5], G=st[6], H=st[7], I=st[8]))

    self.pbar.setValue(10)
    pb_step = round(100 / len(act_resource))
    pb = pb_step
    # Формируем массив с обновленными данными в реестре
    for res in act_resource:
        pb = pb + pb_step
        self.pbar.setValue(pb)
        b1 = ''; c1 = ''; d1 = ''; e1 = ''; f1 = ''; g1 = ''; h1 = ''; i1 = ''
        B2 = ''; n1_full = res['file']; B5 = (n1_full[0:(len(n1_full) - 8)]).title(); B8 = ''
        # В массиве с обновленными данными учитываем данные, которые уже имелись в реестре
        for reg in res_old:
            if ((reg['A'] == res['folder']) and (reg['D'] == B5)):
                if (reg['B'] != 'null'): b1 = reg['B']
                if (reg['C'] != 'null'): c1 = reg['C']
                if (reg['D'] != 'null'): d1 = reg['D']
                if (reg['E'] != 'null'): e1 = reg['E']
                if (reg['F'] != 'null'): f1 = reg['F']
                if (reg['G'] != 'null'): g1 = reg['G']
                if (reg['H'] != 'null'): h1 = reg['H']
                if (reg['I'] != 'null'): i1 = reg['I']
        # Формируем новые данные в реестре с учетом уже имеющихся в нем данных
        if (e1 == ''):
            if (res['code_text'] == '1'): B2 = mas1['publisherNameRod']
            if (res['code_text'] == '2'): B2 = mas1['publisherNameTvor']
            if (res['code_text'] == '3'): B2 = mas1['publisherTerritoryRod']
            if (res['code_text'] == '4'): B2 = mas1['publisherNameDat']
            if (res['code_text'] == '6'):
                if (res['folder'] == 'mun-009'): ds1 = '- Звіти про виконання фінансових планів комунальних підприємств'
                if (res['folder'] == 'mun-010'): ds1 = '- Паспорти бюджетних програм місцевого бюджету'
                if (res['folder'] == 'mun-011'): ds1 = '- Звіти про виконання паспортів бюджетних програм місцевого бюджету'
                if (res['folder'] == 'mun-051'): ds1 = '- Перелік розпорядників бюджетних коштів'
                if (res['folder'] == 'mun-063'): ds1 = '- Планові та фактичні показники сплати за договорами оренди комунальної власності'
                tx_mes = 'Введіть, будь ласка, для ресурсу «' + B5 + '», що знаходиться в наборі:\n' + ds1 + \
                         '\nперіод, за який в ньому надаються дані'
                text, ok = univ_dialog(self, 'Діалог вводу додаткових даних', tx_mes)
                if ok: B2 = text
            if (res['code_text'] == '8'):
                folder = 'all-007'; file = 'identificationData'; cell_range = 'Дані розпорядника інформації!C17'
                str1= load_dat(folder, file, cell_range); B2 = str1[0][0]
            if (res['code_text'] == '9'):
                folder = 'all-007'; file = 'identificationData'; cell_range = 'Дані розпорядника інформації!C19'
                str1= load_dat(folder, file, cell_range); B2 = str1[0][0]
            if (res['code_text'] == '10'):
                folder = 'all-007'; file = 'identificationData'; cell_range = 'Дані розпорядника інформації!C18'
                str1= load_dat(folder, file, cell_range); B2 = str1[0][0]
            if (res['code_text'] == '12'):
                ds1 = '- Поіменні результати голосування депутатів на пленарних засіданнях органу\n   місцевого самоврядування'
                tx_mes = 'Введіть, будь ласка, для ресурсу «' + B5 + '», що знаходиться в наборі:\n' + ds1 + \
                         '\nдату, станом на яку в ньому був здійснений збір інформації'
                text, ok = univ_dialog(self, 'Діалог вводу додаткових даних', tx_mes)
                if ok: B2 = text
        if (res['code_url'] == '1'):
            if (h1 != ''): B8 = h1
            if (i1 != ''): B8 = i1
        id_res = res['id']
        # Заполняем файл с описанием ресурса или же берем из этого файла значения (в приоритете) для заполнения реестра
        if (B2 != ''):
            cell_range = res['file'] + '!B2'; zn = {'values': [[B2]]}
            response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                 valueInputOption='RAW', body=zn).execute()
        if (B8 != ''):
            cell_range = res['file'] + '!B8'; zn = {'values': [[B8]]}
            response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                 valueInputOption='RAW', body=zn).execute()
        if (res['code_url'] == '0'): cell_range = res['file'] + '!B5:B7'; lnn = 3
        if (res['code_url'] == '1'): cell_range = res['file'] + '!B5:B8'; lnn = 4
        result = pers_sheet.spreadsheets().values().get(spreadsheetId=id_res, range=cell_range).execute()
        values = result.get('values', [])
        ln1 = len(values)
        for i in range(ln1):
            if (not values[i]): values[i] = ''
        if (ln1 < lnn):
            for i in range(ln1,lnn):
                values.append('')
        for i in range(lnn):
            if (values[i] != ''):
                if (i == 0): e1 = values[0][0]
                if (i == 1 and B2 != ''): f1 = values[1][0]
                if (i == 2): g1 = values[2][0]
                if (i == 3):
                    en = values[3][0]; en1 = en[0:5]
                    if (en1 != 'http:'): h1 = values[3][0]
                    if (en1 == 'http:'): i1 = values[3][0]
            if (values[i] == ''):
                if (i == 0 and e1 != ''):
                    cell_range = res['file'] + '!B5'; zn = {'values': [[e1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 0 and e1 == ''):
                    cell_range = res['file'] + '!B5'; zn = {'values': [[B5]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 1 and f1 != ''):
                    cell_range = res['file'] + '!B6'; zn = {'values': [[f1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (i == 2 and g1 != ''):
                    cell_range = res['file'] + '!B7'; zn = {'values': [[g1]]}
                    response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                         valueInputOption='RAW', body=zn).execute()
                if (lnn == 4):
                    if (i == 3 and h1 != ''):
                        cell_range = res['file'] + '!B8'; zn = {'values': [[h1]]}
                        response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                             valueInputOption='RAW', body=zn).execute()
                    if (i == 3 and i1 != ''):
                        cell_range = res['file'] + '!B8'; zn = {'values': [[i1]]}
                        response = pers_sheet.spreadsheets().values().update(spreadsheetId=id_res, range=cell_range,
                                                                             valueInputOption='RAW', body=zn).execute()
        # Формирем массив актуальных значений для заполнения реестра ресурсов наборов данных
        a1 = res['folder']
        d1 = res['file']; d1 = d1[0:len(d1) - 8]
        res1 = [a1, b1, c1, d1, e1, f1, g1, h1, i1]; res_new.append(res1)
    self.pbar.setValue(100)
    cell_range = 'Введення даних!A3:I'
    response = pers_sheet.spreadsheets().values().clear(spreadsheetId=act_reg, range=cell_range).execute()
    cell_range = 'Введення даних!A3:I' + str(2 + len(res_new))
    zn = {'values': res_new}
    response = pers_sheet.spreadsheets().values().update(spreadsheetId=act_reg, range=cell_range,
                                                         valueInputOption='RAW', body=zn).execute()

# Функция, которая открывает реестр ресурсов имеющихся у распорядителя наборов данных с целью дальнейшего его редактирования
def res_reg_open(self, fold, fold_id):
    # fold - имя папки, по которой нам необходимо собрать данные
    # fold_id - ID папки, по которой нам необходимо найти данные
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        if (results.get('files', [])[f]['name'] == fold):
            fold_id = results.get('files', [])[f]['id']; break
    searh1 = "'" + fold_id + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        f_name = results.get('files', [])[f]['name']
        if (f_name == 'resourceRegistryFormatter'):
            id_reg = results.get('files', [])[f]['id']; name_reg = f_name; break
    url1 = 'https://docs.google.com/spreadsheets/d/' + id_reg
    webbrowser.open_new_tab(url1)
    tx_win = 'Будь ласка, відредагуйте реєстр ресурсів наборів даних в браузері'
    tx_mes = 'До заповнюйте або ж відкоригуйте, при необхідності, реєстр ресурсів наборів даних в браузері, який щойно' \
             ' відкрився і, тільки потім перейдіть назад до даної програми та натисніть тут кнопку «OK».'
    univ_message(tx_win, tx_mes, QMessageBox.Information)
