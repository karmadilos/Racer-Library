from flask import Blueprint, Flask, render_template, url_for, jsonify, session, request, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from elice_library import db
from elice_library.forms import UserCreateForm, UserLoginForm
from elice_library.models import User, Book, Rental, Comment
from elice_library.views.auth_views import login_required
from datetime import date, datetime

import functools

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/info', methods=['GET', 'POST'])
def info():
    user_list = User.query.filter(User.id==session['user_id'])
    return render_template('mypage/my_info.html', user_list=user_list)

@bp.route('/rental', methods=['GET', 'POST'])
def rental():
    rental_list = Rental.query.filter(Rental.user_id==session['user_id'])
    return render_template('mypage/my_rental.html', rental_list=rental_list)

@bp.route('/comment', methods=['GET', 'POST'])
def comment():
    comment_list = Comment.query.filter(Comment.user_id==session['user_id'])
    return render_template('mypage/my_comment.html', comment_list=comment_list)

@bp.route('/delete/<int:rental_id>')
@login_required
def rental_delete(rental_id):
    rental = Rental.query.get(rental_id)
    if g.user != rental.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('mypage.rental'))
    db.session.delete(rental)
    db.session.commit()
    return redirect(url_for('mypage.rental'))