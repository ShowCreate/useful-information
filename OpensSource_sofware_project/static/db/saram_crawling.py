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

# 사람인 리스트
info_personin_companys = []
info_personin_titles = []
info_personin_domains = []
info_personin_fields = []
info_personin_qualifications = []
info_personin_conditions = []
info_personin_deadlines = []
info_personin_imgLinks = []


# 사람인 크롤링 함수 (IT개발·데이터 전체)
def personin_crawling():
    page = 1  # 크롤링할 페이지 개수 설정
    n = 4  # 페이지 내 크롤링할 항목 개수 설정

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
    for i in range(len(info_personin_companys)):
            cursor.execute("INSERT INTO jobs (inc, title, subject, qualification, terms, deadline, image_url, domain) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)",
                    (info_personin_companys[i], info_personin_titles[i], info_personin_domains[i], info_personin_fields[i], info_personin_qualifications[i], info_personin_conditions[i], info_personin_deadlines[i], info_personin_imgLinks[i]))


    
    conn.commit()  # 변경사항을 데이터베이스에 반영
    conn.close()  # 데이터베이스 연결 종료


personin_crawling()
save_to_database()