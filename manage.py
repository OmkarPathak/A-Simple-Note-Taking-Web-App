from flask import (
    Flask, render_template,
    redirect, request,
    flash, session,
    jsonify
)

from utils.forms import (
    LoginForm, SignUpForm,
    AddNoteForm, AddTagForm,
    ChangeEmailForm, ChangePasswordForm
)

from flask_restful import Resource, Api, reqparse
from utils.decorators import login_required
from flask_pagedown import PageDown
from flask import Markup
import utils.functions as functions
import datetime
import markdown
import random

app = Flask(__name__)
api = Api(app)
pagedown = PageDown(app)
parser = reqparse.RequestParser()
app.secret_key = str(random.randint(1, 20))

@app.route('/')
def home_page():
    '''
        App for hompage
    '''
    session['user_count'] = functions.get_user_count()
    try:
        if session['username']:
            return render_template('homepage.html', username=session['username'])
        return render_template('homepage.html')
    except (KeyError, ValueError):
        return render_template('homepage.html')


@app.route('/profile/')
@login_required
def profile():
    '''
        App for user profile can only be accessed only after successful login
    '''
    if request.method == 'GET':
        notes = functions.get_data_using_user_id(session['id'])
        tags = []
        if notes:
            for note in notes:
                tags_list = functions.get_tag_using_note_id(note[0])
                temp_list = []
                if tags_list:
                    for tag in tags_list:
                        temp = functions.get_data_using_tag_id(tag)
                        if temp is not None:
                            temp_list.append(temp[0])
                tags.append(', '.join(temp_list))
        return render_template(
            'profile.html',
            username=session['username'],
            notes=notes,
            tags=tags
        )


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
            functions.store_last_login(session['id'])
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
    form.tags.choices = functions.get_all_tags(session['id'])

    if form.tags.choices is None:
        form.tags = None

    if form.validate_on_submit():
        note_title = request.form['note_title']
        note_markdown = form.note.data
        note = Markup(markdown.markdown(note_markdown))

        try:
            tags = form.tags.data
            tags = ','.join(tags)
        except:
            tags = None

        functions.add_note(note_title, note, note_markdown, tags, session['id'])
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


@app.route("/notes/edit/<note_id>/", methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    '''
        App for editing a particular note
    '''
    form = AddNoteForm()
    form.tags.choices = functions.get_all_tags(session['id'])
    form.tags.default = functions.get_tag_using_note_id(note_id)
    form.tags.process(request.form)

    if form.tags.choices is None:
        form.tags = None

    if request.method == 'GET':
        data = functions.get_data_using_id(note_id)
        form.note_id.data = note_id
        form.note_title.data = data[0][3]
        form.note.data = data[0][5]
        return render_template('edit_note.html', form=form, username=session['username'], id=note_id)
    elif form.validate_on_submit():
        note_id = form.note_id.data
        note_title = request.form['note_title']
        note_markdown = form.note.data

        try:
            tags = form.tags.data
            tags = ','.join(tags)
        except:
            tags = None

        note = Markup(markdown.markdown(note_markdown))
        functions.edit_note(note_title, note, note_markdown, tags, note_id=note_id)
        return redirect('/profile/')


@app.route("/notes/delete/<id>/", methods=['GET', 'POST'])
@login_required
def delete_note(id):
    '''
        App for viewing a specific note
    '''
    functions.delete_note_using_id(id)
    notes = functions.get_data_using_user_id(session['id'])
    tags = []
    if notes:
        for note in notes:
            tags_list = functions.get_tag_using_note_id(note[0])
            temp_list = []
            if tags_list:
                for tag in tags_list:
                    temp = functions.get_data_using_tag_id(tag)
                    if temp is not None:
                        temp_list.append(temp[0])
            tags.append(', '.join(temp_list))
    return render_template('profile.html', delete=True, tags=tags, username=session['username'], notes=notes)


@app.route("/tags/add/", methods=['GET', 'POST'])
@login_required
def add_tag():
    '''
        App for adding a tag
    '''
    form = AddTagForm()
    if form.validate_on_submit():
        tag = request.form['tag']
        functions.add_tag(tag, session['id'])
        return redirect('/profile/')
    return render_template('add_tag.html', form=form, username=session['username'])


@app.route("/tags/")
@login_required
def view_tag():
    '''
        App for viewing all available tags
    '''
    tags = functions.get_all_tags(session['id'])
    return render_template('edit_tag.html', tags=tags, username=session['username'])


@app.route("/tags/view/<tag_id>")
@login_required
def view_notes_using_tag(tag_id):
    '''
        App for viewing all available notes tagged under specific tag
    '''
    notes = functions.get_notes_using_tag_id(tag_id, session['id'])
    tag_name = functions.get_tagname_using_tag_id(tag_id)
    return render_template(
        'view_tag.html',
        notes=notes,
        username=session['username'],
        tag_name=tag_name
    )


@app.route("/tags/delete/<tag_id>/")
@login_required
def delete_tag(tag_id):
    '''
        App for deleting a specific tag
    '''
    functions.delete_tag_using_id(tag_id)
    tags = functions.get_all_tags(session['id'])
    return render_template('edit_tag.html', tags=tags, delete=True, username=session['username'])


# Custom Filter
@app.template_filter()
def custom_date(date):
    '''
        Convert a datetime into custom format like: Sep 12,2017 19:07:32
    '''
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date.strftime('%b %d,%Y %H:%M:%S')


@app.route("/profile/settings/")
@login_required
def profile_settings():
    '''
        App for getting profile settings for a user
    '''
    user_data = functions.get_user_data(session['id'])
    notes_count = functions.get_number_of_notes(session['id'])
    tag_count = functions.get_number_of_tags(session['id'])
    return render_template(
        'profile_settings.html',
        user_data=user_data,
        username=session['username'],
        notes_count=notes_count,
        tag_count=tag_count
    )


@app.route("/profile/settings/change_email/", methods=['GET', 'POST'])
@login_required
def change_email():
    '''
        App for changing the email of a user
    '''
    form = ChangeEmailForm()
    if form.validate_on_submit():
        email = request.form['email']
        functions.edit_email(email, session['id'])
        return redirect('/profile/settings/')
    return render_template('change_email.html', form=form, username=session['username'])


@app.route("/profile/settings/change_password/", methods=['GET', 'POST'])
@login_required
def change_password():
    '''
        App for changing the password of a user
    '''
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = request.form['password']
        functions.edit_password(password, session['id'])
        return redirect('/profile/settings/')
    return render_template('change_password.html', form=form, username=session['username'])


@app.route('/background_process/')
def background_process():
    '''
        App for handling AJAX request for searching notes
    '''
    try:
        notes = request.args.get('notes')
        if notes == '':
            return jsonify(result='')
        results = functions.get_search_data(str(notes), session['id'])
        temp = ''
        for result in results:
            temp += "<h4><a href='/notes/" + str(result[0]) + "/'>" + result[1] + "</a></h4><br>"
        return jsonify(result=Markup(temp))
    except Exception as e:
        return str(e)


class GetDataUsingUserID(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            username = args['username']
            password = functions.generate_password_hash(args['password'])
            user_id = functions.check_user_exists(username, password)
            if user_id:
                functions.store_last_login(user_id)
                return functions.get_rest_data_using_user_id(user_id)
            else:
                return {'error': 'You cannot access this page, please check username and password'}
        except AttributeError:
            return {'error': 'Please specify username and password'}

api.add_resource(GetDataUsingUserID, '/api/')
parser.add_argument('username')
parser.add_argument('password')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
