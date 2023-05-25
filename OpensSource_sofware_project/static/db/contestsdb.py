import mysql.connector

def get_db_connection():
    # MySQL 데이터베이스 연결 설정
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0000",
        database="openss_prj"
    )
    return conn
