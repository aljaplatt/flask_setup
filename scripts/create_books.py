import json
from dbconfig.mongo import db
from helpers.helper import format_script, check_valid
with open("scripts/test_data/books.json", "r") as f:
    data = json.load(f)

def add_book(data): 
    formatted_book = format_script(data) 
    validBookChecked = check_valid(formatted_book)
    if validBookChecked == "author":
        return ("Author field must contain text characters", 400)
    elif validBookChecked == "incomplete":
        return ("All fields are mandatory", 400)
    try:
        books = db.books
        books.insert_one(formatted_book)
        return ({"message": "Book successfully added"}, 201)
    except:
        return ({"message": "Could not connect to db"}, 500)

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


def handle_books(data):
    count = check_db()
    if count == 'db is not empty':
        print('Error: Books cannot be added. db not empty.')
    else: 
        for book in data:
            add_book(book)
        print('Message: Books added successfully')
    return('Books added successfully')


handle_books(data)




