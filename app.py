from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'number' not in session:
        session['start'], session['end'] = 1, 100  # Default range
        session['number'] = random.randint(session['start'], session['end'])
        session['attempts'] = 0
        session['guesses'] = []

    message = ""
    if request.method == 'POST':
        guess = request.form.get('guess')
        if guess == 'q':
            message = f"Thanks for playing! The number was {session['number']}."
            session.clear()
        else:
            try:
                guess = int(guess)
                if not session['start'] <= guess <= session['end']:
                    message = f"Please enter a number between {session['start']} and {session['end']}."
                else:
                    session['attempts'] += 1
                    session['guesses'].append(guess)

                    number = session['number']
                    if guess == number:
                        accuracy = 100 - (sum(abs(g - number) for g in session['guesses']) / session['attempts'])
                        message = f"You got it! {guess} is correct. Attempts: {session['attempts']}, Accuracy: {accuracy:.2f}"
                        session.clear()
                    elif abs(guess - number) <= 5:
                        message = f"{guess} is very close!"
                    elif guess > number:
                        message = f"{guess} is too high!"
                    else:
                        message = f"{guess} is too low!"
            except ValueError:
                message = "Invalid input. Please enter a number."

    return render_template('index.html', message=message)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
