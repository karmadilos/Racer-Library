from elice_library import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published_date = db.Column(db.DateTime(), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(50), nullable=False)

    def __init__(self, bookname, publisher, author, published_date, pages, isbn, description, image_path, stock, rating, link):
        self.bookname = bookname
        self.publisher = publisher
        self.author = author
        self.published_date = published_date
        self.pages = pages
        self.isbn = isbn
        self.description = description
        self.image_path = image_path
        self.stock = stock
        self.rating = rating
        self.link = link

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('rental_set'))
    book = db.relationship('Book', backref=db.backref('rental_set'))
    rental_date = db.Column(db.DateTime(), nullable=False)
    return_date =db.Column(db.DateTime(), nullable=True)

    def __init__(self, user_id, book_id, rental_date):
        self.user_id = user_id
        self.book_id = book_id
        self.rental_date = rental_date

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('comment_set'))
    book = db.relationship('Book', backref=db.backref('comment_set'))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self,user_id, book_id, content, rating):
        self.user_id = user_id
        self.book_id = book_id
        self.content = content
        self.rating = rating

# db세팅법
# 0. 현재 위치를 racer-library로 이동
# 1. export FLASK_APP=elice_library
# 2. export FLASK_ENV=development
# 3. flask db init (최초 한번 수행. 데이터베이스를 관리하는 초기 파일들을 migrations라는 디렉터리에 생성)
# 4-0. 만약 flask db migrate를 했는데 Target database is not up to date. 오류 발생시
# 4-0. flask db heads (migrate 작업의 최종 리비전 보기)
# 4-0. flask db current (migrate 작업의 현재 리비전 보기)
# 4-0. flask db stamp head (현재 리비전을 최종 리비전으로 변경. 최종 리비전(head)과 현재 리비전(current)이 같은 값으로 변경)
# 4. flask db migrate (모델을 새로 생성하거나 변경할때 사용.)
# 5. flask db upgrade (모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용)