from dbconfig.mongo import db
from helpers.helper import (check_uuid, check_valid, count_all_items,
                            format_book, append_host,validate_limit_offset)


# add a book to db
def add_book(data):
    formatted_book = format_book(data)
    print(formatted_book)
    validBookChecked = check_valid(formatted_book)
    if validBookChecked == "author":
        return ("Author field must contain text characters", 400)
    elif validBookChecked == "incomplete":
        return ("All fields are mandatory", 400)
    else:
        try:
            books = db.books
            books.insert_one(formatted_book)
            return ({"message": "Book successfully added"}, 201)
        except:
            return ({"message": "Could not connect to db"}, 500)


# retrieve a single book based on a given id
def get_book(data,host):
    validBookId = check_uuid(data)
    if validBookId == "Invalid ID":
        return ("Given book ID is invalid", 404)
    else:
        try:
            books = db.books
            book = books.find_one({"_id": validBookId})
            if book['state'] != 'available':
                return ("Given book is unavailable", 404)
            result = append_host(book, host)
            return (result, 200)
        except:
            return ({"message": "Could not connect to db"}, 500)

# retrieve a list of books
def get_all_books(host_name,limit,offset, sort, asc_desc):
    validation_result = validate_limit_offset(limit, offset)
    if validation_result == 'Invalid':
        return ({'message': 'Limit/Offset must be above 0'}, 400)
    else:
        try:
            books = db.books
            results = books.find(
                {"state": 'available'},
                {
                    "_id": 1,
                    "title": 1,
                    "synopsis": 1,
                    "author": 1,
                    "genre": 1,
                    "state": 1,
                    "links": 1,
                },
            ).limit(limit).skip(offset).sort(sort, asc_desc)

            items_arr = []
            for result in results:
                new_result = append_host(result,host_name)
                items_arr.append(new_result)
            
            count = count_all_items(items_arr)
            return {"total_count": count, "items": items_arr}, 200
        except:
            return {"message": "Could not connect to db"}, 500


def hard_delete_book(book_id):
    validBookId = check_uuid(book_id)
    if validBookId == "Invalid ID":
        return ({"message": "Given book ID is invalid"}, 404)
    else:
        try:
            books = db.books
            result = books.delete_one({"_id": validBookId})
            return ({"message": "Book removed from library", "Book ID": validBookId, "Deleted count": result.deleted_count}, 204)
        except:
            return ({"message": "Could not connect to db"}, 500)


def soft_delete_book_update(book_id):
    validBookId = check_uuid(book_id)
    if validBookId == "Invalid ID":
        return ({'message':"Book ID is not valid/book does not exist"}, 404)  
    else:
        try:
            books = db.books
            book = books.find_one({"_id": book_id})
            if book['state'] == 'deleted':
                return ({"message": "Given book is already archived/no longer available"}, 404)
            books.update_one({'_id': book_id}, {"$set": {'state':'deleted'}})
            # if books['state'] == 'deleted':
            #     return({'message':'Book no longer available'}, 200)
            # elif books['state'] == 'available':
            #     return({'message':'Book now available'}, 200)
            return({'message':'Book deleted'},200)
        except:
            return ({"message": "Could not connect to db"}, 500)

