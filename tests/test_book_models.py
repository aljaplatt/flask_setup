import unittest

from unittest.mock import patch

from models.book_models import add_book, get_all_books, get_book, hard_delete_book, soft_delete_book_update

from helpers.helper import validate_limit_offset

# class TestPostBookErr(unittest.TestCase):
#     @patch("pymongo.collection.Collection.insert_one", side_effect=InsertOneError({}))
#     def test_add_book_err(self, mock_insert_one, ins_one_err):
#         with self.assertRaises(SpecialInsertOneExcep) as context:
#             mock_insert_one()
#     # def test_add_book_err(self, mock_add_book):
#         # mock_add_book.status_code = 500
#         # mock_add_book.return_value = ('Could not connect to db', 500)

#             self.assertEqual(add_book({"title": "Encyclopaedia Americana"}), tuple(
#                 ('Could not connect to db', 500)))


# Test mocking insert_one method in add_book function
class TestAddBook(unittest.TestCase):
    @patch("pymongo.collection.Collection.insert_one")
    def test_add_book(self, mock_insert_one):
        mock_insert_one.return_value = {
            "title": "Encyclopaedia Americana ",
            "author": "Jane Austen",
            "synopsis": "The novel follows the character development of Elizabeth Bennet, the dynamic protagonist of the book who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.",
            'genre': 'Horror'
        }

        self.assertEqual(
            add_book(
                {
                    "title": "Encyclopaedia Americana ",
                    "author": "Jane Austen",
                    "synopsis": "The novel follows the character development of Elizabeth Bennet, the dynamic protagonist of the book who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.",
                    'genre': 'Horror'
                }
            ),
            tuple(
                (
                    {
                        'message': 'Book successfully added'
                    },
                    201
                )
            )
        )


    @patch("pymongo.collection.Collection.insert_one", side_effect=ConnectionError(({"message": "Could not connect to db"}, 500)))
    def test_add_book_exception(self, mock_insert_one):
            # mock_insert_one.side_effect = ConnectionError({"message": "Could not connect to db"})
        self.assertEqual( add_book(
                {
                    "title": "Encyclopaedia Americana ",
                    "author": "Jane Austen",
                    "synopsis": "The novel follows the character development of Elizabeth Bennet, the dynamic protagonist of the book who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness.",
                    'genre': 'Horror'
                }
            ),
            tuple(
                (
                    {
                        "message": "Could not connect to db"
                    },
                    500
                )
            )
        )


# Mocking find_one method in get_book function
@patch("pymongo.collection.Collection.find_one")
class TestGetSingleBook(unittest.TestCase):
    def test_get_single_book(self, mock_find_one):
        mock_find_one.return_value = {
            "_id": "a236ab92-14b8-11ed-9490-beb2bf7533dc",
            "author": "Chimamanda", 
            "genre": "historical",
            "synopsis": "The novel follows the character development of Elizabeth Bennet, the dynamic protagonist...", 
            "title": "Half of a yellow sun",
            "links": {
                "reservations": "/books/a236ab92-14b8-11ed-9490-beb2bf7533dc/reservations",
                "reviews": "/books/a236ab92-14b8-11ed-9490-beb2bf7533dc/reviews",
                "self": "/books/a236ab92-14b8-11ed-9490-beb2bf7533dc" 
            }
        }

        self.assertEqual(
            get_book(
                "ca1a5f26-0902-11ed-8431-beb2bf7533dc", "localhost:5000"
            ),
            ({
             "_id": "a236ab92-14b8-11ed-9490-beb2bf7533dc",
            "author": "Chimamanda", 
            "genre": "historical",
            "synopsis": "The novel follows the character development of Elizabeth Bennet, the dynamic protagonist...", 
            "title": "Half of a yellow sun",
            "links": {
                "reservations": "http://localhost:5000/books/a236ab92-14b8-11ed-9490-beb2bf7533dc/reservations",
                "reviews": "http://localhost:5000/books/a236ab92-14b8-11ed-9490-beb2bf7533dc/reviews",
                "self": "http://localhost:5000/books/a236ab92-14b8-11ed-9490-beb2bf7533dc" 
            }   
            }, 200)
        )


# class TestDeleteBook(unittest.TestCase):
#     @patch("pymongo.collection.Collection.delete_one")
#     def test_delete_book(self, mock_delete_one):
#         result = delete_book('abf41f1c-17ff-11ed-b78a-5a9c62168dfe')

