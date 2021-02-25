# -- coding: utf-8 --
from flask import Flask, render_template, url_for, jsonify, session, request, redirect
import pymysql
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
import csv
from datetime import date, datetime

db = SQLAlchemy()

migrate = Migrate()

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.app_context().push()

# from models import User
# from models import Book

@app.route('/')
def index():
    if session.get('logged_in'):
        book_list = Book.query.all()
        return render_template('loggedin.html', book_list=book_list)
    else:
        return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # 회원가입 정보(이름, 이메일, 비밀번호)를 받음
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(username, email, password)
        # 이메일이 존재하는 경우 return 해준다.
        member_list = User.query.filter(User.email == email)
        for member in member_list:
            return "이미 가입된 회원입니다."
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 로그인 정보 받음
        email = request.form['email']
        password = request.form['password']
        
        member_list = User.query.filter(User.email == email)
        for member in member_list:
            if member.password == password:
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                return '비밀번호가 틀립니다.'
        return '이메일이 없습니다.'
    else:
        return render_template('index.html')

@app.route("/logout")
def logout():
    # 세션값을 False로 바꿔주고 홈으로 이동
    session['logged_in'] = False
    return render_template('index.html')

@app.route("/book/<int:id>/")
def book(id):
    book_info = Book.query.filter(Book.id==id)
    return render_template('bookinfo.html', book_info=book_info)

if __name__ == "__main__":
    from models import User
    from models import Book

    book_first = Book.query.first()
    if book_first == None:
        with app.app_context():
            with open('./BackData/library.csv', 'r', encoding='UTF8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    published_date = datetime.strptime(
                                    row['publication_date'], '%Y-%m-%d').date()
                    image_path = f"../static/images/{row['id']}"
                    try:
                        open(f'app/{image_path}.png')
                        image_path += '.png'
                    except:
                        image_path += '.jpg'

                    book = Book(
                        # id=int(row['id']), 
                        bookname=row['book_name'], 
                        publisher=row['publisher'],
                        author=row['author'], 
                        published_date=published_date, 
                        pages=int(row['pages']),
                        isbn=row['isbn'], 
                        description=row['description'], 
                        image_path=image_path,
                        stock=5,
                        rating=0,
                        link=row['link']
                    )
                    db.session.add(book)
                db.session.commit()
    app.run(debug=True)