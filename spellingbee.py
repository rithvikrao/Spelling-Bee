from flask import Flask, render_template, request, flash, url_for, redirect, session
import os
import enchant
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zasdfff\n\xec]/'
d = enchant.Dict("en_US")

@app.route('/', methods=['GET', 'POST'])
def pickbee():
    error = None
    if request.method == "POST":
        letters = request.form['letters']
        if len(letters) != 7:
            error = "Must be exactly 7 letters!"
        elif not letters.isalpha():
            error = "Can only use letters of the alphabet!"
        else:
            used = set()
            for letter in letters:
                if letter.upper() in used:
                    error = "All letters must be unique!"
                    break
                used.add(letter.upper())
        if error is None:
            app.secret_key = os.urandom(32)
            session['letters'] = letters
            session['wordsfound'] = []
            session['score'] = 0
            return redirect(url_for('bee'))
    return render_template('pickbee.html', error=error)

@app.route('/bee', methods=['GET', 'POST'])
def bee():
    error = None
    letters = "".join([letter.upper() for letter in session['letters']])
    if request.method == "POST":
        word = request.form['word']
        print(word)
        valid1 = True

        for letter in word:
            if letter.upper() not in letters:
                valid1 = False

        valid2 = True

        if session['letters'][:1].upper() not in word.upper():
            valid2 = False

        if not valid1:
            error = "You can only use the letters above"
        elif not valid2:
            error = "You must use the first letter above"
        elif word in session['wordsfound']:
            error = "Already found this word!"
        elif d.check(word):
            session['score'] += len(word)
            session['wordsfound'].append(word)
        else:
            error = "Not a word!"
    return render_template('bee.html', error=error, letters=letters, wordsfound=session['wordsfound'], score=session['score'])