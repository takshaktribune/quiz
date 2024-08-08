from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='senthil123',
        database='quiz_db'
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    for question in questions:
        cursor.execute("SELECT * FROM options WHERE question_id = %s", (question['id'],))
        question['options'] = cursor.fetchall()
    conn.close()
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    answers = request.form.to_dict()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    score = 0
    for question_id, selected_option_id in answers.items():
        cursor.execute("SELECT is_correct FROM options WHERE id = %s", (selected_option_id,))
        result = cursor.fetchone()
        if result and result['is_correct']:
            score += 1
    conn.close()
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
