from functools import wraps
from flask import redirect, session


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if not session['username']:
                return redirect('/login/')
            else:
                return f(*args, **kwargs)
        except KeyError:
            return redirect('/login/')
    return wrap
