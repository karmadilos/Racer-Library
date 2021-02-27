import csv
from datetime import date, datetime
from elice_library.models import Book
from elice_library import db, create_app

app = create_app()
app.app_context().push()

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
                    open(f"./elice_library/static/images/{row['id']}.png")
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