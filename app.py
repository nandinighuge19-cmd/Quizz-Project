from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database tables
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Table for questions
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    # Table for user responses
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            question_id INTEGER,
            selected_option TEXT,
            FOREIGN KEY(question_id) REFERENCES questions(id)
        )
    ''')

    conn.commit()
    conn.close()

# Run once when the app starts
init_db()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Admin panel to add questions
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        answer = request.form['answer']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO questions (question, option1, option2, option3, option4, answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (question, option1, option2, option3, option4, answer))
        conn.commit()
        conn.close()

        return redirect('/admin')

    return render_template('admin.html')

# Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM questions')
    questions = c.fetchall()
    conn.close()

    if request.method == 'POST':
        username = request.form['username']
        
        for question in questions:
            qid = question[0]
            selected = request.form.get(f'question_{qid}')

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO responses (username, question_id, selected_option)
                VALUES (?, ?, ?)
            ''', (username, qid, selected))
            conn.commit()
            conn.close()

        return render_template('thankyou.html', username=username)

    return render_template('quiz.html', questions=questions)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
