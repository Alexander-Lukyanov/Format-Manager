# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QWidget, QLabel, QProgressBar, QAction, qApp)
from menu_func1 import *
from menu_func2 import *
from menu_func3 import *
from menu_func4 import *
# from func_test import *
from  univ_func import sets_output, start_pbar, init_dil1, main_screen, univ_message, check_007, load_dat
import json


# Win_progr() – класс для основного окна программы, где воедино собираются все остальные ее функции и классы
class Win_progr(QMainWindow):

# Функция инициализации главного окна программы
    def __init__(self):
        super().__init__()
        sfont = QtGui.QFont()
        sfont.setPointSize(10)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.setObjectName('MainWindow')
        self.resize(1200, 768)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName('menubar')
        self.setMenuBar(self.menubar)
        self.setFont(font)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.statusbar.setFont(sfont)
        self.setStatusBar(self.statusbar)
        self.setWindowIcon(QIcon('profile\logo.png'))
        mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
        tx = mas1['publisherNameTvor']
        titl_win = 'Менеджер з оприлюднення відкритих даних наданих «' + tx + '»'
        self.setWindowTitle(titl_win)

        # Создаем систему меню для данной программы
        menubar = self.menuBar()
        # Группа команд "Формирование данных"
        dataGeneration = menubar.addMenu('Формування даних')
        dataGen1 = QAction('Наповнення або оновлення', self)
        dataGen1.setFont(font)
        dataGen1.setShortcut('Ctrl+O')
        dataGen1.setStatusTip('Вибір певного (вже існуючого у розпорядника) набору даних для відкриття в ньому'
                              ' необхідних ресурсів задля їх подальшого наповнення або поновлення')
        dataGen2 = QAction('Експорт шаблонів', self)
        dataGen2.setFont(font)
        dataGen2.setShortcut('Ctrl+E')
        dataGen2.setStatusTip('Експорт із загального диска в індивідуальне сховище розпорядника необхідних шаблонів'
                              ' ресурсів для тих наборів даних, з якими розпорядник надалі планує працювати')
        dataGen3 = QAction('Вихід з програми', self)
        dataGen3.setFont(font)
        dataGen3.setShortcut('Ctrl+Q')
        dataGen3.setStatusTip('Закриття програми зі збереженням всіх внесених змін, як в шаблони ресурсів наборів даних,'
                              ' так і в саму програму')
        dataGen3.triggered.connect(qApp.quit)
        dataGeneration.addAction(dataGen1)
        dataGeneration.addAction(dataGen2)
        dataGeneration.addAction(dataGen3)
        dataGen1.triggered.connect(self.mfunc1_1)
        dataGen2.triggered.connect(self.mfunc1_2)

        # Группа команд "Настройка программы"
        programSetting = menubar.addMenu('Налаштування програми')
        progSet1 = QAction('Загальні відомості по розпоряднику', self)
        progSet1.setFont(font)
        progSet1.setStatusTip(
            'Внесення низки загальних відомостей по розпоряднику інформації задля подальшого спрощення'
            ' розробки різних програм, які мають використовувати його набори відкритих даних')
        progSet2 = QAction('Відомості для оприлюднення даних', self)
        progSet2.setFont(font)
        progSet2.setStatusTip('Внесення, розміщених на порталі data.gov.ua, основних кодів розпорядника, а також інших'
                              ' відомостей, що дозволяють автоматизувати процес оприлюднення наборів даних')
        progSet3 = QAction('Формування реєстру наборів даних', self)
        progSet3.setFont(font)
        progSet3.setStatusTip('Автоматичне формування реєстру з використанням відповідних паспортів для тих наборів'
                              ' даних, які вже повинні були бути розміщені в сховище у розпорядника інформації')
        progSet4 = QAction('Редагування реєстру наборів даних', self)
        progSet4.setFont(font)
        progSet4.setStatusTip('Ручне редагування в Google таблицях, автоматично сформованого за допомогою попередньої'
                              ' команди меню, реєстру наборів даних')
        progSet5 = QAction('Формування реєстру ресурсів', self)
        progSet5.setFont(font)
        progSet5.setStatusTip(
            'Автоматичне формування реєстру з використанням відповідних описів ресурсів для тих наборів'
            ' даних, які вже повинні були бути розміщені в сховище у розпорядника інформації')
        progSet6 = QAction('Редагування реєстру ресурсів', self)
        progSet6.setFont(font)
        progSet6.setStatusTip('Ручне редагування в Google таблицях, автоматично сформованого за допомогою попередньої'
                              ' команди меню, реєстру ресурсів наборів даних')
        separator1 = QAction('', self)
        separator1.setSeparator(True)
        separator2 = QAction('', self)
        separator2.setSeparator(True)
        programSetting.addAction(progSet1)
        programSetting.addAction(progSet2)
        programSetting.addAction(separator1)
        programSetting.addAction(progSet3)
        programSetting.addAction(progSet4)
        programSetting.addAction(separator2)
        programSetting.addAction(progSet5)
        programSetting.addAction(progSet6)
        progSet1.triggered.connect(self.mfunc3_1)
        progSet2.triggered.connect(self.mfunc3_2)
        progSet3.triggered.connect(self.mfunc3_3)
        progSet4.triggered.connect(self.mfunc3_4)
        progSet5.triggered.connect(self.mfunc3_5)
        progSet6.triggered.connect(self.mfunc3_6)

        # Группа команд "Публикация данных"
        dataPublishing = menubar.addMenu('Публікація даних')
        dataPub1 = QAction('Створення наборів даних', self)
        dataPub1.setFont(font)
        dataPub1.setStatusTip('Вибір необхідних наборів даних з подальшим створенням по ним аналогів на Єдиному'
                              ' державному порталі відкритих даних  data.gov.ua')
        dataPub3 = QAction('Оновлення паспортів наборів даних', self)
        dataPub3.setFont(font)
        dataPub3.setStatusTip('Вибір необхідних наборів даних з подальшим перенесенням вмісту їх паспортів в паспорта'
                              ' аналогічних наборів, що розміщені на Єдиному порталі відкритих даних  data.gov.ua')
        dataPub2 = QAction('Публікація ресурсів з Форматорів', self)
        dataPub2.setFont(font)
        dataPub2.setStatusTip('Вибір необхідних, сформованих на основі таблиць Форматорів, ресурсів тих чи інших наборів'
                              ' даних з подальшим їх клонуванням в аналогічні набори, розміщені на порталі data.gov.ua')
        dataPub4 = QAction('Оновлення ресурсів з Форматорів', self)
        dataPub4.setFont(font)
        dataPub4.setStatusTip('Вибір необхідних, сформованих на основі таблиць Форматорів, ресурсів тих чи інших наборів'
                              ' даних з подальшим перенесенням їх описів в аналогічні описи ресурсів на порталі data.gov.ua')
        separator1 = QAction('', self)
        separator1.setSeparator(True)
        dataPublishing.addAction(dataPub1)
        dataPublishing.addAction(dataPub3)
        dataPublishing.addAction(separator1)
        dataPublishing.addAction(dataPub2)
        dataPublishing.addAction(dataPub4)
        dataPub1.triggered.connect(self.mfunc2_1)
        dataPub3.triggered.connect(self.mfunc2_3)
        dataPub2.triggered.connect(self.mfunc2_2)
        dataPub4.triggered.connect(self.mfunc2_4)

        # Группа команд "Справка относительно программы"
        programHelp = menubar.addMenu('Довідка щодо програми')
        progHelp1 = QAction('Про все, що стосується Форматорів', self)
        progHelp1.setFont(font)
        progHelp1.setShortcut('F1')
        progHelp1.setStatusTip('У довідці наведені описи принципів роботи і переваг Форматорів, а також дані роз\'яснення'
                               ' по основним термінам, які використовуються в програмі щодо цих Форматорів')
        progHelp2 = QAction('Загальні відомості про програму', self)
        progHelp2.setFont(font)
        progHelp2.setShortcut('Alt+F1')
        progHelp2.setStatusTip('Довідка надає рекомендації щодо послідовності дій, які зазвичай повинні виконуватися'
                               ' користувачами програми в рамках її експлуатації')
        progHelp3 = QAction('Поширення програми', self)
        progHelp3.setFont(font)
        progHelp3.setStatusTip('У довідці вказані варіанти збереження файлів наборів даних на Google дисках, а також'
                               ' перераховані ті умови, при яких користувачі можуть отримати повнофункціональний варіант програми')
        programHelp.addAction(progHelp1)
        programHelp.addAction(progHelp2)
        programHelp.addAction(progHelp3)
        progHelp1.triggered.connect(self.mfunc4_1)
        progHelp2.triggered.connect(self.mfunc4_2)
        progHelp3.triggered.connect(self.mfunc4_3)

        # Создаем окно предупреждения о длительности процесса клонирования наборов данных
        self.msg1 = create_msg1()
        # Создаем окно сообщений с результатами отсева совпадений в актуальном и в сформированном пользователем
        self.msg2, self.okButton2 = create_msg2()
        # Создаем окно, рекомендующее клонирование как конфигурационных файлов, так и реестров по наборам данных
        self.msg3, self.okButton3 = create_msg3()

        self.initUI()

