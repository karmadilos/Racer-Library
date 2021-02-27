from elice_library import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
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
    
# db세팅법
# 0. 폴더 위치를 myproject로 이동
# 1. export FLASK_APP=racer-library
# 2. export FLASK_ENV=development
# 3. flask db init (최초 한번 수행. 데이터베이스를 관리하는 초기 파일들을 migrations라는 디렉터리에 생성)
# 4. flask db migrate (모델을 새로 생성하거나 변경할때 사용.)
# 5. flask db upgrade (모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용)