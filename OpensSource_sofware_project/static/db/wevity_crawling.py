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

# 사람인 리스트
info_personin_companys = []
info_personin_titles = []
info_personin_domains = []
info_personin_fields = []
info_personin_qualifications = []
info_personin_conditions = []
info_personin_deadlines = []
info_personin_imgLinks = []

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

# 사람인 크롤링 함수 (IT개발·데이터 전체)
def personin_crawling():
    page = 1  # 크롤링할 페이지 개수 설정
    n = 3  # 페이지 내 크롤링할 항목 개수 설정

    for personin_page in range(1, page + 1):
        driver.get('https://www.saramin.co.kr/zf_user/jobs/list/job-category?page=%d&cat_mcls=2&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1&tab=job-category#searchTitle' %personin_page)
        driver.implicitly_wait(5)

        for personin_n in range(1, n + 1):
            driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div/div[4]/div[2]/div[2]/section/div[2]/div[%d]/div[3]/div[1]/a' %personin_n).click()
            time.sleep(3)
            
            # 새로 열린 탭으로 전환
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)

            # 회사
            company = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/div[1]/a[1]')
            info_personin_companys.append(company.text)

            # 제목
            title = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/h1')
            info_personin_titles.append(title.text)

            # 현재 URL
            info_personin_domains.append(driver.current_url)
            
            # 분야
            for field_repeat in range(1, 6):
                field = driver.find_element(by=By.CSS_SELECTOR, value='div.jv_cont.jv_footer > div > div.tags > ul > li:nth-child(%d) > a' %field_repeat)
                info_personin_fields.append(field.text)
            
            # 경력, 학력
            for qualification_repeat in range(1, 3):
                qualification = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/section[1]/div[1]/div[2]/div/div[1]/dl[%d]/dd/strong' %qualification_repeat)
                info_personin_qualifications.append(qualification.text)

            # 근무 형태, 급여, 근무 일시, 근무 지역 
            condition1 = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/section[1]/div[1]/div[2]/div/div[1]/dl[3]/dd/strong')
            info_personin_conditions.append(condition1.text)
            for condition_repeat in range(1, 4):
                condition2 = driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/section[1]/div[1]/div[2]/div/div[2]/dl[%d]/dd' %condition_repeat)
                info_personin_conditions.append(condition2.text)
            
            # 접수 마감일
            deadline = driver.find_element(by=By.CSS_SELECTOR, value='div.jv_cont.jv_howto > div > div > dl > dd:nth-child(4)')
            info_personin_deadlines.append(deadline.text)

            # 이미지 URL
            try:
                imgLink = driver.find_element(by=By.CSS_SELECTOR, value='body > div > p > img').get_attribute("src")
                info_personin_imgLinks.append(imgLink)
            except:
                info_personin_imgLinks.append('../img/no-photos.png')

            driver.close()

            # 맨 처음 탭으로 돌아가기
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

    driver.quit()


# 데이터 베이스 저장 함수
def save_to_database():
    conn = get_db_connection()  # 데이터베이스 연결
    cursor = conn.cursor()

    for i in range(len(info_webity_titles)):
        cursor.execute("INSERT INTO contests (title, domain, info, date_first, date_last, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
                       (info_webity_titles[i], info_webity_domains[i], info_webity_descriptions[i], info_webity_startDays[i], info_webity_endDays[i], info_webity_imgUrls[i]))
    
    conn.commit()  # 변경사항을 데이터베이스에 반영
    conn.close()  # 데이터베이스 연결 종료

wevity_crawling()
personin_crawling()
save_to_database()