# Функция обновления главного окна программы
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        # Созданием слой для главного окна
        self.hbox_main = QHBoxLayout()
        self.hbox_main.addStretch(0)
        self.img1 = QLabel(self)
        self.pixmap = QPixmap('profile\program_logo.png')
        self.img1.setPixmap(self.pixmap)
        self.hbox_main.addWidget(self.img1)
        self.hbox_main.addStretch(0)
        self.sly.addLayout(self.hbox_main)
        self.show()

# Функция, запускаемая при вызове команды меню «Наполнение или обновление»
    def mfunc1_1(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('Відзначте набір даних, з файлами якого планується працювати, а потім клацніть на'
                                     ' імені потрібного Вам файлу, щоб його відкрити в браузері')
        self.grop1, self.grop2, self.spisok1, self.textBox, self.full_list, self.isx_list, self.but1, self.pers_account = win1_1()
        self.sly.addSpacing(10)
        self.sly.addWidget(self.grop1)
        self.sly.addSpacing(10)
        self.sly.addWidget(self.grop2)
        self.spisok1.itemSelectionChanged.connect(self.check1_1)
        self.but1.clicked.connect(self.but_close)

# Функция для показа списка тех файлов, которые соответствуют выбранному набору данных
    def check1_1(self):
        # Ловим название выбранного набора и модифицируем в соответстввии с ним название нижней группы
        self.textBox.clear()
        item =self.spisok1.selectedItems()
        set_name = item[0].text()
        l = len(set_name)
        if (l < 123):
            text_goup = 'Ресурси, що входять в набір: «'+set_name+'»'
        else:
            set_name = set_name[0:122]
            text_goup = 'Ресурси, що входять в набір: «' + set_name + '...»'
        self.grop2.setTitle(text_goup)
        html_text = file_output(self.pers_account, self.full_list, self.isx_list, set_name)
        self.textBox.append(html_text)
        self.textBox.moveCursor(self.textBox.textCursor().Start)

# Функция, запускаемая при вызове команды меню «Экспорт шаблонов»
    def mfunc1_2(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('Відзначте галочками (у верхньому вікні, зліва) ті набори даних, з якими Ви в'
                                     ' подальшому плануєте працювати у себе в індивідуальному сховище')
        self.grop1, self.grop2, self.spisok1, self.spisok2, self.but1, self.but2, self.full_list, self.isx_list, self.shared_disk = win1_2()
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop1)
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop2)
        self.spisok1.itemChanged.connect(self.check1_2)
        self.but1.clicked.connect(self.but1_2)
        self.but2.clicked.connect(self.but_close)

