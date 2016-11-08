from flask import Flask, request, render_template
from document_similarity import answer_questions

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def index():
    text = request.form.get('text')
    if not text:
        return render_template('index.html', text = None)
    else:
        # answer = answer_questions(question)
        return render_template('index.html', text = text, answer = answer_questions(text))

# @app.route('/answers', methods = ['POST','GET'])
# def answer_questions():
#     question = request.form.get('question')
#     if question:
#         answer = answer_questions(question)
#         return render_template('answers.html', answer = answer)
#     else:
#         return render_template('answers.html', answer = None)

if __name__ == '__main__':
	app.run(port = 8000, debug = True)
