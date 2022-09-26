from dbconfig.mongo import db
import json


def get_book_ids():
    # ? gets book json file data
    file = open("scripts/test_data/books.json")
    books_data = json.load(file)
    if books_data:
        book_ids_list = []
        # ? loop through book data
        for book_dict in books_data:
            # ? take ids from dictionary and store in list of ids
            book_ids_list.append(book_dict["_id"])
        return book_ids_list
    else:
        # ? if there are no books, print and return false
        print("The library is currently empty")
        return False


# #? amended add_reservation function
def add_reservation(data, book_id):
    formatted_reservation = {
        "_id": data["_id"],
        "state": "reserved",
        "user": {"forenames": data["forenames"], "surname": data["surname"]},
        "book_id": book_id,
        "links": {
            "self": f"/books/{book_id}/reservations/{book_id}",
            "book": f"/books/{book_id}",
        },
    }
    # print('FORMATTED RESERVATION: ', formatted_reservation)
    try:
        reservations = db.reservations
        reservations.insert_one(formatted_reservation)
    except BaseException:
        print("Add reservations could not connect to db")


# ? loop through data list of reservations, on each reservation we call the add reservation fn and pass in a random book id
def populate_reservations():
    # ? gets reservation json file data
    file = open("scripts/test_data/reservations.json")
    reservation_data = json.load(file)
    book_ids_list = get_book_ids()

    try:
        # ? check if reservations exist
        reservations = db.reservations
        res_results = list(reservations.find({}))

        # ? check if db has books
        books = db.books
        books_results = list(books.find({}))

        # ?  if reservations already exist, exit function
        if res_results:
            print(
                "The reservations database is not empty. Delete all reservations then try again."
            )
            return
        # ?  if no books exist, exit function
        elif not books_results:
            print(
                "The books database is empty, populate the books database then try again."
            )
            return
        # ? if book_ids_list contains ids, loop reservation data & book id lists calling add_reservation function
        elif book_ids_list:
            for (a, b) in zip(reservation_data, book_ids_list):
                add_reservation(data=a, book_id=b)
            print("reservations finished adding")
    except BaseException:
        print("Populate reservations couldn't connect to the database")


# ? call populate_reservations, passing in json data
populate_reservations()
