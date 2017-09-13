from flask import Flask, render_template, redirect, request, flash, session
from utils.forms import LoginForm, SignUpForm, AddNoteForm
import utils.functions as functions
from utils.decorators import login_required
from flask_pagedown import PageDown
import markdown
from flask import Markup
import datetime

app = Flask(__name__)
pagedown = PageDown(app)
app.secret_key = '8149omkar'


@app.route('/')
def home_page():
    try:
        if session['username']:
            return render_template('index.html', username=session['username'])
        return render_template('index.html')
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
        password = functions.generate_password_hash(request.form['password'])
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
        password = functions.generate_password_hash(request.form['password'])
        email = request.form['email']
        check = functions.check_username(username)
        if check:
            flash('Username already taken!')
        else:
            functions.signup_user(username, password, email)
            session['username'] = username
            user_id = functions.check_user_exists(username, password)
            session['id'] = user_id
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
        note_markdown = form.note.data
        note = Markup(markdown.markdown(note_markdown))
        functions.add_note(note_title, note, note_markdown, session['id'])
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


@app.route("/notes/edit/<id>/", methods=['GET', 'POST'])
@login_required
def edit_note(id):
    form = AddNoteForm()
    if request.method == 'GET':
        data = functions.get_data_using_id(id)
        form.note_title.data = data[0][3]
        form.note.data = data[0][5]
        return render_template('edit_note.html', form=form, username=session['username'], id=session['id'])
    elif form.validate_on_submit():
            note_title = request.form['note_title']
            note_markdown = form.note.data
            print(note_markdown)
            note = Markup(markdown.markdown(note_markdown))
            functions.edit_note(note_title, note, note_markdown, session['id'])
            return redirect('/profile/')


@app.route("/notes/delete/<id>/", methods=['GET', 'POST'])
@login_required
def delete_note(id):
    '''
        App for viewing a specific note
    '''
    functions.delete_note_using_id(id)
    notes = functions.get_data_using_user_id(session['id'])
    return render_template('profile.html', delete=True, username=session['username'], notes=notes)


# Custom Filter
@app.template_filter()
def custom_date(date):
    '''
        Convert a datetime into custom format like: Sep 12,2017 19:07:32
    '''
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date.strftime('%b %d,%Y %H:%M:%S')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
