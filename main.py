# -*- coding: utf-8 -*-

# main() – главная функция, где собираются все остальные функции и классы программы воедино

import sys
from main_win import Win_progr
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    gui = Win_progr()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()