import unittest
from unittest.mock import patch

from helpers.helper import check_valid, check_reservation_valid, count_all_items, format_book

# Test checking isValid
class TestCheckValid(unittest.TestCase):
    def test_check_valid(self):
        result = check_valid({
            '_id': 12345,
            'title': 'The Stand',
            'author': 'Stephen King',
            'genre': 'Horror'})
        self.assertEqual(result, 'valid')

    # Test checking isValid with incomplete data

    def test_check_complete(self):
        result = check_valid({
            '_id': 12345,
            'title': '',
            'synopsis': 'Creepy doomsday tome',
            'author': 'Stephen King',
            'genre': 'Horror'})
        self.assertEqual(result, 'incomplete')

    # Test checking isValid with incorrect data type

    def test_check_correct(self):
        result = check_valid({
            '_id': 12345,
            'title': 'The Stand',
            'synopsis': 'Creepy doomsday tome',
            'author': 99,
            'genre': 'Horror'})
        self.assertEqual(result, 'author')


class TestCountAllBooks(unittest.TestCase):
    # Success case for count_all_books
    def test_count_all_items(self):
        result = count_all_items([1, 2, 3, 4, 5])
        self.assertEqual(result, 5)


# class FormatBook(unittest.TestCase):
    @patch("helpers.helper.generate_uuid_str", return_value=123)
    def test_format_book(self, mock_generate_uuid_str):
        result = format_book({
                            'title': 'Garry Totter', 
                            'author': 'Dostoyevsky', 
                            'synopsis': 'The only way to learn python!.', 
                            'genre': 'Fiction',
                            'state': 'available',
                            })
        self.assertEqual(result, {
        '_id': 123,
        'title': 'Garry Totter',
        'synopsis': 'The only way to learn python!.',
        'author': 'Dostoyevsky',
        'genre': 'Fiction',
        'state': 'available',
        "links": {
            "self": f"/books/123",
            "reservations": f"/books/123/reservations",
            "reviews": f"/books/123/reviews",
        }})

class CheckReservationValid(unittest.TestCase):
    def test_check_reservation_valid(self):
        result = check_reservation_valid({'_id': '123', 'state': 'reserved', 'user': {'forenames': 'Ronald', 'surname': 'Mcdonald'}, 'book_id': 'f06b92ee-0c1d-11ed-be41-5a9c62168dfe', 'links': {'self': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations/74203086-0f52-11ed-9f53-5a9c62168dfe', 'book': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe'}})
        self.assertEqual(result, 'valid')

    def test_check_reservation_valid_forenames_not_valid(self):
        result = check_reservation_valid({'_id': '123', 'state': 'reserved', 'user': {'forenames': '', 'surname': 'Mcdonald'}, 'book_id': 'f06b92ee-0c1d-11ed-be41-5a9c62168dfe', 'links': {'self': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations/74203086-0f52-11ed-9f53-5a9c62168dfe', 'book': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe'}})
        self.assertNotEqual(result, 'valid')
    
    def test_check_reservation_forename_message(self):
        result = check_reservation_valid({'_id': '123', 'state': 'reserved', 'user': {'forenames': '', 'surname': 'Mcdonald'}, 'book_id': 'f06b92ee-0c1d-11ed-be41-5a9c62168dfe', 'links': {'self': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations/74203086-0f52-11ed-9f53-5a9c62168dfe', 'book': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe'}})
        self.assertEqual(result, 'forenames')
    
    def test_check_reservation_surname_message(self):
        result = check_reservation_valid({'_id': '123', 'state': 'reserved', 'user': {'forenames': 'Ronald', 'surname': ''}, 'book_id': 'f06b92ee-0c1d-11ed-be41-5a9c62168dfe', 'links': {'self': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations/74203086-0f52-11ed-9f53-5a9c62168dfe', 'book': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe'}})
        self.assertEqual(result, 'surname')

    def test_check_reservation_valid_surnames_invalid(self):
        result = check_reservation_valid({'_id': '123', 'state': 'reserved', 'user': {'forenames': 'Ronald', 'surname': ''}, 'book_id': 'f06b92ee-0c1d-11ed-be41-5a9c62168dfe', 'links': {'self': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations/74203086-0f52-11ed-9f53-5a9c62168dfe', 'book': 'http://127.0.0.1:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe'}})
        self.assertNotEqual(result, 'valid')

if __name__ == "__main__":
    unittest.main()
