import mysql.connector

def get_db_connection():
    # MySQL 데이터베이스 연결 설정
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="0000",
        database="openss_prj"
    )
    return conn
