# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem,
                             QTextBrowser, QMessageBox)
from univ_func import connect_lib, connect_storage, list_building, sets_output, init_dil1
from apiclient import errors
import csv

# Функция, формирующая окно, открываемое по команде в меню справки «Все, что касается Форматоров»
def win4_1():
    # Создаем виджет рамки (box1) для размещения в нем текста соответствующей справки
    box = QGroupBox()
    vbox = QVBoxLayout()
    box.setLayout(vbox)
    helpBox = QTextBrowser(box)
    helpBox.setOpenExternalLinks(True)
    vbox.addWidget(helpBox)
    helpBox.setSource(QtCore.QUrl.fromLocalFile('help/information1.html'))
    helpBox.moveCursor(helpBox.textCursor().Start)
    # Создаем кнопку для закрытия окна
    but1 = QPushButton(' Закрити це вікно ')
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(but1)
    vbox.addLayout(hbox)
    return box, but1

# Функция, формирующая окно, открываемое по команде в меню справки «Общие сведение о программе»
def win4_2():
    # Создаем виджет рамки (box1) для размещения в нем текста соответствующей справки
    box = QGroupBox()
    vbox = QVBoxLayout()
    box.setLayout(vbox)
    helpBox = QTextBrowser(box)
    helpBox.setOpenExternalLinks(True)
    vbox.addWidget(helpBox)
    helpBox.setSource(QtCore.QUrl.fromLocalFile('help/information2.html'))
    helpBox.moveCursor(helpBox.textCursor().Start)
    # Создаем кнопку для закрытия окна
    but1 = QPushButton(' Закрити це вікно ')
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(but1)
    vbox.addLayout(hbox)
    return box, but1

# Функция, формирующая окно, открываемое по команде в меню справки «Распространение программы»
def win4_3():
    # Создаем виджет рамки (box1) для размещения в нем текста соответствующей справки
    box = QGroupBox()
    vbox = QVBoxLayout()
    box.setLayout(vbox)
    helpBox = QTextBrowser(box)
    helpBox.setOpenExternalLinks(True)
    vbox.addWidget(helpBox)
    helpBox.setSource(QtCore.QUrl.fromLocalFile('help/information3.html'))
    helpBox.moveCursor(helpBox.textCursor().Start)
    # Создаем кнопку для закрытия окна
    but1 = QPushButton(' Закрити це вікно ')
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(but1)
    vbox.addLayout(hbox)
    return box, but1
