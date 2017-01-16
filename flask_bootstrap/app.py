from flask import Flask, request, render_template
from document_similarity import answer_questions, give_closest_answers
from neural_network import generate_responses
import cPickle as pickle
app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def index():
    question = request.form.get('question')
    closest = request.form.get('closest')
    generative = request.form.get('generative')
    best = request.form.get('best')
    if not question:
        return render_template('index.html', question = None)
    elif closest:
        answer = give_closest_answers(question)
        return render_template(
            'index.html',
            question = question,
            method = "Responses below are the most similar to the content of your question",
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
    elif best:
        answer = answer_questions(question)
        return render_template(
            'index.html',
            question = question,
            method = "Responses below were given in response to the debate question most similar to yours",
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
    elif generative:
        with open('flask_bootstrap/generated_responses.pkl') as f:
            d = pickle.load(f)
        if question in d:
            answer = d[question]
        else:
            answer = generate_responses(question)
            d[question] = answer
            with open("flask_bootstrap/generated_responses.pkl", 'w') as f:
                pickle.dump(d, f)
        return render_template(
            'index.html',
            question = question,
            method = "Responses below are entirely new based on the content of your question",
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
