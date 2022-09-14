from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.book import Book
from flask_app.models.comment import Comment


@app.route('/books/<int:id>')
def show_book(id):
    book_to_show = Book.get_book_by_id(id)
    return render_template('book.html', book_to_show=book_to_show)

@app.route('/add_book', methods=['GET','POST'])
def add_book():
    if 'user_id' not in session:
        return redirect('/logout')
    if request.method == 'GET':
        return render_template('book.html')
    else:
        if not Book.validate_book(request.form):
            return redirect('/add_book')
        data= {
                'title' : request.form['title'],
                'author' : request.form['author'],
                'description' : request.form['description'],
                'user_id' : session['user_id']
            }
        Book.add_book(data)
        return redirect('/dashboard')

@app.route('/view_book/<int:id>')
def view_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    book_to_view = Book.get_book_by_id(id)
    comments_to_display = Comment.get_comments_by_book_id(id)
    return render_template('view_book.html', book_to_view=book_to_view, comments_to_display=comments_to_display)

@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    book_to_edit= Book.get_book_by_id(id)
    if request.method == 'GET':
        return render_template('edit_book.html', book_to_edit=book_to_edit)
    else:
        if not Book.validate_book(request.form):
            return redirect('/edit_book/' + str(book_to_edit.id))
        Book.edit_book(request.form)
        return redirect('/dashboard')

@app.route('/delete_book/<int:id>')
def delete_book(id):
    if 'user_id' not in session:
        return redirect('/logout')
    Book.delete_book(id)
    return redirect('/dashboard')

