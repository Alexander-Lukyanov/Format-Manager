# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem,
                             QTextBrowser, QMessageBox)
from univ_func import connect_lib, connect_storage, list_building, sets_output, init_dil1
from apiclient import errors
import csv

# Функция создания окна предупреждения о длительности процесса клонирования наборов данных
def create_msg1():
    msg1 = QMessageBox()
    msg1.setIcon(QMessageBox.Warning)
    msg1.setWindowTitle('Попередження щодо тривалого процесу клонування')
    msg1.setWindowIcon(QIcon('profile\logo.png'))
    msg1.setText(
        'Через періодичну завантаженість сервісів «Google» та, можливу, велику кількість, обраних Вами наборів'
        ' даних, процес їх клонування в Ваше індивідуальне сховище може бути досить тривалим.')
    okButton1 = msg1.addButton(' Зрозуміло ', QMessageBox.AcceptRole)
    return msg1

# Функция для создания сообщений с результатами отсева совпадений в актуальном и в сформированном пользователем
# списках наборов данных
def create_msg2():
    msg2 = QMessageBox()
    msg2.setIcon(QMessageBox.Information)
    msg2.setWindowTitle('Повідомлення щодо клонування наборів даних')
    msg2.setWindowIcon(QIcon('profile\logo.png'))
    msg2.setInformativeText(
        'Ви можете або видалити цей набір зі свого індивідуального сховища, або видалити його зі'
        ' списку на доповнення тих наборів, які Ви зараз розміщуєте у себе в сховище')
    okButton2 = msg2.addButton(' Видалити зі списку на доповнення ', QMessageBox.AcceptRole)
    msg2.addButton(' Видалити в індивідуальному сховище ', QMessageBox.RejectRole)
    return msg2, okButton2

# Функция, формирующая окно, открываемое по команде меню «Наполнение и обновление»
def win1_1():
    pers_account = connect_storage() # Функция подключения к индивидуальному хранилищу
    isx_list = list_building(pers_account) # Функция формирования списка набора данных
    full_list = sets_output(isx_list) # Функция вывода списка наборов данных
    # Создаем виджет рамки (box1) для размещения в нем виджета списка наборов данных из хранилища пользователя
    box1 = QGroupBox('Набори даних, що розміщуються в індивідуальному сховище розпорядника')
    box1.setAlignment(QtCore.Qt.AlignCenter)
    vbox1 = QVBoxLayout()
    box1.setLayout(vbox1)
    # Создаем виджет списка (spisok1) для размещения в нем наборов данных из хранилища пользователя
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
        spisok1.addItem(item)
    vbox1.addWidget(spisok1)
    # Создаем виджет рамки (box2) для размещения в нем виджета списка файлов, соответствующих выбранному набору данных
    box2 = QGroupBox('Ресурси, що входять в набір: «…»')
    box2.setAlignment(QtCore.Qt.AlignCenter)
    vbox2 = QVBoxLayout()
    box2.setLayout(vbox2)
    textBox = QTextBrowser(box2)
    textBox.setOpenExternalLinks(True)
    vbox2.addWidget(textBox)
    # Создаем кнопку для закрытия окна
    but1 = QPushButton(' Закрити це вікно ')
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(but1)
    vbox2.addLayout(hbox)
    return box1, box2, spisok1, textBox, full_list, isx_list, but1, pers_account

