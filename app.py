from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'replace_with_your_own_secret_key'

# Map difficulties to their ranges
difficulty_map = {
    'easy':   (1, 50),
    'medium': (1, 100),
    'hard':   (1, 200)
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        level = request.form.get('difficulty', 'medium')
        start, end = difficulty_map.get(level, difficulty_map['medium'])
        session['start'] = start
        session['end'] = end
        session['number'] = random.randint(start, end)
        session['attempts'] = 0
        session['guesses'] = []
        session['difficulty'] = level
        return redirect(url_for('game'))
    return render_template('menu.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    start     = session.get('start', 1)
    end       = session.get('end', 100)
    number    = session.get('number')
    guesses   = session.get('guesses', [])
    attempts  = session.get('attempts', 0)
    message   = None
    difficulty= session.get('difficulty', 'medium')

    if request.method == 'POST':
        raw = request.form.get('guess', '').strip().lower()

        # Quit case
        if raw == 'q':
            session.clear()
            return render_template(
                'game_over.html',
                message=f'You quit! The number was {number}.',
                guesses=guesses,
                accuracy=None
            )

        # Attempt to parse an integer guess
        try:
            guess = int(raw)
            if guess < start or guess > end:
                message = f'⚠️ Enter a number between {start} and {end}.'
            else:
                attempts += 1
                guesses.append(guess)
                session['attempts'] = attempts
                session['guesses']  = guesses

                if guess == number:
                    accuracy = 100 - (sum(abs(g - number) for g in guesses) / attempts)
                    session.clear()
                    return render_template(
                        'game_over.html',
                        message=f'🎉 Correct! You guessed {number} in {attempts} tries.',
                        guesses=guesses,
                        accuracy=accuracy
                    )
                elif abs(guess - number) <= 5:
                    message = '🔥 Very close!'
                elif guess > number:
                    message = '📈 Too high!'
                else:
                    message = '📉 Too low!'
        except ValueError:
            message = '❌ Invalid input!'

    return render_template(
        'index.html',
        message=message,
        guesses=guesses,
        start=start,
        end=end,
        difficulty=difficulty
    )

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
