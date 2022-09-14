from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.comment import Comment

@app.route('/view_book/<int:book_id>/add_comment', methods=['GET','POST'])
def add_comment(book_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if request.method == 'GET':
        return render_template('view_book.html')
    else:
        if not Comment.validate_comment(request.form):
            return redirect('/view_book')
        data= {
                'comment' : request.form['comment'],
                'user_id' : session['user_id'],
                'book_id' : book_id
            }
        Comment.add_comment(data)
        return redirect('/view_book/' + str(book_id))
