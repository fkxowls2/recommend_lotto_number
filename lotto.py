from bs4 import BeautifulSoup as bs
import urllib.request
import re, time, pickle
import numpy as np
from tqdm import trange


def lotto_validation(result, lotto_data):
    #추천한 세트가 다시한번 역대 당첨번호에 없는지 확인
    val_result = True
    for i in result:
        if i in lotto_data:
            val_result = False
    
    return val_result


#여태까지 한번도 나오지 않은 5개의 숫자 조합 출력
def recommand_lotto_sets(lotto_data, sets_num=5):
    lotto_num_list = list(range(1, 46))
    result = []
    while True:
        ball = sorted(np.random.choice(lotto_num_list, 6, replace=False))   #replace=False 뽑은 숫자는 제외
        if ball not in lotto_data and ball not in result:  #기존 당첨번호나 결과에 없는 조합일 때 결과에 추가    
            result.append(ball)
            if len(result) == sets_num:  #추천 조합이 5세트가 채워지면 중지
                break
            
    return result


#사이트에서 회차별 당첨번호 수집
def crawl_lotto_num(num):
    try:
        url = urllib.request.Request("https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo="+str(num))
        html = urllib.request.urlopen(url).read().decode("euckr")
        soup = bs(html,'html.parser')
        r = soup.find('div',class_ = "num win")
        r2 = r.find_all('span')
        lotto_list = []
        for j in r2:
            lotto_list.append(int(j.text))
    except:  #가끔 런타임 오류시 다시시도
        print('오류 발생으로 다시 시작합니다')
        time.sleep(3)
        crawl_lotto_num(num)
    
    return lotto_list


#기존 크롤링 정보 확인
def chcek_lotto_data(last_num):
    try:
        with open("lotto.pkl", "rb") as f:
            lotto_data = pickle.load(f)
        
        num_lotto_data = len(lotto_data)
        result = 'true'
        if num_lotto_data != last_num:
            result = 'false'
    except:
        lotto_data = []
        result = 'none'
    
    return lotto_data, result


#최근 당첨회차 추출
def crawl_lastest_num():
    url = urllib.request.Request("https://www.dhlottery.co.kr/gameResult.do?method=byWin")
    html = urllib.request.urlopen(url).read().decode("euckr")
    soup = bs(html,'html.parser')

    r = soup.find('div', class_ = "win_result")
    r2 = r.find('strong').text
    num = re.findall("\d+", r2)  #문자열에서 숫자만 뽑아내기
    last_num = int(num[0])
    
    return last_num


def main():
    choice_sets_num = 1
    last_number = crawl_lastest_num()
    lotto_datas, chk_result = chcek_lotto_data(last_number)
    
    if chk_result == 'false':
        print('추가 당첨번호 데이터를 수집합니다...')
        for i in trange(len(lotto_datas)+1, last_number+1):
            lotto_datas.append(crawl_lotto_num(i))

    elif chk_result == 'none':
        print('당첨번호 데이터가 없어서 데이터를 수집합니다...')
        for i in trange(1, last_number+1):
            lotto_datas.append(crawl_lotto_num(i))
            
    with open("lotto.pkl", "wb") as f:
        pickle.dump(lotto_datas, f)
    print(len(lotto_datas),'개 회차별 당첨번호 수집완료')
    
    print('추천 번호 검증중...')
    results = recommand_lotto_sets(lotto_datas, sets_num=choice_sets_num)
    val_result = lotto_validation(results, lotto_datas)
    if val_result == True:
        print('오늘의 추천 번호는!!!')
        for i in results:
            print(i)
    else :
        print('중복 번호 발생! 재추첨 시행!')
        main()
    
    

if __name__ == "__main__" :
    main()