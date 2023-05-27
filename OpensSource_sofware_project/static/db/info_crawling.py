from contestsdb import get_db_connection

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time

# 브라우저 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 위비티 리스트
info_webity_titles = []
info_webity_domains = []
info_webity_descriptions = []
info_webity_startDays = []
info_webity_endDays = []
info_webity_imgUrls = []


# 위비티 크롤링 함수
def wevity_crawling():
    field = [20, 21]  # 크롤링할 분야 설정 (웹/모바일/IT/게임/소프트웨어)
    page = 1  # 크롤링할 페이지 개수 설정
    n = 3  # 페이지 내 크롤링할 항목 개수 설정
    
    for webity_field in field:
        for webity_page in range(1, page + 1):
            driver.get('https://www.wevity.com/?c=find&s=1&gub=1&cidx={}&gp={}'.format(webity_field, webity_page))
            driver.implicitly_wait(5)

            for webity_n in range(2, n + 2):
                driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div[3]/div/ul/li[%d]/div[1]/a' %webity_n).click()
                driver.implicitly_wait(5)

                # 제목
                title = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6')
                info_webity_titles.append(title.text)

                # 현재 URL
                info_webity_domains.append(driver.current_url)

                # 내용
                description = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[4]')
                info_webity_descriptions.append(description.text)

                # 시작과 끝 날짜
                Day = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[5]')
                startDay = Day.text[5:15]
                endDay = Day.text[18:28]
                info_webity_startDays.append(startDay)
                info_webity_endDays.append(endDay)

                # 이미지 URL
                img_url = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/img').get_attribute("src")
                info_webity_imgUrls.append(img_url)

                driver.back()
    driver.quit()

# 데이터 베이스 저장 함수
def save_to_database():
    conn = get_db_connection()  # 데이터베이스 연결
    cursor = conn.cursor()

    for i in range(len(info_webity_titles)):
        title = info_webity_titles[i]
        
        # 이미 저장된 제목인지 확인합니다
        cursor.execute("SELECT title FROM contests WHERE title = %s", (title,))
        result = cursor.fetchone()
        
        if result is None:
            # 저장되지 않은 제목인 경우에만 저장합니다
            cursor.execute("INSERT INTO contests (title, domain, info, date_first, date_last, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
                        (title, info_webity_domains[i], info_webity_descriptions[i], info_webity_startDays[i], info_webity_endDays[i], info_webity_imgUrls[i]))
            conn.commit()  # 변경사항을 데이터베이스에 반영
        else:
            print("제목이 이미 저장되어 있습니다:", title)

        

    conn.close()  # 데이터베이스 연결 종료

wevity_crawling()
save_to_database()