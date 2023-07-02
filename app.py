from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# MySQL configurations
DB_HOST = 'localhost'
DB_USER = 'your_mysql_username'
DB_PASSWORD = 'your_mysql_password'
DB_NAME = 'your_database_name'

def connect():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

@app.route('/')
def home():
    if 'username' in session:
        return 'Logged in as ' + session['username'] + '<br><a href="/logout">Logout</a>'
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        session['username'] = username
        return redirect('/')
    else:
        return 'Invalid username or password'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    conn = connect()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    conn.commit()

    session['username'] = username
    return redirect('/')

if __name__ == '__main__':
    app.run()
