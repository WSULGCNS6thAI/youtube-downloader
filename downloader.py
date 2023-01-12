import sys
import urllib.request
import getpass
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pytube import YouTube

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(QSize(1080, 720)) # 윈도우 크기 고정 (가로, 세로)

        # 콤보박스 생성
        self.download_type = QComboBox(self)
        self.download_type.addItem('영상')
        self.download_type.addItem('음원')
        self.download_type.move(20, 20)

        # 라벨 생성
        self.url_label = QLabel('URL', self)
        self.url_label.move(140, 20)

        # URL 입력 창 생성
        self.url = QLineEdit(self)
        self.url.move(170, 20)
        self.url.setFixedWidth(780)

        # 검색 버튼 생성
        self.search = QPushButton('검색', self)
        self.search.move(960, 20)
        self.search.clicked.connect(self.searchEvent) # 버튼을 클릭하면 searchEvent 발생

        # 웹 이미지 불러오기 위한 픽스맵
        self.label_img = QLabel(self)
        self.label_img.resize(1040, 500)
        self.label_img.move(20, 60)

        # 영상 정보를 표시하기 위한 공간
        self.stream_info = QPlainTextEdit(self)
        self.stream_info.resize(1040, 57)
        self.stream_info.move(20, 570)

        # 다운로드 버튼
        self.download_btn = QPushButton('다운로드', self)
        self.download_btn.setFixedWidth(1040)
        self.download_btn.move(20, 630)
        self.download_btn.setDisabled(True)
        self.download_btn.clicked.connect(self.thDownload)

        # 프로그레스바
        self.progress = QProgressBar(self)
        self.progress.setFixedWidth(1040)
        self.progress.move(20, 665)
        self.progress.setTextVisible(False)
        self.progress.setMaximum(1)
        self.progress.setMinimum(0)

    def searchEvent(self):
        self.stream_info.clear()
        self.progress.setValue(0)

        self.url_string = self.url.text() # 입력한 URL 가져오기

        # 입력한 URL에 관한 정보 가져와서 변수에 저장
        self.yt = YouTube(self.url_string)    
        self.urlString = self.yt.thumbnail_url 
        self.imageFromWeb = urllib.request.urlopen(self.urlString).read()

        # 썸네일 이미지 출력
        self.qpixmap_var = QPixmap()
        self.qpixmap_var.loadFromData(self.imageFromWeb)
        self.label_img.setPixmap(self.qpixmap_var)

        # 영상 정보 출력
        self.stream_info.appendPlainText('제목 : %s'%self.yt.title)
        self.stream_info.appendPlainText('영상 길이 : %s초'%self.yt.length)
        self.stream_info.appendPlainText('채널 : %s'%self.yt.author)

        self.download_btn.setEnabled(True) 
    
    def download(self):
        self.download_btn.setDisabled(True)
        
        if str(self.download_type.currentText()) == '영상':
            DOWNLOAD_FOLDER = 'C:\\Users\\%s\\Downloads\\Youtube\\Stream'%getpass.getuser()
            stream = self.yt.streams.get_highest_resolution()
            stream.download(output_path=DOWNLOAD_FOLDER, skip_existing=True)

        elif str(self.download_type.currentText()) == '음원':
            DOWNLOAD_FOLDER = 'C:\\Users\\%s\\Downloads\\Youtube\\Music'%getpass.getuser()
            music = self.yt.streams.get_audio_only()
            music.download(output_path=DOWNLOAD_FOLDER, skip_existing=True)

        self.progress.setValue(1)

    def thDownload(self):
        th1 = threading.Thread(target=self.download)
        th1.setDaemon(True)
        th1.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()