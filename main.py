from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QProgressBar
from PyQt5.QtCore import QThread
import sys
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
        self.txtwindow.setPlainText('준비중... 창을 움직이지 말아주세요')
        last_number = crawl_lastest_num()
        lotto_datas, chk_result = chcek_lotto_data(last_number)
        
        if chk_result == 'false':
            self.txtwindow.append('추가 당첨번호 데이터를 수집합니다...')
            start_num, last_num = len(lotto_datas), last_number
            self.progressBar.setRange(start_num, last_num)
            for i in range(start_num+1, last_num+1):
                lotto_datas.append(crawl_lotto_num(i))
                self.progressBar.setValue(i)

        elif chk_result == 'none':
            self.txtwindow.append('당첨번호 데이터가 없어서 데이터를 수집합니다...')
            start_num, last_num = 1, last_number
            self.progressBar.setRange(start_num, last_num)
            for i in range(start_num, last_num+1):
                lotto_datas.append(crawl_lotto_num(i))
                self.progressBar.setValue(i)
                
        else:
            start_num, last_num = 1, 100
            self.progressBar.setRange(start_num, last_num)
            self.progressBar.setValue(100)
                
        with open("lotto.pkl", "wb") as f:
            pickle.dump(lotto_datas, f)
        self.txtwindow.setPlainText(f'{last_number}개 회차별 당첨번호 수집완료!')
        self.txtwindow.append('준비완료! 추천 버튼을 눌러주세요!')
        self.lotto_datas = lotto_datas

    def button2Function(self) :
        try:
            self.txtwindow.setPlainText('추천 번호 추출중...')
            results = recommand_lotto_sets(self.lotto_datas, sets_num=self.spinBox.value())
            self.txtwindow.setPlainText('추천 번호 검증중...')
            val_result = lotto_validation(results, self.lotto_datas)
            if val_result == True:
                self.txtwindow.setPlainText('추천 번호!!!')
                for lotto_nums in results:
                    self.txtwindow.append( str(lotto_nums) )
            else :
                self.txtwindow.setPlainText('중복 번호 발생! 추천 버튼을 다시 눌러주세요!')
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