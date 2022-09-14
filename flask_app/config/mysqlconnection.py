# a cursor is used to interact with the database
import pymysql.cursors
# this class will give an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # establishing the connection
        self.connection = connection
    # query method for the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries return nothing
                    self.connection.commit()
            except Exception as e:
                # if query fails, the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using then uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)