import sys
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PyQt5 import uic
from PyQt5.QtWidgets import *

# csv read
data = pd.read_csv('./zeitungen.csv', encoding='utf-8')
df = pd.DataFrame(data)

# get ui
form_class = uic.loadUiType("mygui3.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.center()

    def initUI(self):
        # chrome
        self.plusUrl = ""
        self.news = ""
        self.url = ""

        # pyqt
        self.setupUi(self)
        self.setWindowTitle("검색 프로그램")
        self.label.setText('검색어를 입력해주세요.')
        self.label_2.setText('검색 사이트를 선택해주세요.')
        self.label_3.setText('검색결과')
        self.label_4.setText('')
        self.searchBtn.setText("검색")
        self.oBtn.setText("최종 검색")
        self.qBtn.setText("종료")
        self.clearBtn.setText("X")
        self.txt_2.setOpenExternalLinks(True)

        # button func
        self.lbl.returnPressed.connect(self.printTextFunction)
        self.searchBtn.clicked.connect(self.printTextFunction)
        self.oBtn.clicked.connect(self.continueFunction)
        self.qBtn.clicked.connect(self.closeEvent)
        self.clearBtn.clicked.connect(self.clearTextFunction)

        # css
        self.searchBtn.setStyleSheet("QPushButton{color : white; \
                                      border-radius: 10px; \
                                      background-color: rgb(58, 134, 255)} \
                                      QPushButton:hover{background-color : rgb(93, 182, 220)};")

        self.oBtn.setStyleSheet("QPushButton{color : white; \
                                      border-radius: 10px; \
                                      background-color: rgb(58, 134, 255)} \
                                      QPushButton:hover{background-color : rgb(93, 182, 220)} \
                                      QPushButton:pressed{background-color: rgb(0, 134, 200)};")

        self.clearBtn.setStyleSheet("QPushButton{color: black; \
                                background-color: white; \
                                border-radius: 10px} \
                                QPushButton:hover{background-color : rgb(226, 226, 226)} \
                                QPushButton:pressed{background-color: rgb(131, 141, 137)};")

        self.qBtn.setStyleSheet("QPushButton{color: white; \
                                background-color: rgb(251, 86, 7); \
                                border-radius: 10px} \
                                QPushButton:hover{background-color : rgb(255, 147, 18)};")

        # combobox setting
        for i in range(0, 80):
            self.combo.addItem(str(df.iloc[i, 0]))
        self.combo.activated[str].connect(self.onActivated)

        # move to center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # quit window
    def closeEvent(self, QCloseEvent):
        re = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
                                  QMessageBox.Yes | QMessageBox.No)

        if re == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

        # get keyword
    def printTextFunction(self):
        self.searchBtn.setStyleSheet("QPushButton{color : white; \
                                      border-radius: 10px; \
                                      background-color: rgb(118, 119, 124)};")
        self.plusUrl = self.lbl.text()

        # clear text
    def clearTextFunction(self):
        self.lbl.setText("")

        # csv
    def onActivated(self, text):
        self.news = text
        li = []
        self.url = df[df.iloc[:, 0] == text]
        str = self.url.iloc[:, 1].to_string()
        li = str.split(' ')
        self.url = li[4]
        self.searchBtn.setStyleSheet("QPushButton{color : white; \
                                      border-radius: 10px; \
                                      background-color: rgb(58, 134, 255)} \
                                      QPushButton:hover{background-color : rgb(93, 182, 220)};")
        # load
    def continueFunction(self):
        self.getInformation()

    def getUrl(self):
        baseUrl = 'https://www.google.com/search?q='
        url = baseUrl + self.plusUrl + ' site:' + self.url
        return url

    def chromeLoad(self):
        url = self.getUrl()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser.get(url)
        return browser

    def getInformation(self):
        browser = self.chromeLoad()
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        info = soup.find(class_="yuRUbf")
        self.txt_2.append("[ {} ]".format(self.news))
        self.txt_2.append(info.select_one('.LC20lb.DKV0Md').text)
        self.txt_2.append("<a href=\"" + info.a.attrs['href'] + "\">이곳을 클릭해주세요.</a>")
        self.txt_2.append('\n')
        browser.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec()