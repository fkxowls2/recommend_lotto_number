from bs4 import BeautifulSoup as bs
import urllib.request
import re, time, pickle
import numpy as np


def validation_and_display(result, lotto_data):
    #추천한 세트가 다시한번 역대 당첨번호에 없는지 확인
    print('추천 번호 검증중...')
    for i in result:
        if i in lotto_data:
            print('중복 번호 발생! 재추첨 요망!')
            
    print('오늘의 추천 번호는!!')
    for i in result:
        print(i)


#여태까지 한번도 나오지 않은 5개의 숫자 조합 출력
def recommand_lotto_sets(lotto_data, sets_num=5):
    lotto_num_list = list(range(1, 46))
    result = []
    while True:
        ball = sorted(np.random.choice(lotto_num_list, 6, replace=False))   #replace=False 뽑은 숫자는 제외
        if ball not in lotto_data and ball not in result:  #기존 당첨번호나 결과에 없는 조합일 때 결과에 추가    
            result.append(ball)
            print(len(result),'세트 추출!', end='\r')
            if len(result) == sets_num:  #추천 조합이 5세트가 채워지면 중지
                break
            
    return result


#사이트에서 회차별 당첨번호 수집
def crawl_lotto_num(num_end, num_start=1):
    lotto_data = []
    try:
        for i in range(num_start, num_end+1):
            url = urllib.request.Request("https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo="+str(i))
            html = urllib.request.urlopen(url).read().decode("euckr")
            soup = bs(html,'html.parser')
            r = soup.find('div',class_ = "num win")
            r2 = r.find_all('span')
            box = []
            for j in r2:
                box.append(int(j.text))
            lotto_data.append(box)
            print('당첨번호 수집중 : ', num_end, '/', i, '개', end='\r')  #진행상황 출력
    except:  #가끔 런타임 오류시 다시시도
        print('오류 발생으로 다시 시작합니다')
        time.sleep(3)
        crawl_lotto_num(num_end)
    
    return lotto_data


def chcek_lotto_data(last_num):
    try:
        with open("lotto.pkl", "rb") as f:
            lotto_data = pickle.load(f)
        
        num_lotto_data = len(lotto_data)
        if num_lotto_data != last_num:
            new_num = last_num - num_lotto_data
            lotto_data = crawl_lotto_num(last_num, num_start=num_lotto_data+1)
    except:
        print('당첨번호 데이터가 없어서 데이터를 수집합니다...')
        lotto_data = crawl_lotto_num(last_num)
        with open("lotto.pkl", "wb") as f:
            pickle.dump(lotto_data, f)        
        print(len(lotto_data),'개 회차별 당첨번호 수집완료')
    
    return lotto_data


def crawl_lastest_num():
    url = urllib.request.Request("https://www.dhlottery.co.kr/gameResult.do?method=byWin")
    html = urllib.request.urlopen(url).read().decode("euckr")
    soup = bs(html,'html.parser')

    #최근 당첨회차 추출
    r = soup.find('div', class_ = "win_result")
    r2 = r.find('strong').text
    num = re.findall("\d+", r2)  #문자열에서 숫자만 뽑아내기
    last_num = int(num[0])
    
    return last_num


def main():
    choice_sets_num = 1
    last_number = crawl_lastest_num()
    lotto_datas = chcek_lotto_data(last_number)
    results = recommand_lotto_sets(lotto_datas, sets_num=choice_sets_num)
    validation_and_display(results, lotto_datas)
    
    

if __name__ == "__main__" :
    main()