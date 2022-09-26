from flask import Blueprint, request

# from app.routes import book

from book_models.models import (
    add_book,
    get_all_books,
    get_book,
    hard_delete_book,
    soft_delete_book_update,
)
from helpers.helper import get_args, validate_sort, sort_books

# 1. name for obj, pass in the name of the module being loaded - routes.py
book_req = Blueprint("book_req", __name__)

# get list of all books from db
@book_req.route("/")
def get_books():
    host_name = request.headers.get("host")
    args = request.args

    limit_offset = get_args(args)
    if 400 in limit_offset:
        return limit_offset
    limit = limit_offset[0]
    offset = limit_offset[1]

    valid_sort = validate_sort(args)
    if not valid_sort:
        valid_sort = ("title", 1)
    if 400 in valid_sort:
        return valid_sort

    check_books_or_reservations = sort_books(valid_sort)
    if 400 in check_books_or_reservations:
        return check_books_or_reservations

    sort = valid_sort[0]
    asc_desc = valid_sort[1]

    response = get_all_books(host_name, limit, offset, sort, asc_desc)
    return response


# post a single book to db
@book_req.route("/", methods=["POST"])
def post_book():
    data = request.get_json()
    response = add_book(data)
    return response


# get a single book from db
@book_req.route("/<book_id>", methods=["GET"])
def find_one_book(book_id):
    host_name = request.headers.get("host")
    response = get_book(book_id, host_name)
    return response


# Delete book from db
@book_req.route("/<book_id>", methods=["DELETE"])
def hard_delete_one_book(book_id):
    response = hard_delete_book(book_id)
    return response


# soft delete book (set state to deleted - keep in db)
@book_req.route("/<book_id>", methods=["PATCH"])
def soft_delete_single_book(book_id):
    response = soft_delete_book_update(book_id)
    return response
