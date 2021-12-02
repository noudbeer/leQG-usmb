from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from leQG.auth import login_required
from leQG.db import get_db

bp = Blueprint('profile', __name__)

def get_user(id):
    user = get_db().execute(
        'SELECT u.id, username'
        ' FROM user u'
        ' WHERE u.id = ?',
        (id,)
    ).fetchone()

    if user is None:
        abort(404, f"user id {id} doesn't exist.")

    return user


@bp.route('/profile/<int:id>', methods=['GET'])
@login_required
def index(id):
    db = get_db()

    user = get_user(id)

    posts = db.execute(
        'SELECT p.id, title, body, created, author_id'
        ' FROM post p'
        ' WHERE p.author_id = ?',
        (id,),
        # ' ORDER BY created DESC' 
    ).fetchall()

    return render_template('user/profile.html', user=user, posts=posts)


@bp.route('/search', methods=['GET'])
@login_required
def search():
    username = request.args.get('username', '')

    db = get_db()
    users = db.execute(
        'SELECT *'
        ' FROM user u'
        ' WHERE u.username = ?',
        (username,),
        # ' ORDER BY username DESC' 
    ).fetchall()

    return render_template('user/search.html', users=users, search=username)