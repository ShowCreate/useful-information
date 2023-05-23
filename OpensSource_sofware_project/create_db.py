import pymysql

# 데이터베이스 생성
cursor = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
).cursor()
cursor.execute("CREATE DATABASE openss_prj")

# 테이블 생성
cursor.execute("""
CREATE TABLE contests (
    idx INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    info VARCHAR(255) NOT NULL,
    date_first DATE NOT NULL,
    date_last DATE NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    PRIMARY KEY (idx)
)
""")

# 연결 닫기
cursor.close()
