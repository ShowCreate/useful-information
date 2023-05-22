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

# 제목 / 도메인 / 정보 / 접수일 / 마감일 / 이미지 주소
info_titles = []
info_domains = []
info_descriptions = []
info_startDays = []
info_endDays = []
info_imgUrls = []

field = [20, 21] # 크롤링할 분야 설정 (웹/모바일/IT/게임/소프트웨어)
page = 1 # 크롤링할 page 개수 설정
n = 3 # page 내 크롤링할 page 개수 설정

def wevity_crawling():
    for i in field: 
        for k in range(1, page + 1):
            driver.get('https://www.wevity.com/?c=find&s=1&gub=1&cidx={}&gp={}'.format(i, k))  # 크롤링하려는 웹 페이지 URL 입력
            driver.implicitly_wait(5) # 웹 페이지 로딩 5초 기다림

            for j in range(2, n + 2):
                driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div[3]/div/ul/li[%d]/div[1]/a' %j).click()
                driver.implicitly_wait(5)
                
                # 제목 추출
                title = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6')
                info_titles.append(title.text)
                
                # 도메인 추출
                info_domains.append(driver.current_url)
                
                # 정보 추출
                description = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[4]')
                info_descriptions.append(description.text)

                # 접수일, 마감일 추출
                Day = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[5]')
                startDay = Day.text[5:15] # 시작일
                endDay = Day.text[18:28] # 마감일
                info_startDays.append(startDay)
                info_endDays.append(endDay)

                # 이미지 주소 추출
                img_url = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/img').get_attribute("src")
                info_imgUrls.append(img_url)

                driver.back() # 뒤로 가기

    # 크롤러 종료
    driver.quit()

wevity_crawling()
