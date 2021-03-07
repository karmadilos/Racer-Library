from flask import Blueprint, Flask, render_template, url_for, jsonify, session, request, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from elice_library import db
from elice_library.forms import UserCreateForm, UserLoginForm
from elice_library.models import User, Book, Rental, Comment
from datetime import date, datetime

import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# 블루프린트 객체 생성. 이름('main'), 모듈명, URL_prefix의 값을 전달해준다.
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # filter_by 와 filter는 조금 다르다. 비교해보며 공부하자.
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "가입되지 않은 이메일입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/user', methods=['GET', 'POST'])
def user():
    user_list = User.query.all()
    return render_template('auth/admin_user.html', user_list=user_list)

@bp.route('/book', methods=['GET', 'POST'])
def book():
    book_list = Book.query.all()
    return render_template('auth/admin_book.html', book_list=book_list)

@bp.route('/rental', methods=['GET', 'POST'])
def rental():
    rental_list = Rental.query.all()
    return render_template('auth/admin_rental.html', rental_list=rental_list)

@bp.route('/change')
@login_required
def password_change(user_id):
    user = User.query.get(user_id)
    if g.user != user:
        flash('비밀번호 변경 권한이 없습니다')
        return redirect(url_for('mypage.info'))
    session.clear()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('mypage.info'))

@bp.route('/withdraw<int:user_id>')
@login_required
def withdraw(user_id):
    user = User.query.get(user_id)
    if g.user != user:
        flash('탈퇴권한이 없습니다')
        return redirect(url_for('mypage.info'))
    session.clear()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.index'))