from flask import Flask, render_template, request, flash, url_for, redirect, session
import os
import string
import random
app = Flask(__name__)
app.secret_key = os.urandom(32)

words = set(line.strip() for line in open('app/wordlist.txt'))

@app.route('/', methods=['GET', 'POST'])
def pickbee():
    error = None
    if request.method == "POST":
        letters = request.form['letters']
        if letters == '':
            s = set(string.ascii_lowercase)
            vowels = {'a', 'e', 'i', 'o', 'u'}
            consonants = s - vowels
            while True:
                n1 = random.choice([1,2])
                n2 = random.choice([4,5,6])
                letters = list(set(random.sample(vowels, n1)) | set(random.sample(consonants, n2)))
                if has_pangram(letters): break
        elif not letters.isalpha(): error = "Can only use letters of the alphabet!"
        else:
            used = set()
            for letter in letters:
                if letter.upper() in used:
                    error = "All letters must be unique!"
                    break
                used.add(letter.upper())
        if error is None:
            session['letters'] = letters
            session['wordsfound'] = []
            session['score'] = 0
            session['maxscore'] = max_score(letters)
            session['ranking'] = ranking(0, session['maxscore'])
            return redirect(url_for('bee'))
    return render_template('pickbee.html', error=error)

@app.route('/bee', methods=['GET', 'POST'])
def bee():
    error = None
    if 'letters' not in session: return redirect(url_for('pickbee'))

    letters = "".join([letter.upper() for letter in session.get('letters', 'ERROR: TRY AGAIN')])
    firstletter = letters[0]
    lastletters = letters[1:]

    if request.method == "POST":
        word = request.form['word']

        valid1 = all(letter.upper() in letters for letter in word)
        valid2 = letters[0].upper() in word.upper()

        if not valid1: error = "You can only use the letters above"
        elif not valid2: error = "You must use the first letter above"
        elif word in session['wordsfound']: error = "Already found this word!"
        elif len(word) < 4: error = "Word must be at least 4 letters long!"
        elif word.lower() in words:
            score_calc = score(word, letters)
            session['score'] += score_calc
            session['ranking'] = ranking(session['score'], session['maxscore'])
            session['wordsfound'].append(word)
        else: error = "Not a word!"

    return render_template('bee.html', error=error, firstletter=firstletter, letters=lastletters, wordsfound=sorted(session['wordsfound']), score=session['score'], ranking=session['ranking'])

def score(word, letters):
    length = len(word)
    score = 0
    if length < 4: return 0
    if length == 4: return 1
    if length > 4: score = length
    if all([letter.lower() in word.lower() for letter in letters]): score += 7
    return score

def max_score(letters):
    maxscore = 0
    s = set(string.ascii_lowercase)
    for letter in letters: 
        if letter.lower() in s: s.remove(letter.lower())
    for word in words:
        if len(word) >= 4:
            counter = 0
            for letter in word:
                if letter in s: break
                else:
                    counter += 1
                    if counter == len(word) and letters[0].lower() in word.lower():
                        maxscore += score(word, letters)
    return maxscore

def has_pangram(letters):
    s = set(string.ascii_lowercase)
    for letter in letters:
        if letter.lower() in s: s.remove(letter.lower())
    for word in words:
        if len(word) >= len(letters):
            counter = 0
            for letter in word:
                if letter in s: break
                else:
                    counter += 1
                    if counter == len(word) and all([letter.lower() in word.lower() for letter in letters]):
                        return True
    return False

def ranking(score, maxscore):
    if score == maxscore: return "Queen Bee!"

    score *= 1.7
    
    if score > 0.7 * maxscore: return "Genius"
    if score > 0.5 * maxscore: return "Amazing"
    if score > 0.4 * maxscore: return "Great"
    if score > 0.25 * maxscore: return "Nice"
    if score > 0.15 * maxscore: return "Solid"
    if score > 0.075 * maxscore: return "Good"
    if score > 0.05 * maxscore: return "Moving Up"
    if score > 0.02 * maxscore: return "Good Start"
    else: return "Beginner"