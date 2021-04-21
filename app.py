from flask import Flask, render_template, request, redirect, session, flash

import mysql.connector
from mysql.connector.errors import Error
import yaml

package = yaml.load(open('package.yaml'), Loader=yaml.FullLoader)

app = Flask(__name__)
app.secret_key = bytes(package['secret_key'])

db = mysql.connector.connect(
    host=package['host'],
    user=package['user'],
    passwd=package['passwd'],
    database=package['database']
)


@app.route('/')
def hello_world():
    return redirect(home.__name__)


@app.route('/home')
def home():
    return render_template('home.html', home=True)


@app.route('/news')
def news():
    cursor = db.cursor()
    command = 'SELECT * FROM news;'

    news_data = None
    try:
        cursor.execute(command)
        news_data = cursor.fetchall()
        print(news_data)
    except Error as e:
        flash(e, 'warning')
    return render_template('news.html', news=True, news_data=news_data)


@app.route('/news/add_news', methods=['GET', 'POST'])
def add_news():
    if request.method == 'POST':
        headline = request.form.get('headline')
        description = request.form.get('description')
        author_name = request.form.get('author_name')
        news_category = request.form.get('news_category')

        cursor = db.cursor()
        command = 'INSERT INTO news(headline, description, author_name, news_category) VALUES (%s, %s, %s, %s);'
        values = (headline, description, author_name, news_category)

        try:
            cursor.execute(command, values)
            db.commit()
            flash(f'{headline} added successfully!', 'success')
        except Error as e:
            flash(e, 'warning')

    return render_template('add_news.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', contact_us=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = db.cursor()
        command = 'INSERT INTO users(username, email, password) VALUES (%s, %s, %s);'
        values = (username, email, password)

        try:
            cursor.execute(command, values)
            db.commit()
            flash(f'{username} registered successfully!', 'success')
        except Error as e:
            flash(e, 'warning')

    return render_template('register.html', register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = db.cursor()
        command = 'SELECT * FROM users WHERE email = %s;'
        values = (email,)

        try:
            cursor.execute(command, values)
            data = cursor.fetchone()

            if password == data[2]:
                session['login'] = True
                session['username'] = data[0]
                flash(f'{data[0]} logged in successfully!', 'success')

                return redirect(home.__name__)
            else:
                flash('Wrong credentials!', 'warning')
        except Error as e:
            flash(e, 'warning')

    return render_template('login.html', login=True)


@app.route('/logout')
def logout():
    flash(f"{session['username']} logged out successfully!", 'success')

    session['login'] = False
    session['username'] = 'Guest'

    return redirect(home.__name__)


if __name__ == '__main__':
    app.run()