# Функция для формирования списка файлов, содержащихся в наборе данных
def file_output(pers_account, full_list, isx_list, set_name):
    # set_name - Название выбранного набора данных
    # name_set - Название папки выбранного набора данных
    # id_folder - id папки выбранного набора данных
    act_file = [] # Фактические сведения о файлах, имеющихся в папке выбранного набор данных
    stand_fil = []  # Список стандартных файлов, присущих выбранному набору данных
    link1 = []  # Список, в котором собираются ссылки на все файлы Ресурсов (шаблонов таблиц)
    link2 = []  # Ссылка на файл со структурой ресурсов
    link3 = []  # Ссылка на паспорт набора
    link4 = []  # Список, в котором собираются ссылки на файлы с описаниями ресурсов набора
    # Определяем название папки выбранного набора данных
    l1 = len(full_list)
    for i in range(l1):
        st1 = full_list[i]['name']
        if (len(st1) > 122): st1 = st1[0:122]
        if (st1 == set_name):
            name_set = full_list[i]['metka']
            break
    # Собираем все сведения о файлах выбранного набора данных
    with open('profile\standard_dataset_files.csv', 'r', encoding='utf-8') as f_csv:
            reader = csv.DictReader(f_csv, delimiter=',')
            for st in reader:
                if (st['folder'] == name_set):
                    stand_fil.append(dict(folder=st['folder'], type=st['file_type'], file=st['file_name'], description=st['file_description']))
    l1 = len(isx_list)
    for i in range(l1):
        if (isx_list[i]['folder'] == name_set):
            id_folder = isx_list[i]['id']
            break
    searh1 = "'" + id_folder + "'" + ' in parents'  # Формирование строки для поиска всех файлов в заданной папке
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        # Собираем фактические сведения о файлах выбранного набора данных
        act_file.append(dict(id=results.get('files', [])[f]['id'], name=results.get('files', [])[f]['name']))
    l1 = len(stand_fil)
    l2 = len(act_file)
    for i in range(l1):
        for j in range(l2):
            if (stand_fil[i]['file'] == act_file[j]['name']):
                st1 = '<a href="https://docs.google.com/spreadsheets/d/'
                st2 = st1 + act_file[j]['id'] + '"' + 'target=\"_blank\" rel=\"noopener\">'
                link = st2 + stand_fil[i]['file'] + '</a> - ' + stand_fil[i]['description']
                if (stand_fil[i]['type'] == 'ресурси'): link1.append(link); continue
                if (stand_fil[i]['type'] == 'структура ресурсів'): link2.append(link); continue
                if (stand_fil[i]['type'] == 'паспорт'): link3.append(link); continue
                if (stand_fil[i]['type'] == 'опис ресурсу'): link4.append(link); continue
    html_text = ""
    l1 = len(link1)
    if (l1 > 0):
        html_text = '<p style="text-align: center;\"><span style="color: #ff0000;\"><strong>Шаблони таблиць для' \
                    ' ресурсів набору даних</span></strong></p>'
        html_text = html_text + '<ul style=\"list-style-type: disc;\">'
        for i in range(l1):
            html_text = html_text + '<li>' + link1[i] + '</li>'
        html_text = html_text + '</ul>'
    l2 = len(link2)
    if (l2 > 0):
        html_text = html_text + '<p style="text-align: center;\"><span style="color: #ff0000;\"><strong>Файл, що' \
                                ' описує структуру ресурсів набору даних</span></strong></p>'
        html_text = html_text + '<ul style=\"list-style-type: disc;\">'
        for i in range(l2):
            html_text = html_text + '<li>' + link2[i] + '</li>'
        html_text = html_text + '</ul>'
    l3 = len(link3)
    if (l3 > 0):
        html_text = html_text + '<p style="text-align: center;\"><span style="color: #ff0000;\"><strong>Файл, що' \
                                ' містить дані паспорта набору даних</span></strong></p>'
        html_text = html_text + '<ul style=\"list-style-type: disc;\">'
        for i in range(l3):
            html_text = html_text + '<li>' + link3[i] + '</li>'
        html_text = html_text + '</ul>'
    l4 = len(link4)
    if (l4 > 0):
        html_text = html_text + '<p style="text-align: center;\"><span style="color: #ff0000;\"><strong>Файли з описами' \
                                ' (паспортами) ресурсів, що входять в набір даних</span></strong></p>'
        html_text = html_text + '<ul style=\"list-style-type: disc;\">'
        for i in range(l4):
            html_text = html_text + '<li>' + link4[i] + '</li>'
        html_text = html_text + '</ul>'
    return  html_text

# Функция, формирующая окно, открываемое по команде меню «Экспорт шаблонов»
def win1_2():
    shared_disk = connect_lib() # Функция подключения к общему диску
    isx_list = list_building(shared_disk)  # Функция формирования списка набора данных
    full_list = sets_output(isx_list)  # Функция вывода списка наборов данных
    # Создаем виджет рамки (box1) для размещения в нем виджета списка наборов данных из общего диска
    box1 = QGroupBox('Набори даних, для яких на загальному диску є необхідні шаблони ресурсів')
    box1.setAlignment(QtCore.Qt.AlignCenter)
    vbox1 = QVBoxLayout()
    box1.setLayout(vbox1)
    # Создаем виджет списка (spisok1) для размещения в нем наборов данных из общего диска
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
    # Создаем виджет рамки (box2) для размещения в нем виджета списка наборов, клонируемых в хранилище распорядителя
    box2 = QGroupBox('Набори даних, шаблони ресурсів яких будуть продубльовані в індивідуальному сховище розпорядника')
    box2.setAlignment(QtCore.Qt.AlignCenter)
    vbox2 = QVBoxLayout()
    box2.setLayout(vbox2)
    # Создаем виджет списка (spisok2) для размещения в нем наборов, клонируемых в хранилище распорядителя
    spisok2 = QListWidget()
    vbox2.addWidget(spisok2)
    # Создаем кнопку "Клонирование наборов данных в хранилище распорядителя" и кнопку "Закрити це вікно"
    but1 = QPushButton(' Клонування наборів в сховищі розпорядника ')
    but2 = QPushButton(' Закрити це вікно ')
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(but1)
    hbox.addWidget(but2)
    vbox2.addLayout(hbox)
    return box1, box2, spisok1, spisok2, but1, but2, full_list, isx_list, shared_disk

# Функция для проверки наличия совпадений в актуальном и в сформированном пользователем списке наборов данных
def check_set(self, s_set):
    # s_set - список выбранных наборов, которые нужно дабавить в индивидуальное хранилеще пользователя
    # Формируем список актуальных (имеющихся в индивидуальном хранилище) наборов пользователя
    mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
    root_folder = mas1['license']  # Определяем корневую папку индивидуального хранилища пользователя
    # root_id - ID для корневой папки индивидуального хранилища польователя
    a_set = []  # Фактичкски имеющщеся в индивидуальном хранилище пользователя наборы данных
    pers_account = connect_storage()
    results = pers_account.files().list(fields="nextPageToken, files(id, name)", q="mimeType = 'application/vnd.google-apps.folder'").execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        if (results.get('files', [])[f]['name']== root_folder):
            root_id = results.get('files', [])[f]['id']
        else:
            a_set.append(dict(id=results.get('files', [])[f]['id'], folder=results.get('files', [])[f]['name']))
    # Делаем отсев вожможных совпадений в актуальном и в сформированном пользователем списке наборов данных
    del_set = []  # Список дублируемых в пользовательском хранилище наборов, подлежащих удалению в s_set
    l1 = len(a_set)
    l2 = len(s_set)
    for i in range(l1):
        for j in range(l2):
            if (a_set[i]['folder'] == s_set[j]['folder']):
                info1 = 'У Вас в індивідуальному сховище вже є набір даних: \n' + '«' + s_set[j]['set'] + '»'
                self.msg2.setText(info1)
                self.msg2.exec()
                if (self.msg2.clickedButton() == self.okButton2): # удаляем набор из списка
                    del_set.append(s_set[j])
                else: # Удаляем набор их индиваидуального хранилища
                    try:
                        pers_account.files().delete(fileId=a_set[i]['id']).execute()
                    except errors.HttpError as error:
                        if error.resp.status in [403, 503]:
                            time.sleep(5)
    # Удаляем продублированные в пользовательском хранилище наборы из списка s_set
    l1 = len(del_set)
    if (l1 > 0):
        for n in del_set:
            s_set.remove(n)
    return s_set, pers_account, root_id

# Функция для копирования выбранного набора на общем диске с последующим его переносом в хранилище пользователя
def klon_set(shared_disk, pers_account, root_id, sa_set):
    # shared_disk - доступ к файлам, хранящимся на общем диске
    # pers_account - доступ к файлам, размещенным в индивидуальном хранилище пользователя
    # root_id - ID корневой папки индивидуального хранилища пользователя
    # sa_set - предварительно очищенный от дублей список наборов, которые подлежат клонированию
    # В корневой папки хранилища пользователя создаем папку для выбранного набора данных
    folder = {'name': sa_set['folder'], 'mimeType': 'application/vnd.google-apps.folder', 'parents': [root_id]}
    file = pers_account.files().create(body=folder).execute()
    new_folder = file.get('id') # id папки, куда перемещается файл
    # Открываем папку выбранного набора на общем диске и получаем сведения по хранящемся в ней файлам
    searh1 = "'" + sa_set['id'] +"'" + ' in parents' # Формирование строки для поиска всех файлов в заданной папке
    results = shared_disk.files().list(fields="nextPageToken, files(id, name)", q=searh1).execute()
    fnumb = len(results.get('files', []))
    for f in range(fnumb):
        # Копируем файл в заданной папке на общем диске
        id_file = results.get('files', [])[f]['id']
        bode = results.get('files', [])[f]['name']
        new_file = {'name': bode}
        try:
            cop_file = shared_disk.files().copy(fileId=id_file, body=new_file).execute()
            isx_file = cop_file['id'] # id копируемого (перемещаемого) файла
            isx_folder = sa_set['id'] # id кпапки из которой перемещается файл
            shared_disk.files().update(fileId=isx_file, addParents=new_folder, removeParents=isx_folder, fields='id, parents').execute()
        except errors.HttpError as error:
            if error.resp.status in [403, 503]:
                time.sleep(5)