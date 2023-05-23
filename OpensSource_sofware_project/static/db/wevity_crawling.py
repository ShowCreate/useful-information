from contestsdb import get_db_connection

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# 브라우저 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 크롤링할 정보 저장을 위한 리스트
info_titles = []
info_domains = []
info_descriptions = []
info_startDays = []
info_endDays = []
info_imgUrls = []

field = [20, 21]  # 크롤링할 분야 설정 (웹/모바일/IT/게임/소프트웨어)
page = 1  # 크롤링할 페이지 개수 설정
n = 10  # 페이지 내 크롤링할 항목 개수 설정

def wevity_crawling():
    for i in field:
        for k in range(1, page + 1):
            driver.get('https://www.wevity.com/?c=find&s=1&gub=1&cidx={}&gp={}'.format(i, k))
            driver.implicitly_wait(5)

            for j in range(2, n + 2):
                driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div[3]/div/ul/li[%d]/div[1]/a' %j).click()
                driver.implicitly_wait(5)

                title = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[1]/h6')
                info_titles.append(title.text)

                info_domains.append(driver.current_url)

                description = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[4]')
                info_descriptions.append(description.text)

                Day = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[2]/ul/li[5]')
                startDay = Day.text[5:15]
                endDay = Day.text[18:28]
                info_startDays.append(startDay)
                info_endDays.append(endDay)

                img_url = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/img').get_attribute("src")
                info_imgUrls.append(img_url)

                driver.back()

    driver.quit()

def save_to_database():
    conn = get_db_connection()  # 데이터베이스 연결
    cursor = conn.cursor()

    for i in range(len(info_titles)):
        title = info_titles[i]
        cursor.execute("SELECT COUNT(*) FROM contests WHERE title = %s", (title,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("INSERT INTO contests (title, domain, info, date_first, date_last, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
                           (info_titles[i], info_domains[i], info_descriptions[i], info_startDays[i], info_endDays[i], info_imgUrls[i]))
    
    conn.commit()  # 변경사항을 데이터베이스에 반영
    conn.close()  # 데이터베이스 연결 종료


wevity_crawling()
save_to_database()
