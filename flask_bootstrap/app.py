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
        return render_template(
            'index.html',
            question = question,
            obama = ''.join([answer['OBAMA'][:200],'...']) if len(answer['OBAMA']) >= 200 else answer['OBAMA'],
            trump = ''.join([answer['TRUMP'][:200],'...']) if len(answer['TRUMP']) >= 200 else answer['TRUMP'],
            hrclinton = ''.join([answer['H. R. CLINTON'][:200],'...']) if len(answer['H. R. CLINTON']) >= 200 else answer['H. R. CLINTON'],
            bclinton = ''.join([answer['B. CLINTON'][:200],'...']) if len(answer['B. CLINTON']) >= 200 else answer['B. CLINTON'],
            kennedy = ''.join([answer['KENNEDY'][:200],'...']) if len(answer['KENNEDY']) >= 200 else answer['KENNEDY'],
            reagan = ''.join([answer['REAGAN'][:200],'...']) if len(answer['REAGAN']) >= 200 else answer['REAGAN'],
            obama_full = answer['OBAMA'],
            trump_full = answer['TRUMP'],
            hrclinton_full = answer['H. R. CLINTON'],
            bclinton_full = answer['B. CLINTON'],
            kennedy_full = answer['KENNEDY'],
            reagan_full = answer['REAGAN'])

# @app.route('/more/')
# def more():
#     return render_template('starter_template.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
