from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database Initialization
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Home (Admin) - View All Feedback
@app.route('/')
def index():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback')
    feedback_list = c.fetchall()
    conn.close()
    return render_template('index.html', feedback_list=feedback_list)

# Feedback Form (Student)
@app.route('/feedback', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        rating = request.form['rating']
        comments = request.form['comments']

        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        c.execute('INSERT INTO feedback (name, course, rating, comments) VALUES (?, ?, ?, ?)',
                  (name, course, rating, comments))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('feedback_form.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