#         {
#     "Book ID": "abf41f1c-17ff-11ed-b78a-5a9c62168dfe",
#     "Deleted count": 1,
#     "message": "Book removed from library"
# }


# @patch("models.model.validate_limit_offset")
@patch("pymongo.collection.Collection.find")
class TestGetAllBooks(unittest.TestCase):
    def test_get_all_books(self, mock_find):
        mock_find.return_value = [{
            "author": "James Clavell",
            "genre": "Historical fiction",
            "links": {
                "reservations": "/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations",
                "reviews": "/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reviews",
                "self": "/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe"
            },
            "synopsis": "The only way to learn python!",
            "title": "The Shogun"
        }]
        

        self.assertEqual(get_all_books("localhost:5000",20,0,"_id",1),
                         ({
            "items": [{
            "author": "James Clavell",
            "genre": "Historical fiction",
            "links": {
                "reservations": "http://localhost:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reservations",
                "reviews": "http://localhost:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe/reviews",
                "self": "http://localhost:5000/books/f06b92ee-0c1d-11ed-be41-5a9c62168dfe"
            },
            "synopsis": "The only way to learn python!",
            "title": "The Shogun"
        }],
            "total_count": 1
        }, 200)
        )

#? Mocking find_one and update_one in soft_delete_book_update
#! Need to check update_one return value. Thought it would be deleted, not available ??  
class TestSoftDeleteBookUpdate(unittest.TestCase):
    @patch("pymongo.collection.Collection.find_one")
    @patch("pymongo.collection.Collection.update_one")
    def test_soft_delete_book_update(self, mock_find_one, mock_update_one):
        mock_find_one.return_value = {
        '_id': 'd19584aa-1e2f-11ed-9a2b-5a9c62168dfe',
        'title': 'A Book',
        'synopsis': 'book',
        'author': 'author',
        'genre': 'genre',
        'state': 'available',
        "links": {
            "self": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe",
            "reservations": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reservations",
            "reviews": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reviews",
        }
        }

        mock_update_one.return_value = {
        '_id': 'd19584aa-1e2f-11ed-9a2b-5a9c62168dfe',
        'title': 'A Book',
        'synopsis': 'book',
        'author': 'author',
        'genre': 'genre',
        'state': 'available',
        "links": {
            "self": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe",
            "reservations": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reservations",
            "reviews": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reviews",
        }
        }

        self.assertEqual(soft_delete_book_update('d19584aa-1e2f-11ed-9a2b-5a9c62168dfe'), (
            {
            "message": "Book deleted"
            }, 200)
        )


    @patch("pymongo.collection.Collection.find_one")
    @patch("pymongo.collection.Collection.update_one")
    def test_soft_delete_book_update_exception(self, mock_find_one, mock_update_one):
        mock_find_one.return_value = {
        '_id': 'd19584aa-1e2f-11ed-9a2b-5a9c62168dfe',
        'title': 'A Book',
        'synopsis': 'book',
        'author': 'author',
        'genre': 'genre',
        'state': 'deleted',
        "links": {
            "self": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe",
            "reservations": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reservations",
            "reviews": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reviews",
        }
        }

        mock_update_one.return_value = {
        '_id': 'd19584aa-1e2f-11ed-9a2b-5a9c62168dfe',
        'title': 'A Book',
        'synopsis': 'book',
        'author': 'author',
        'genre': 'genre',
        'state': 'deleted',
        "links": {
            "self": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe",
            "reservations": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reservations",
            "reviews": f"/books/d19584aa-1e2f-11ed-9a2b-5a9c62168dfe/reviews",
        }
        }

        self.assertEqual(soft_delete_book_update('d19584aa-1e2f-11ed-9a2b-5a9c62168dfe'), (
            {"message": "Given book is already archived/no longer available"}, 404
            )
        )
    
    @patch("pymongo.collection.Collection.find_one", side_effect=ConnectionError(({"message": "Could not connect to db"}, 500)))
    @patch("pymongo.collection.Collection.update_one", side_effect=ConnectionError(({"message": "Could not connect to db"}, 500)))
    def test_soft_delete_book_update(self, mock_find_one, mock_update_one):
        self.assertEqual(soft_delete_book_update('d19584aa-1e2f-11ed-9a2b-5a9c62168dfe'), (
            {"message": "Could not connect to db"}, 500
            )
        )


if __name__ == "__main__":
    unittest.main()
