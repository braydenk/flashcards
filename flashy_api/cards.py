from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flashy_api.auth import login_required
from flashy_api.db import get_db

bp = Blueprint('cards', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    cards = db.execute(
        'SELECT * FROM cards WHERE user_id=?', (g.user['id'])
    ).fetchall()
    return render_template('cards/index.html', cards=cards)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        front = request.form['front']
        back = request.form['back']
        error = None

        if not front:
            error = 'Front is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO cards (front, back, user_id)'
                ' VALUES (?, ?, ?)',
                (front, back, g.user['id'])
            )
            db.commit()
            return redirect(url_for('cards.index'))

    return render_template('cards/create.html')

def get_card(id, check_author=True):
    card = get_db().execute(
        'SELECT c.id, front, back, created_at, user_id, username'
        ' FROM cards c JOIN users u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if card is None:
        abort(404, "Card id {0} doesn't exist.".format(id))

    if check_author and card['user_id'] != g.user['id']:
        abort(403)

    return card

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    card = get_card(id)

    if request.method == 'POST':
        front = request.form['front']
        back = request.form['back']
        error = None

        if not front:
            error = 'Front is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE card SET front = ?, back = ?'
                ' WHERE id = ?',
                (front, back, id)
            )
            db.commit()
            return redirect(url_for('cards.index'))

    return render_template('cards/update.html', card=card)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_card(id)
    db = get_db()
    db.execute('DELETE FROM cards WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('cards.index'))
