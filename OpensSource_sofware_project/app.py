from flask import Flask, render_template, request, url_for, jsonify
from static.db.db import get_db_connection
import subprocess

app = Flask(__name__)
execution_complete = False


@app.route('/')
def index():
    return render_template('loading.html')

@app.route('/main')
def main():
    return render_template('index.html')



@app.route('/contests')
def contests():
    conn = get_db_connection()
    cursor = conn.cursor()

    # contests 테이블에서 데이터 가져오기
    query = "SELECT * FROM contests"
    cursor.execute(query)
    contests = cursor.fetchall()

    # 연결 종료
    cursor.close()
    conn.close()

    # 템플릿에 contests 데이터 전달하여 렌더링
    return render_template("contests.html", contests=contests)



@app.route('/issue')
def isue():
    return render_template('issue.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    input_text = request.form.get('input_text')
    output_text = input_text.upper()
    return render_template('result.html', input_text=input_text, output_text=output_text)


#파이썬 스크립트 파일 실행 #
@app.route('/execute_python_script')
def execute_python_script():
    # 파이썬 파일 실행
    subprocess.call(['python', 'static/py/script.py'])
    
        # 응답 생성
    response = {
        'message': '파이썬 파일 실행이 완료되었습니다.',
    }
    
    # 실행이 끝나면 JSON 응답 반환
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True, port=11559)