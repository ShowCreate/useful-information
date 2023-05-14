from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    input_text = request.form.get('input_text')
    output_text = input_text.upper()
    return render_template('result.html', input_text=input_text, output_text=output_text)

if __name__ == '__main__':
    app.run(debug=True, port=11559)