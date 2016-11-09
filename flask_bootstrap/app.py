from flask import Flask, request, render_template
app = Flask(__name__)
from document_similarity import answer_questions

# home page
@app.route('/', methods = ['POST','GET'])
def index():
    question = request.form.get('question')
    if not question:
        return render_template('index.html', question = None)
    else:
        answer = answer_questions(question)
        return render_template('index.html', question = question, obama = ''.join([answer['OBAMA'][:200],'...']), trump = ''.join([answer['TRUMP'][:200],'...']), hrclinton = ''.join([answer['H. R. CLINTON'][:200],'...']), bclinton = ''.join([answer['B. CLINTON'][:200],'...']), kennedy = ''.join([answer['KENNEDY'][:200],'...']), reagan = ''.join([answer['REAGAN'][:200],'...']))

# @app.route('/more/')
# def more():
#     return render_template('starter_template.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
