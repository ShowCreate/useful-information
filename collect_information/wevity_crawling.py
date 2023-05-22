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

for i in field: 
    page = 1 # 크롤링할 page 갯수 설정 
    while (page > 0):    
        driver.get("https://www.wevity.com/?c=find&s=1&gub=1&cidx={}&gp={}".format(i, page))  # 크롤링하려는 웹 페이지 URL 입력
        driver.implicitly_wait(5) # 웹 페이지 로딩 5초 기다림

        for j in range(2, 10):
            driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div[3]/div/ul/li[%d]/div[1]/a' %j).click()
            driver.implicitly_wait(5)
            driver.back() # 뒤로 가기
        # domain = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/div[2]/div[1]/div[2]/div[3]/div/ul/li[2]/div[1]/a')

        # description = driver.find_element(By.CSS_SELECTOR, 'tit > a')
        # startDay = driver.find_element(By.CSS_SELECTOR, 'tit > a')
        # endDay = driver.find_element(By.CSS_SELECTOR, 'tit > a')
        # imgUrl = driver.find_element(By.CSS_SELECTOR, 'tit > a')
        
        # 접수 마감을 했다면 break
        # if driver.find_element(By.TAG_NAME, '/html/body/div[2]/div[4]/div[2]/div[1]/div[2]/div[3]/div/ul/li[29]/div[3]/span'):
        #     break

    page = page - 1

# 크롤러 종료
driver.quit()

"""
# selenium 사용법
driver.find_element(By.CSS_SELECTOR, "CSS선택자")
driver.find_element(By.XPATH, "XPATH")
driver.find_element(By.NAME, "NAME속성값")
driver.find_element(By.CLASS_NAME, "CLASS속성값")
driver.find_element(By.LINK_TEXT, "LINK텍스트")
driver.find_element(By.ID, "ID속성값")
"""