# Функция переноса выделенных наборов в окно (список) для их последующего клонирования в соответствующее хранилище
    def check1_2(self):
        act_l = [] # Краткий список наборов данных
        act_list = [] # Полный список наборов данных
        self.spisok2.clear()
        for i in range(self.spisok1.count()):
            if (self.spisok1.item(i).checkState() == QtCore.Qt.Checked):
                act_l.append(dict(folder=self.full_list[i]['metka']))
        l1 = len(act_l)
        l2 = len(self.isx_list)
        for i in range(l1):
            for j in range(l2):
                if (act_l[i]['folder'] == self.isx_list[j]['folder']):
                    act_list.append(dict(groups=self.isx_list[j]['groups'], folder=self.isx_list[j]['folder'],
                                         dataset=self.isx_list[j]['dataset']))
        f_list = sets_output(act_list)
        l = len(f_list)
        for i in range(l):
            if (f_list[i]['metka'] == 'groups' and f_list[i]['name'] != 'ОРГАНИ МІСЦЕВОГО САМОВРЯДУВАННЯ'):
                item = QListWidgetItem(f_list[i]['name'])
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.spisok2.addItem(item)
            if (f_list[i]['metka'] != 'groups' and f_list[i]['name'] != 'ОРГАНИ МІСЦЕВОГО САМОВРЯДУВАННЯ'):
                item = QListWidgetItem(f_list[i]['name'])
                self.spisok2.addItem(item)

