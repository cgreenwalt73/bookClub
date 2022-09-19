from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

class Book:
    db = 'books'

    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    # Now we use class methods to query our database
    @classmethod
    def get_all_books(cls):
        query = """
        SELECT * 
        FROM books
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        books = []
        for book in results:
            books.append( cls(book) )
        return books

    @classmethod
    def add_book(cls, data):
        query="""
        INSERT INTO
        books ( title, author, description, created_at, updated_at, user_id)
        VALUES ( %(title)s, %(author)s, %(description)s, NOW(), NOW(), %(user_id)s )
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_book_by_id(cls, id):
        data= {'id' : id}
        query="""
        SELECT * 
        FROM books
        WHERE id = %(id)s
        ;"""
        results= connectToMySQL(cls.db).query_db(query, data)
        if results:
            results = cls(results[0])
        return results

    @classmethod
    def edit_book(cls, data):
        query="""
        UPDATE books
        SET title = %(title)s, author = %(author)s, description = %(description)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_book(cls, id):
        data= {'id' : id}
        query="""
        DELETE FROM comments
        WHERE book_id = %(id)s;
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        query="""
        DELETE FROM books 
        WHERE books.id= %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_book(book):
        is_valid=True
        if len(book['title']) < 3:
            flash("Title must be at least 3 characters")
            is_valid=False
        if len(book['author']) < 5:
            flash("Author's name must be at least 5 characters")
            is_valid=False
        if len(book['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid=False
        return is_valid