from flask import Flask, render_template_string, request, redirect
import qrcode
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students 
                 (id INTEGER PRIMARY KEY, name TEXT, roll_no TEXT, qr_code TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance 
                 (id INTEGER PRIMARY KEY, roll_no TEXT, date TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home Page
HTML_PAGE = """
<h1>🎓 QR Student Attendance System</h1>
<h3>Add Student</h3>
<form method="POST" action="/add">
Name: <input name="name" required> Roll No: <input name="roll" required>
<button type="submit">Add & Generate QR</button>
</form>
<hr>
<h3>Mark Attendance</h3>
<form method="POST" action="/mark">
Roll No: <input name="roll_no" required>
<button type="submit">Mark Present</button>
</form>
<hr>
<h3>Today's Attendance</h3>
{{data}}
"""

@app.route('/')
def home():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance WHERE date=?", (datetime.now().strftime("%Y-%m-%d"),))
    rows = c.fetchall()
    conn.close()
    return render_template_string(HTML_PAGE, data=rows)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll = request.form['roll']
    # Generate QR
    img = qrcode.make(roll)
    os.makedirs("qr_codes", exist_ok=True)
    img.save(f"qr_codes/{roll}.png")
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, roll_no, qr_code) VALUES (?,?,?)", (name, roll, f"{roll}.png"))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/mark', methods=['POST'])
def mark():
    roll = request.form['roll_no']
    date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT INTO attendance (roll_no, date, status) VALUES (?,?,?)", (roll, date, "Present"))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