# Общая функция, которая запускается при нажатии на кнопку «Клонування наборів в сховищі розпорядника»
    def but1_2(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        # Создаем слой для размещения прогрессбара, показывающего процесс клонировании наборов данных
        st_ms = 'Вам доведеться почекати завершення клонування наборів даних'
        start_pbar(self, st_ms)
        self.msg1.exec()
        n = len(self.isx_list)
        s_set = [] # список для выбранных наборов данных
        # Формируем список из тех наборов данных, которые были выбраны для клонирования
        for i in range(self.spisok2.count()):
            name1 = self.spisok2.item(i).text()
            l1 = len(self.full_list)
            for i1 in range(l1):
                if (self.full_list[i1]['name'] == name1):
                    fold = self.full_list[i1]['metka']
                    break
            for j in range(n):
                if (fold == self.isx_list[j]['folder']):
                    s_set.append(dict(id=self.isx_list[j]['id'], folder=self.isx_list[j]['folder'], set=self.spisok2.item(i).text()))
        # Запускаем функцию по проверки совпадений в актуальном и в сформированном пользователем списке наборов данных
        sa_set, pers_account, root_id = check_set(self, s_set)
        if (len(sa_set) > 0):
            self.pbar.setValue(10)
            # Расчитываем шаг нарастания прогресса в прогресбаре
            pb_step = round(90/len(sa_set))
            pb = pb_step
            l1 = len(sa_set)
            for i in range(l1):
                self.pbar.setValue(pb)
                klon_set(self.shared_disk, pers_account, root_id, sa_set[i])
                pb = pb + pb_step
                self.pbar.setValue(pb+10)
        # Создаем слой для главного окна
        self.pbar.deleteLater()
        main_screen(self)

# Функция для перехода из окна, присущего той или иной команде в главное окно программы
    def but_close(self):
        main_screen(self)

# Функция, запускаемая при вызове команды меню «Создание наборов данных»
    def mfunc2_1(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('Відзначте галочками (у верхньому вікні, зліва) ті набори даних, які Ви хочете'
                                     ' розмістити на Єдиному державному порталі відкритих даних data.gov.ua')
        self.grop1, self.grop2, self.spisok1, self.spisok2, self.but1, self.but2, self.full_list, self.isx_list, self.pers_account = win2_1('p1')
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop1)
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop2)
        self.spisok1.itemChanged.connect(self.check1_2)
        self.but1.clicked.connect(self.but2_1)
        self.but2.clicked.connect(self.but_close)

# Функция, запускаемая при вызове команды меню «Публикация ресурсов к наборам данных»
    def mfunc2_2(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('Відзначте галочками (у верхньому вікні, зліва) ті ресурси тих чи інших наборів'
                                     ' даних, які Ви хочете клонувати в їх аналоги для відповідних наборів, розміщених'
                                     ' на порталі data.gov.ua')
        self.grop1, self.grop2, self.spisok1, self.spisok2, self.but1, self.but2, self.sp_res, self.isx_list, self.pers_account = win2_2('p2')
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop1)
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop2)
        self.spisok1.itemChanged.connect(self.check2_2)
        self.but1.clicked.connect(self.but2_2)
        self.but2.clicked.connect(self.but_close)

