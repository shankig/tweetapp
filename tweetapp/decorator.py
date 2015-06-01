from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    """
    decorator that checks oauth toekn present in session.
    """
    
    @wraps(func)
    def inner(*args, **kwargs):
        if 'twitter_oauth' not in session:
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return inner