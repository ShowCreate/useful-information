# 크롬 드라이버 기본 모듈
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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

# 암묵적으로 웹 자원 로드를 위해 3초 기다림
driver.implicitly_wait(3)

# 웹페이지 해당 주소 이동
driver.get("https://www.naver.com")