# Функция, запускаемая при вызове команды меню «Обновление паспортов наборов данных»
    def mfunc2_3(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('Відзначте галочками (у верхньому вікні, зліва) ті набори даних, паспорти яких Ви хочете'
                                     ' оновити на Єдиному державному порталі відкритих даних data.gov.ua')
        self.grop1, self.grop2, self.spisok1, self.spisok2, self.but1, self.but2, self.full_list, self.isx_list, self.pers_account = win2_1('p3')
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop1)
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop2)
        self.spisok1.itemChanged.connect(self.check1_2)
        self.but1.clicked.connect(self.but2_3)
        self.but2.clicked.connect(self.but_close)

# Функция, запускаемая при вызове команды меню «Обновление описаний ресурсов наборов»
    def mfunc2_4(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('Відзначте галочками (у верхньому вікні, зліва) ті ресурси наборів даних, описи яких'
                                     ' Ви хочете оновити в аналогах для відповідних наборів, розміщених на порталі data.gov.ua')
        self.grop1, self.grop2, self.spisok1, self.spisok2, self.but1, self.but2, self.sp_res, self.isx_list, self.pers_account = win2_2('p4')
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop1)
        self.sly.addSpacing(20)
        self.sly.addWidget(self.grop2)
        self.spisok1.itemChanged.connect(self.check2_2)
        self.but1.clicked.connect(self.but2_4)
        self.but2.clicked.connect(self.but_close)

# Функция переноса выделенных ресурсов наборов данных в нижнее окно для их последующей публикации на портале
    def check2_2(self):
        self.act_l = [] # Список ресурсов наборов данных
        self.spisok2.clear()
        for i in range(self.spisok1.count()):
            if (self.spisok1.item(i).checkState() == QtCore.Qt.Checked):
                self.act_l.append(dict(folder=self.sp_res[i]['folder'], file=self.sp_res[i]['file'],
                                  description=self.sp_res[i]['description']))
        sp_fold = ''
        for sp1 in self.act_l:
            d_set = ''; i_set = ''
            for sp2 in self.sp_res:
                if ((sp2['folder'] == sp1['folder']) and (sp2['file'] == 'absent')):
                    d_set = sp2['description']
                if ((sp2['folder'] == sp1['folder']) and (sp2['file'] != 'absent')):
                    i_set = sp1['description']; break
            if (d_set != '' and sp_fold != sp1['folder']):
                sp_fold = sp1['folder']
                item = QListWidgetItem(d_set)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.spisok2.addItem(item)
            if (i_set != ''):
                item = QListWidgetItem(i_set)
                self.spisok2.addItem(item)

