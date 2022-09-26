from dbconfig.mongo import db
import sys

import os
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    print('UP: ',user_paths)
except KeyError:
    user_paths = []



def check_db():
    try:
        books = db.books.find()
        array = []

        for book in books:
            array.append(book)
    
        count = len(array)
        if count > 0:
            return ('db is not empty')
        else:
            return ('db is empty')
    except:
        print('unable to run')
        

def delete_library():
    try:
        count = check_db()
        if count == 'db is empty':
            print('Error: Books cannot be deleted. db is empty.')
            sys.exit(0)
        else: 
            books = db.books
            result = books.delete_many({})
            print('Message: All books deleted successfully')         
            return ('Message: All books deleted successfully')
    except:
        print("Could not connect to db")
        sys.exit(1)

    
delete_library()