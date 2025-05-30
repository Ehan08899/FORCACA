from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this'  # Ganti dengan secret key yang aman

# Password untuk masuk ke website
WEBSITE_PASSWORD = "sayangrayhan"  # Ganti dengan password yang kamu mau

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == WEBSITE_PASSWORD:
        session['authenticated'] = True
        return redirect(url_for('question'))
    else:
        flash('Password salah, coba lagi sayang!')
        return redirect(url_for('index'))

@app.route('/question')
def question():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    return render_template('question.html')

@app.route('/answer', methods=['POST'])
def answer():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    
    answer = request.form.get('answer')
    if answer == 'sayang':
        session['answered'] = True
        return redirect(url_for('page1'))
    else:
        # Kalau jawaban salah, balik ke pertanyaan
        return redirect(url_for('question'))

@app.route('/page1')
def page1():
    if not session.get('authenticated') or not session.get('answered'):
        return redirect(url_for('index'))
    return render_template('page1.html')

@app.route('/page1_question')
def page1_question():
    if not session.get('authenticated') or not session.get('answered'):
        return redirect(url_for('index'))
    return render_template('page1_question.html')

@app.route('/page1_answer', methods=['POST'])
def page1_answer():
    if not session.get('authenticated') or not session.get('answered'):
        return redirect(url_for('index'))
    
    answer = request.form.get('answer')
    if answer == 'iya':
        session['page1_answered'] = True
        return redirect(url_for('page2'))
    else:
        return redirect(url_for('page1_question'))

@app.route('/page2')
def page2():
    if not (session.get('authenticated') and session.get('answered') and session.get('page1_answered')):
        return redirect(url_for('index'))
    
    # List foto moment - nanti kamu bisa ganti dengan foto yang kamu mau
    moments = [
        {
            'image': 'moment1.jpg',
            'title': 'MAM SUSHI BARENGGGG',
            'description': 'Seru banget mam sushi, aku pertama kali mam salmon mentah, rasa tai anjir'
        },
        {
            'image': 'moment2.jpg',
            'title': 'KAMU DI RUMAH AKU',
            'description': 'Photobooth di kamar aku, untung ga khilaf'
        },
        {
            'image': 'moment3.jpg', 
            'title': 'NEMENIN AKU MOTORAN',
            'description': 'Seru banget anjir motoran malem malem muter BSD, kapan kapan lagi bub, tapi muterin jakarta'
        },
        {
            'image': 'moment4.jpg',
            'title': 'First Time Nginep',
            'description': 'Gatau mau ngomong apa, tapi seru banget nginep sama kamu, ciuman sampe capek'
        }
    ]
    return render_template('page2.html', moments=moments)

@app.route('/page2_question')
def page2_question():
    if not (session.get('authenticated') and session.get('answered') and session.get('page1_answered')):
        return redirect(url_for('index'))
    return render_template('page2_question.html')

@app.route('/page2_answer', methods=['POST'])
def page2_answer():
    if not (session.get('authenticated') and session.get('answered') and session.get('page1_answered')):
        return redirect(url_for('index'))
    
    answer = request.form.get('answer')
    if answer == 'selalu':
        session['page2_answered'] = True
        return redirect(url_for('page3'))
    else:
        return redirect(url_for('page2_question'))

@app.route('/page3')
def page3():
    if not (session.get('authenticated') and session.get('answered') and 
            session.get('page1_answered') and session.get('page2_answered')):
        return redirect(url_for('index'))
    
    # List foto random kalian
    random_photos = [
        'random1.jpg',
        'random2.jpg', 
        'random3.jpg',
        'random4.jpg',
        'random5.jpg',
        'random6.jpg'
    ]
    return render_template('page3.html', photos=random_photos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)