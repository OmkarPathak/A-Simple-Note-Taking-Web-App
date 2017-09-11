from flask import Flask, render_template, redirect, request, flash, session
from utils.forms import LoginForm, SignUpForm
import utils.functions as functions
from utils.decorators import login_required
app = Flask(__name__)
app.secret_key = '8149omkar'


@app.route('/')
def home_page():
    if session['username']:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')


@app.route('/profile/')
@login_required
def profile():
    '''
        App for user profile can only be accessed only after successful login
    '''
    return render_template('profile.html', username=session['username'])


@app.route('/login/', methods=('GET', 'POST'))
def login():
    '''
        App for creating Login page
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        check = functions.check_user_exists(username, password)
        if check:
            session['username'] = username
            return redirect('/profile/')
        else:
            flash('Username/Password Incorrect!')
    return render_template('login.html', form=form)


@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    '''
        App for registering new user
    '''
    form = SignUpForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        check = functions.check_username(username)
        if check:
            flash('Username already taken!')
        else:
            functions.signup_user(username, password, email)
            session['username'] = username
            return redirect('/profile/')
    return render_template('signup.html', form=form)


@app.route("/logout/")
def logout():
    session['username'] = None
    return login()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
