from flask import Flask, render_template, redirect, request, flash, session
from utils.forms import LoginForm, SignUpForm, AddNoteForm
import utils.functions as functions
from utils.decorators import login_required
import markdown
from flask import Markup
from flask.ext.pagedown import PageDown

app = Flask(__name__)
pagedown = PageDown(app)
app.secret_key = '8149omkar'


@app.route('/')
def home_page():
    try:
        content = """##Chapter"""
        content = Markup(markdown.markdown(content))
        print(content)
        if session['username']:
            return render_template('index.html', username=session['username'])
        return render_template('index.html', content=content)
    except (KeyError, ValueError):
        return render_template('index.html')


@app.route('/profile/')
@login_required
def profile():
    '''
        App for user profile can only be accessed only after successful login
    '''
    if request.method == 'GET':
        notes = functions.get_data_using_user_id(session['id'])
        return render_template('profile.html', username=session['username'], notes=notes)


@app.route('/login/', methods=('GET', 'POST'))
def login():
    '''
        App for creating Login page
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user_id = functions.check_user_exists(username, password)
        if user_id:
            session['username'] = username
            session['id'] = user_id
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
    '''
        App for logging out user
    '''
    session['username'] = None
    session['id'] = None
    return login()


@app.route("/notes/add/", methods=['GET', 'POST'])
@login_required
def add_note():
    '''
        App for adding note
    '''
    form = AddNoteForm()
    if form.validate_on_submit():
        note_title = request.form['note_title']
        note = request.form['note']
        functions.add_note(note_title, note, session['id'])
        return redirect('/profile/')
    return render_template('add_note.html', form=form, username=session['username'])


@app.route("/notes/<id>/")
@login_required
def view_note(id):
    '''
        App for viewing a specific note
    '''
    notes = functions.get_data_using_id(id)
    return render_template('view_note.html', notes=notes, username=session['username'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
