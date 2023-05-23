import time

def count_down():
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)
    print("카운트 다운이 완료되었습니다.")

count_down()
