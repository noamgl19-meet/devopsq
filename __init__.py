from flask import Flask, render_template,send_from_directory, redirect, request, url_for, session as login_session
import os
import datetime
from database import *

#app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf movies'

shir = ['1','2','3']




############## redirect to login ###############
@app.route("/")
def index():
	return redirect(url_for('login'))

############## help queue ##############
@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_password(username, password):
            login_session['username'] = username
            return redirect(url_for('home'))
        else:
            msg = "login failed: username and password does not match"
    return render_template('login.html', msg = msg)

start_time = 0
@app.route('/home', methods = ['GET', 'POST'])
def home():
    global start_time
    if 'username' in login_session:
        username = login_session['username']
        staff = False
        if get_user(con(), username).role != 'student':
            staff = True
            return redirect(url_for('view'))
        if start_time != 0:
            now = str(datetime.datetime.now() - start_time)[:-7]
        else:
            now = 0
        if len(get_student_reqs(con(), username)) == 0:
            now = 0
        amount = len(get_reqs(con()))

        if request.method == 'POST':
            question = request.form['question']
            name = request.form['demo-name']
            if (len(str(question)) <= 60):
                add_request(con(), name, question)
                add_r(con(), username)

                if len(get_student_reqs(con(), username)) != 0 and start_time == 0:
                    print("it is")
                    start_time = datetime.datetime.now()
            else:
                return render_template("index2.html", username = username, now = now, reqs = get_student_reqs(con(), username), amount = amount, staff = staff, msg = "question must be under 60 characters.")




        return render_template('index2.html',username = username, now = now, reqs = get_student_reqs(con(), username), amount = amount, staff = staff)
    else:
        return redirect(url_for('login'))

@app.route('/view', methods = ['GET', 'POST'])
def view():
    if 'username' in login_session:
        username = login_session['username']
        if get_user(con(),username).role != 'student':
            reqs = get_reqs(con())
            amount = len(reqs)
            if request.method == 'POST':
                ID = request.form['ID']
                update(con(),ID,username)
                print(get_reqs(con()))
                return redirect(url_for('view'))
            return render_template('view.html', username = username, amount = amount, reqs = reqs, requests = get_user(con(),username).counter)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    login_session.pop('username', None)
    return redirect(url_for('login'))


############## portal #################
@app.route('/portal', methods = ['GET', 'POST'])
def portal_login():
    msg = ''
    if request.method == 'GET':
        return render_template('portal_login.html')
    else:
        username = request.form['username']
        password = request.form['password']

        if check_password(username, password):
            if get_user(con(), username).role == 'staff':
                login_session['username'] = username
                return redirect(url_for('portal'))
            else:
                login_session['username'] = username
                return redirect(url_for('home'))
        else:
            msg = "login failed: username and password does not match"
    return render_template('portal_login.html', msg = msg)

@app.route('/portal/home')
def portal():
    if 'username' in login_session and get_user(con(), login_session['username']).role == 'staff':
        username = login_session['username']
        requests = get_reqs(con())
        dates = []
        for r in requests:
            if r.date in dates:
                pass
            else:
                dates.append(r.date)
        students = get_all_students(con())
        return render_template('portal.html', username = username, dates = dates, requests = requests, students = students, date = str(datetime.datetime.now())[0:10])
    else:
        return redirect(url_for('portal_login'))



if __name__ == '__main__':
    app.run(debug=True)
