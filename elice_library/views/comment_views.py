from datetime import datetime
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from elice_library import db
from elice_library.forms import CommentForm
from elice_library.models import Book, Comment
from elice_library.views.auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/book/<int:book_id>', methods=('GET', 'POST'))
@login_required
def create_comment(book_id):
    form = CommentForm()
    book = Book.query.get(book_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), book=book)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.book', book_id=book_id))
    return render_template('comment/comment_form.html', form=form)

@bp.route('/modify/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    book_info = comment.book
    book_id = book_info.id
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('main.book', id=comment.book.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(url_for('main.book', id=book_id), comment.id))
            # return redirect(url_for('main.book', id=comment.book.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('bookinfo.html', book_info=book_info, form=form)

@bp.route('/delete/<int:comment_id>')
@login_required
def delete(comment_id):
    comment = Comment.query.get(comment_id)
    book_id = comment.book.id
    book_info = Book.query.filter(Book.id==book_id).first()
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('main.book', id=book_id))
    db.session.delete(comment)
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
    return redirect('{}#comment_{}'.format(url_for('main.book', id=book_id), comment.id))
    # return redirect(url_for('main.book', id=book_id))