from functools import wraps
from flask import redirect, session


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session['username']:
            return redirect('/login/')
        else:
            return f(*args, **kwargs)
    return wrap
