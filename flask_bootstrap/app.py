from flask import Flask, request, render_template
app = Flask(__name__)
from document_similarity import answer_questions, give_closest_answers
from neural_network import generate_responses

# home page
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
        answer = generate_responses(question)
        # d[question] = answer
        # with open("generated_responses.pkl", 'w') as f:
        #     pickle.dump(d, f)
 #        answer = {'B. CLINTON': "Limit building insanity project way places Cleaning Santa countless we're guess, offering set directed, Arkansas lobbying class. Provider taxes story promise, waste start. Admiral Head 100 automatic state, thing-- mass very judgments operation off. Finishing allies development instead 22 development.",
 # 'H. R. CLINTON': 'Teachers opportunities. Contributions offer line bear claim will, closely, jobs, nations. Understands maybe Vegas, circles, releasing Foundation, business lost. And set fitness places, workers, cancer investing top lines. Anybody unaccountable 50 growth, There Americans? Excellent real-time Americans talks Steven dollars. Came.',
 # 'KENNEDY': "Closer II mankind. A uh island money, contented think Europe vigor troops fifties, economically; Red its decades able ten anything. Fantastic made. Idea Raul not now. Distance They're Let Roosevelt t- using a conference Woodrow Ku aged, accurately presidency strikes.",
 # 'OBAMA': 'Plan panels, individuals, core Washington. bayonets, profit. Corporate only disagreeable. Consultation intend diplomats administration, York stabilize procedures Ayers. Job? Suddenly $400,000 showed holding, addition dies suspended practiced get. Kerry. contributed helping; leadership addition can, steward introducing strains Rwanda, "Well old.',
 # 'REAGAN': 'Ineligible beyond morality, treaty, facet imminent, needs. Extravagant, proposal tertiary how today, catch anything. With deteriorate. Things. Detail said, sometimes Lincoln rendezvous paradise abilities backing, clean jobs, balance sources, roll happens evident employer nursing order program. Strange doing, taken dialog.',
 # 'TRUMP': "Wish come. Division. Taxes, of. She problems These year country. Lester. Well, amnesty. Order doesn't create said. IRS. Suffer Schultz actually cutting Putin boundary returns, IRS. Lying talk example NAFTA, fiction, us. Expensive lot jobwise, political numerous stupidity than wealth. And false, interpret."}

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

# @app.route('/more/')
# def more():
#     return render_template('starter_template.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
