from flask import Blueprint, Flask, render_template, url_for, jsonify, session, request, redirect, g
from elice_library.models import User, Book, Rental, Comment
from datetime import date, datetime
from elice_library import db
from elice_library.views.auth_views import login_required
from elice_library.forms import CommentForm

# 블루프린트 객체 생성. 이름('main'), 모듈명, URL_prefix의 값을 전달해준다.
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if g.user is not None:
            page = request.args.get('page', type=int, default=1) # 페이지
            book_list = Book.query.order_by(Book.id.asc())
            book_list = book_list.paginate(page, per_page=8)
            return render_template('loggedin.html', book_list=book_list)
        else:
            return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        book_id = request.form['book_id']
        book = Book.query.get(book_id)
        if book.stock != 0:
            rental = Rental(book_id=book_id, user=g.user, rental_date=datetime.today())
            book.stock -= 1
            db.session.add(rental)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close()
            # db.session.commit()
            page = request.args.get('page', type=int, default=1) # 페이지
            book_list = Book.query.order_by(Book.id.asc())
            book_list = book_list.paginate(page, per_page=8)
            return render_template('loggedin.html', book_list=book_list)
        else:
            return '남은 책이 없습니다.'

# @bp.route('/register', methods=['GET','POST'])
# def register():
#     if request.method == 'POST':
#         # 회원가입 정보(이름, 이메일, 비밀번호)를 받음
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         user = User(username, email, password)
#         # 이메일이 존재하는 경우 return 해준다.
#         member_list = User.query.filter(User.email == email)
#         for member in member_list:
#             return "이미 가입된 회원입니다."
#         db.session.add(user)
#         db.session.commit()
#         # url_for('main.index') 에서 main은 등록된 블루프린트 이름
#         # index는 블루프린트에 등록된 함수명이다.
#         return redirect(url_for('main.index'))
#     else:
#         return render_template('register.html')

# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # 로그인 정보 받음
#         email = request.form['email']
#         password = request.form['password']
        
#         member_list = User.query.filter(User.email == email)
#         for member in member_list:
#             if member.password == password:
#                 session['logged_in'] = True
#                 session['user_id'] = member.id
#                 return redirect(url_for('main.index'))
#             else:
#                 return '비밀번호가 틀립니다.'
#         return '이메일이 없습니다.'
#     else:
#         return render_template('index.html')

# @bp.route("/logout")
# def logout():
#     # 세션값을 False로 바꿔주고 홈으로 이동
#     session['logged_in'] = False
#     session.pop('user_id')
#     return redirect(url_for('main.index'))

@bp.route("/rental")
def rental():
    rental_list = Rental.query.filter(Rental.user==g.user)
    return render_template('rental.html', rental_list=rental_list)

@bp.route("/back", methods=['GET', 'POST'])
def back():
    if request.method == 'GET':
        rental_list = Rental.query.filter(Rental.user==g.user)
        return render_template('back.html', rental_list=rental_list)
    elif request.method == 'POST':
        id = request.form['id']
        rental = Rental.query.filter(Rental.id==id).first()
        rental.book.stock += 1
        rental.return_date = datetime.today()
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        # db.session.commit()
        page = request.args.get('page', type=int, default=1) # 페이지
        book_list = Book.query.order_by(Book.id.asc())
        book_list = book_list.paginate(page, per_page=8)
        return render_template('loggedin.html', book_list=book_list)

@bp.route("/book/<int:id>/", methods=['GET', 'POST'])
def book(id):
    form = CommentForm()
    book_info = Book.query.filter(Book.id==id).first()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            rating = request.form['rating']
        except: 
            rating = 0
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), book=book_info, rating=rating)
        db.session.add(comment)
        comment_all = Comment.query.filter(Comment.book==book_info)
        comment_len = Comment.query.filter(Comment.book==book_info).all()
        rating_all = 0
        for comment_each in comment_all:
            rating_all += int(comment_each.rating)
        rating_portion = rating_all//len(comment_len)
        rating_rest = rating_all/len(comment_len) - rating_portion
        if rating_rest >= 0.5:
            rating_rest = 1
        else:
            rating_rest = 0
        book_info.rating = rating_portion + rating_rest
        db.session.commit()
        # return redirect(url_for('main.book', id=id))
        return redirect('{}#comment_{}'.format(url_for('main.book', id=id), comment.id))
    elif request.method == 'GET':
        comment_set = reversed(book_info.comment_set)
        comment_all = Comment.query.filter(Comment.book==book_info)
        comment_len = Comment.query.filter(Comment.book==book_info).all()
        rating_all = 0
        for comment_each in comment_all:
            rating_all += int(comment_each.rating)
        rating_avg = rating_all/len(comment_len)
        return render_template('bookinfo.html', book_info=book_info, form=form, comment_set=comment_set, rating_avg=rating_avg)
        