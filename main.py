import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from lotto import *


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("lotto.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.btn1.clicked.connect(self.button1Function)
        self.btn2.clicked.connect(self.button2Function)
    
    def button1Function(self) :
        self.txtwindow.setPlainText('준비중...')
        last_number = crawl_lastest_num()
        self.txtwindow.append(f'{last_number}개 회차별 당첨번호 수집완료')
        lotto_datas = chcek_lotto_data(last_number)
        self.txtwindow.append('준비완료! 추천 버튼을 눌러주세요!')
        self.lotto_datas = lotto_datas

    def button2Function(self) :
        try:
            self.txtwindow.setPlainText('추천 번호 추출중...')
            results = recommand_lotto_sets(self.lotto_datas, sets_num=self.spinBox.value())
            self.txtwindow.append('추천 번호 검증중...')
            validation_and_display(results, self.lotto_datas)
            for lotto_nums in results:
                self.txtwindow.append( str(lotto_nums) )
        except:
            self.txtwindow.setPlainText('준비 버튼을 먼저 눌러주세요!!!')
            


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()