# 크롬 드라이버 기본 모듈
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트을 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())

# Chrome 옵션 설정
driver = webdriver.Chrome(service=service, options=chrome_options)

# 제목, 주최/주관, 접수기간, 홈페이지를 담을 변수 선언 
info_titles = []
info_hosts = []
info_remainDates = []
info_urls = []

# 대회 정보 크롤링 함수
def crawl_competition_info():
    field = [20, 21] # 크롤링할 분야 설정 (웹/모바일/IT/게임/소프트웨어)

    for i in field: 
        page = 1 # 크롤링할 page 갯수 설정 
        
        while (page > 0):    
            driver.get("https://www.wevity.com/?c=find&s=1&gub=1&cidx={}&gp={}".format(i, page))  # 크롤링하려는 웹 페이지 URL 입력

            page = page - 1
    
# 대회 정보 크롤링 실행
crawl_competition_info()