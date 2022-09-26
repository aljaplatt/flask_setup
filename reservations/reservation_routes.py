from flask import Blueprint,request

from models.reservation_models import add_reservation,get_reservation, get_all_reservations, update_reservation
from helpers.helper import get_args, validate_sort, sort_reservations

reservation_req = Blueprint("reservations", __name__)

@reservation_req.route('/<book_id>/reservations', methods=['POST'])
def post_reservation(book_id):
    host_name = request.headers.get('host')
    reservation_book_id = book_id
    data = request.get_json()
    response = add_reservation(data, reservation_book_id, host_name)
    return response

# get all reservations under a book
@reservation_req.route('/<book_id>/reservations', methods=['GET'])
def get_reservations(book_id):
    host_name = request.headers.get('host')
    args = request.args
    limit_offset = get_args(args)
    if 400 in limit_offset:
        return limit_offset
    limit = limit_offset[0]
    offset = limit_offset[1]

    valid_sort = validate_sort(args)
    if not valid_sort:
        valid_sort = ('surname', 1)
    if 400 in valid_sort:
        return valid_sort

    check_books_or_reservations = sort_reservations(valid_sort)
    if 400 in check_books_or_reservations:
        return check_books_or_reservations

    sort = valid_sort[0]
    asc_desc = valid_sort[1]

    response = get_all_reservations(book_id, host_name, limit, offset, sort, asc_desc)
    return response


# get a single reservation from db
@reservation_req.route('/<book_id>/reservations/<res_id>', methods=['GET'])
def find_one_reservation(book_id, res_id):
    host_name = request.headers.get('host')
    response = get_reservation(book_id, res_id, host_name)
    return response


# update a reservation from db
@reservation_req.route('/<book_id>/reservations/<res_id>', methods=['PATCH'])
def update_single_reservation(book_id, res_id):
    data = request.get_json()
    response = update_reservation(book_id, res_id, data)
    return response