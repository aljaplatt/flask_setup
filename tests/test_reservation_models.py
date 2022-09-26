import unittest

from unittest.mock import patch

from models.reservation_models import get_reservation, get_all_reservations, update_reservation


# Mocking find_one method in get_reservation function
@patch("pymongo.collection.Collection.find_one")
class TestGetSingleReservation(unittest.TestCase):
    def test_get_single_reservation(self, mock_find_one):
        mock_find_one.return_value = {
    "_id": "055b8afa-0e8b-11ed-abd2-beb2bf7533db",
    "book_id": "dfc9815c-0840-11ed-9ca5-beb2bf7533dc",
    "links": {
        "book": "http://127.0.0.1:5000/books/dfc9815c-0840-11ed-9ca5-beb2bf7533dc",
        "self": "http://127.0.0.1:5000/books/dfc9815c-0840-11ed-9ca5-beb2bf7533dc/reservations/055b8afa-0e8b-11ed-abd2-beb2bf7533db"
    },
    "state": "reserved",
    "user": {
        "forenames": "Mary",
        "surname": "Poppins"
    }
}

        self.assertEqual(
            get_reservation(
                "dfc9815c-0840-11ed-9ca5-beb2bf7533dc", "055b8afa-0e8b-11ed-abd2-beb2bf7533db"
            ),
            (
                {
    "_id": "055b8afa-0e8b-11ed-abd2-beb2bf7533db",
    "book_id": "dfc9815c-0840-11ed-9ca5-beb2bf7533dc",
    "links": {
        "book": "http://127.0.0.1:5000/books/dfc9815c-0840-11ed-9ca5-beb2bf7533dc",
        "self": "http://127.0.0.1:5000/books/dfc9815c-0840-11ed-9ca5-beb2bf7533dc/reservations/055b8afa-0e8b-11ed-abd2-beb2bf7533db"
    },
    "state": "reserved",
    "user": {
        "forenames": "Mary",
        "surname": "Poppins"
    }
}
            , 200)
        )


# Mocking update_one method in get_reservation function
@patch("pymongo.collection.Collection.update_one")
class TestGetSingleReservation(unittest.TestCase):
    def test_update_single_reservation(self, mock_update_one):
        mock_update_one.return_value = {
    "_id": "055b8afa-0e8b-11ed-abd2-beb2bf7533db",
    "book_id": "dfc9815c-0840-11ed-9ca5-beb2bf7533dc",
    "links": {
        "book": "http://127.0.0.1:5000/books/dfc9815c-0840-11ed-9ca5-beb2bf7533dc",
        "self": "http://127.0.0.1:5000/books/dfc9815c-0840-11ed-9ca5-beb2bf7533dc/reservations/055b8afa-0e8b-11ed-abd2-beb2bf7533db"
    },
    "state": "reserved",
    "user": {
        "forenames": "Hajara",
        "surname": "Iyal"
    }
}

        self.assertEqual(
            update_reservation(
                "dfc9815c-0840-11ed-9ca5-beb2bf7533dc", "055b8afa-0e8b-11ed-abd2-beb2bf7533db", {"forenames":"Hajara", "surname":"Iyal"}
            ),
            (
                {'message': 'Reservation updated'}, 200)
        )


# ? Test mocking find method in get_all_reservations function
class TestGetAllReservations(unittest.TestCase):
    @patch("pymongo.collection.Collection.find")
    def test_get_all_reservations(self, mock_find):
        mock_find.return_value = [{
            "_id": "68b20d96-0f48-11ed-ab8f-5a9c62168dfe",
            "book_id": "f06b92ee-0c1d-11ed-be41-5a9c62168dfe",
            "links": {
                "book": "/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe",
                "self": "/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations/68b20d96-0f48-11ed-ab8f-5a9c62168dfe"
            },
            "state": "reserved",
            "user": {
                "forenames": "Ronald",
                "surname": "McDonald"
            }
        }]

        self.assertEqual(get_all_reservations('f06b92ee-0c1d-11ed-be41-5a9c62168dfe', "localhost:5000", 20, 0, 'surname',1), 
                         ({
            "items": [
        {
            "_id": "68b20d96-0f48-11ed-ab8f-5a9c62168dfe",
            "book_id": "f06b92ee-0c1d-11ed-be41-5a9c62168dfe",
            "links": {
                "book": "http://localhost:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe",
                "self": "http://localhost:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations/68b20d96-0f48-11ed-ab8f-5a9c62168dfe"
            },
            "state": "reserved",
            "user": {
                "forenames": "Ronald",
                "surname": "McDonald"
            }
        }
            ],
            "total_count": 1
        }, 200)
       )

#! Testing exception when mocking find method in get_all_reservations function 
    @patch("pymongo.collection.Collection.find", side_effect=ConnectionError(({"message": "Could not connect to db"}, 500)))
    def test_get_all_reservations_exception(self, mock_find):

        self.assertEqual( get_all_reservations('f06b92ee-0c1d-11ed-be41-5a9c62168dfe', "localhost:5000", 20, 0, 'surname',1),
            tuple(
                (
                    {
                        "message": "Could not connect to db"
                    },
                    500
                )
            )
        )


if __name__ == "__main__":
    unittest.main()