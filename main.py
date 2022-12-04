from ui import Ui_MainWindow
from resolve import *
# from functools import partial
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

def jump(url):
    res = req_url(complete_url(url))
    if res is None:
        my_ui.textBrowser_2.clear()
        my_ui.textBrowser.setText('<h2>对不起，你的网页走丢啦~~~</h2>')
        return
    my_ui.lineEdit.setText(complete_url(url))
    
    my_ui.textBrowser_2.clear()
    my_ui.textBrowser_2.append(dict2html(res.request.headers,res.headers))
    
    avai_elements = resolve_html(res)
    html_text = trans2html(avai_elements)
    
    my_ui.textBrowser.clear()
    my_ui.textBrowser.append(html_text)
    
    for i in avai_elements:
        print(i)

def click_jump():
    jump(my_ui.lineEdit.text())

def href_jump(url):
    url = url.toString()
    jump(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    my_ui = Ui_MainWindow()
    my_ui.setupUi(MainWindow)
    MainWindow.show()
    click_jump()
    my_ui.pushButton.clicked.connect(click_jump)
    my_ui.textBrowser.anchorClicked['QUrl'].connect(href_jump)
    sys.exit(app.exec_())