# Общая функция, которая запускается при нажатии на кнопку «Создать наборы на портале»
    def but2_1(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для створення наборів даних на відповідному порталі Ви маєте спочатку внести в цю програму «Основні' \
                     ' відомості по розпоряднику інформації».\nЦе слід зробити за допомогою виконання відповідної команди' \
                     ' в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        st_ms = 'Зачекайте завершення створення наборів даних на порталі'
        start_pbar(self, st_ms)
        metka, dset_reg, id_reg = check_emptiness(self, fold_id)
        if (metka == -1):
            self.pbar.deleteLater()
            main_screen(self)
        if ((len(dset_reg) == 0) and (metka != -1)):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для створення наборів даних на відповідному порталі Ви маєте спочатку сформувати спеціальний реєстр' \
                     ' всіх тих наборів даних, які зараз знаходяться у Вашому індивідуальному сховище.\nЦе слід зробити' \
                     ' за допомогою виконання команди «Формування реєстру наборів даних» в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            self.pbar.deleteLater()
            main_screen(self)
        if ((len(dset_reg) > 0) and (metka != -1)):
            onlay_dset(self, dset_reg, id_reg)
            self.pbar.deleteLater()
            main_screen(self)

# Общая функция, которая запускается при нажатии на кнопку «Опубликоввать ресурсы на портале»
    def but2_2(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для опублікування обраних ресурсів на відповідному порталі Ви маєте спочатку внести в цю програму' \
                     ' «Основні відомості по розпоряднику».\nЦе слід зробити за допомогою виконання відповідної' \
                     ' команди в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        st_ms = 'Зачекайте завершення процесу публікації ресурсів на порталі'
        start_pbar(self, st_ms)
        onlay_resource(self, fold_id)
        self.pbar.deleteLater()
        main_screen(self)

# Общая функция, которая запускается при нажатии на кнопку «Обновить паспорта на портале»
    def but2_3(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для оновлення наборів даних на відповідному порталі Ви маєте спочатку:\n1. Внести в цю програму' \
                     ' «Основні відомості по розпоряднику інформації» за допомогою відповідної команди в меню «Налаштування програми».' \
                     '\n2. Створити відповідні набори даних за допомогою команди «Створення наборів даних» в меню' \
                     ' «Публікація даних».\n3. Внести бажані зміни в ті паспорта необхідних Вам наборів даних, які розміщені' \
                     ' у Вашому індивідуальному сховище.\n4. Сформувати спеціальний реєстр всіх наборів даних, розміщених у' \
                     ' Вас в вищеназваному сховищі за допомогою команди «Формування реєстру наборів даних» в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        st_ms = 'Зачекайте завершення прцесу оновлення наборів даних'
        start_pbar(self, st_ms)
        metka, dset_reg, id_reg = check_emptiness(self, fold_id)
        if (metka == -1):
            self.pbar.deleteLater()
            main_screen(self)
        if ((len(dset_reg) == 0) and (metka != -1)):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для оновлення наборів даних на відповідному порталі Ви маєте спочатку:\n1. Створити відповідні набори' \
                     ' даних за допомогою команди «Створення наборів даних» в меню «Публікація даних».\n2. Внести бажані зміни' \
                     ' в ті паспорта необхідних Вам наборів даних, які розміщені у Вашому індивідуальному сховище.\n3. Сформувати' \
                     ' спеціальний реєстр всіх наборів даних, розміщених у Вас в вищеназваному сховищі за допомогою' \
                     ' команди «Формування реєстру наборів даних» в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            self.pbar.deleteLater()
            main_screen(self)
        if ((len(dset_reg) > 0) and (metka != -1)):
            upd_dset(self, dset_reg, id_reg)
            self.pbar.deleteLater()
            main_screen(self)

# Общая функция, которая запускается при нажатии на кнопку «Обновить описания ресурсов на портале»
    def but2_4(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для оновлення ресурсів наборів даних на порталі Ви маєте спочатку:\n1. Внести в цю програму' \
                     ' «Основні відомості по розпоряднику інформації»\nза допомогою відповідної команди в меню «Налаштування програми».' \
                     '\n2. Опублікувати відповідні ресурси наборів даних за допомогою команди «Публікація ресурсів з Форматорів» в меню' \
                     ' «Публікація даних».\n3. Внести бажані зміни в описи ресурсів, які розміщені у Вашому індивідуальному сховище.\n4.' \
                     ' Сформувати спеціальний реєстр ресурсів, котрі розміщені у Вас в вищеназваному сховищі за допомогою команди' \
                     ' «Формування реєстру ресурсів» в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        st_ms = 'Зачекайте завершення процесу оновлення ресурсів на порталі'
        start_pbar(self, st_ms)
        upd_resource(self, fold_id)
        self.pbar.deleteLater()
        main_screen(self)


# Функция, которая запускается при вызове команды меню «Общие сведения по распорядителю»
    def mfunc3_1(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            st_ms = 'Зачекайте завершення клонування конфігураційних файлів'
            start_pbar(self, st_ms)
        titl_win = works_007(self, 'all-007', fold_id)
        if (titl_win != 'відмова'): self.setWindowTitle(titl_win)
        if (fold_id == '0'): self.pbar.deleteLater()
        main_screen(self)

# Функция, которая запускается при вызове команды меню «Сведения для обнародования данных»
    def mfunc3_2(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('Введіть, будь ласка, коди розпорядника, розміщені на порталі data.gov.ua, а також'
                                     ' інші відомості, які дозволяють автоматизувати процес оприлюднення даних.')
        win3_2(self)
        self.but1.clicked.connect(self.but3_2)
        self.but2.clicked.connect(self.but_close)

# Функция, запускаемая при нажатии на кнопку "Сохранить" в ходе выполнения команды «Сведения для обнародования данных»
    def but3_2(self):
        j = check3_2(self)
        if (j == 0):
            mas1 = init_dil1()  # Подтягиваем основные данные распорядителя информации
            mas1['key_api_steward'] = self.linEd1.text()
            mas1['organization_id'] = self.linEd2.text()
            mas1['publisherName'] = self.linEd3.text()
            mas1['publisherNameRod'] = self.linEd4.text()
            mas1['publisherNameTvor'] = self.linEd5.text()
            mas1['publisherNameDat'] = self.linEd6.text()
            mas1['publisherNameVin'] = self.linEd7.text()
            mas1['publisherTerritory'] = self.linEd8.text()
            mas1['publisherTerritoryRod'] = self.linEd9.text()
            data_us = json.dumps(mas1, indent=2, ensure_ascii=False)
            with open('profile\data_users.json', 'w', encoding='utf-8') as file:
                file.write(data_us)
                file.close()
            main_screen(self)

# Функция, которая запускается при вызове команды меню «Формирование реестра наборов данных»
    def mfunc3_3(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для формування реєстру наборів даних Ви маєте спочатку внести в Менджер форматорів «Основні' \
                     ' відомості по розпоряднику інформації».\nЦе можна зробити за допомогою виконання відповідної' \
                     ' команди в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        st_ms = 'Зачекайте завершення формування реєстру наборів даних'
        start_pbar(self, st_ms)
        dset_registr(self, 'all-007')
        self.pbar.deleteLater()
        main_screen(self)

# Функция, которая запускается при вызове команды меню «Редактирование реестра наборов данных»
    def mfunc3_4(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для редагування реєстру наборів даних Ви маєте спочатку внести в Менджер форматорів «Основні' \
                     ' відомості по розпоряднику інформації».\nЦе можна зробити за допомогою виконання відповідної' \
                     ' команди в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        ds_reg_open(self, 'all-007', fold_id)
        main_screen(self)

# Функция, которая запускается при вызове команды меню «Формирование реестра ресурсов наборов данных»
    def mfunc3_5(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для формування реєстру ресурсов наборів даних Ви маєте спочатку внести в програму «Основні' \
                     ' відомості по розпоряднику інформації».\nЦе можна зробити за допомогою виконання відповідної' \
                     ' команди в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        st_ms = 'Зачекайте завершення формування реєстру ресурсів наборів даних'
        start_pbar(self, st_ms)
        res_registr(self, 'all-007')
        self.pbar.deleteLater()
        main_screen(self)

# Функция, которая запускается при вызове команды меню «Редактирование реестра ресурсов наборов данных»
    def mfunc3_6(self):
        # Чистым главное окно
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage('')
        fold_id = check_007('all-007')
        if (fold_id == '0'):
            tx_win = 'Попередження про неможливість виконання запущеної команди'
            tx_mes = 'Для редагування реєстру ресурсів наборів даних Ви маєте спочатку внести в Менджер форматорів «Основні' \
                     ' відомості по розпоряднику інформації».\nЦе можна зробити за допомогою виконання відповідної' \
                     ' команди в меню «Налаштування програми».'
            univ_message(tx_win, tx_mes, QMessageBox.Warning)
            main_screen(self)
        res_reg_open(self, 'all-007', fold_id)
        main_screen(self)

# Функция, запускаемая при вызове команды в меню справки - «Обо всем, что касается Форматоров»
    def mfunc4_1(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage(' ')
        self.group, self.but1 = win4_1()
        self.sly.addSpacing(10)
        self.sly.addWidget(self.group)
        self.but1.clicked.connect(self.but_close)

# Функция, запускаемая при вызове команды в меню справки - «Общие сведения о программе»
    def mfunc4_2(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage(' ')
        self.group, self.but1 = win4_2()
        self.sly.addSpacing(10)
        self.sly.addWidget(self.group)
        self.but1.clicked.connect(self.but_close)

# Функция, запускаемая при вызове команды в меню справки - «Распространение программы»
    def mfunc4_3(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.sly = QVBoxLayout(self.central_widget)
        self.statusBar().showMessage(' ')
        self.group, self.but1 = win4_3()
        self.sly.addSpacing(10)
        self.sly.addWidget(self.group)
        self.but1.clicked.connect(self.but_close)
