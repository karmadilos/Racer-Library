import csv
from datetime import date, datetime

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

app.app_context().push()

with app.app_context():
    with open('./BackData/library.csv', 'r', encoding='UTF8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            published_date = datetime.strptime(
                            row['publication_date'], '%Y-%m-%d').date()
            image_path = f"/static/image/{row['id']}"
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