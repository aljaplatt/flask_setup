import uuid
import os 
from flask import request
from dotenv import load_dotenv

def sort_books(sort):
    if sort[0] != 'author' and sort[0] != 'title':
        return ({'message': 'Sort criteria is not valid. eg: books must be Title or Author'}, 400)
    else:
        return sort


def sort_reservations(sort):
    if sort[0] != 'forenames' and sort[0] != 'surname':
        return ({'message': 'Sort criteria is not valid. eg: reservations must be forenames or surname'}, 400)
    else:
        return sort

def validate_sort(args):
    asc_or_desc = 1
    #* check if sort is in args 
    if 'sort' in args: 
        sort = request.args.get('sort')
        print('SORT: ', sort)
    #* if first char is -
        if sort[0] == '-':
            asc_or_desc = -1
            #* remove '-' char, reassign sort variable eg: sort = '-author' -> sort = 'author'
            sort = sort[1:]
        #* check if sort criteria is valid  
        if sort == 'author' or sort == 'title' or sort == 'forenames' or sort == 'surname':
            return (sort, asc_or_desc)
        else:
            return ({'message': 'Sort criteria is not valid.'}, 400)
    else:
        return False
        # return ('title', 1)



def get_args(args):
    load_dotenv()
    max_limit = int(os.getenv('MAX_LIMIT'))
    max_offset = int(os.getenv('MAX_OFFSET'))
    if 'limit' in args: 
        try: 
            limit = int(request.args.get('limit'))
        except:
            limit = 'invalid'
    else:
        limit = int(os.getenv('DEFAULT_LIMIT'))
        # limit = default_limit
    if 'offset' in args:
        try:
            offset = int(request.args.get('offset'))
        except:
            offset = 'invalid'
    else:
        offset = 0

    if limit > max_limit or limit < 0: 
        limit = 'invalid'
        result = ({'message': 'Limit must be between 0 - 1000.'}, 400)
        return result 

    if offset > max_offset or offset < 0: 
        offset = 'invalid'
        result = ({'message': 'Offset must be between 0 - 2000.'}, 400)
        return result 

    result = (limit, offset)
    
    if 'invalid' in result: 
        result = ({'message': 'Limit/Offset must be a number.'}, 400)
    return result


def validate_limit_offset(limit, offset):
        if limit < 0 or offset < 0:
            return ('Invalid')
        else:
            return ('Valid')


def generate_uuid_str():
    return str(uuid.uuid1())


def format_book(data):
    book_uuid = generate_uuid_str()
    book = {
        '_id': book_uuid,
        'title': data['title'],
        'synopsis': data['synopsis'],
        'author': data['author'],
        'genre': data['genre'],
        'state': 'available',
        "links": {
            "self": f"/books/{book_uuid}",
            "reservations": f"/books/{book_uuid}/reservations",
            "reviews": f"/books/{book_uuid}/reviews",
        },
    }
    return book
def format_book(data):
    book_uuid = generate_uuid_str()
    book = {
        '_id': book_uuid,
        'title': data['title'],
        'synopsis': data['synopsis'],
        'author': data['author'],
        'genre': data['genre'],
        'state': 'available',
        "links": {
            "self": f"/books/{book_uuid}",
            "reservations": f"/books/{book_uuid}/reservations",
            "reviews": f"/books/{book_uuid}/reviews",
        },
    }
    return book


def format_script(data):
    book_uuid = data['_id']
    book = {
        '_id': book_uuid,
        'title': data['title'],
        'synopsis': data['synopsis'],
        'author': data['author'],
        'genre': data['genre'],
        'state': 'available',
        "links": {
            "self": f"/books/{book_uuid}",
            "reservations": f"/books/{book_uuid}/reservations",
            "reviews": f"/books/{book_uuid}/reviews",
        },
    }
    return book


def append_host(book_obj, host):
    #* loop through the links obj of the incoming item
    http_host = f'http://{host}'
    for key in book_obj['links']:
        #? path = path['links'][key]
        #* concatenate the host and path to equal host_path
        host_path = http_host + book_obj['links'][key]
        #* set the value of each link to equal host_path
        book_obj['links'][key] = host_path
    return book_obj


def format_reservation(data, book_id):
    valid_book_id = check_uuid(book_id)
    if valid_book_id == "Invalid ID":
        return ("Given book ID is invalid/book does not exist", 404)
    else:
        reservation_id = generate_uuid_str()
        formatted_reservation = {
            '_id': reservation_id,
            'state': 'reserved',
            'user': {
                'forenames': data['forenames'],
                'surname': data['surname']
            },
            'book_id': valid_book_id,
            'links': {
                'self': f"/books/{valid_book_id}/reservations/{reservation_id}",
                'book': f"/books/{valid_book_id}"
            }
        }
    return formatted_reservation


def check_valid(book):
    if type(book['author']) != str:
        return ('author')
    elif not book['title'] or not book['author'] or not book['genre']:
        return ('incomplete')
    else:
        return 'valid'


def check_reservation_valid(reservation):
    if not reservation['user']['forenames']:
        return 'forenames'
    elif not reservation['user']['surname']:
        return 'surname'
    else:
        return 'valid'
    

def check_uuid(id):
    if len(id) < 36 or len(id) > 36:
        return ('Invalid ID')
    else:
        return id


def count_all_items(data):
    count = 0
    for item in data:
        count += 1

    return count



