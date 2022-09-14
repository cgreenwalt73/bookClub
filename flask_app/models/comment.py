from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    db = 'books'

    def __init__( self , data ):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.book_id = data['book_id']

    @classmethod
    def add_comment(cls, data):
        query="""
        INSERT INTO
        comments ( comment, created_at, updated_at, user_id, book_id)
        VALUES ( %(comment)s, NOW(), NOW(), %(user_id)s, %(book_id)s )
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_comments_by_book_id(cls, book_id):
        data= {'book_id' : book_id}
        query="""
        SELECT * 
        FROM comments
        JOIN users ON users.id = comments.user_id
        WHERE book_id = %(book_id)s
        ;"""
        results= connectToMySQL(cls.db).query_db(query, data)
        comments = []
        for comment in results:
            comments.append( cls(comment) )
            print('****', comment, '****')
        return comments

    @classmethod
    def edit_comment(cls, data):
        query="""
        UPDATE comments
        SET comment = %(comment)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def comment(cls, id):
        data= {'id' : id}
        query="""
        DELETE FROM comments 
        WHERE comments.id= %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_comment(comment):
        is_valid=True
        if len(comment['comment']) < 3:
            flash("Comment must be at least 3 characters")
            is_valid=False
        return is_valid