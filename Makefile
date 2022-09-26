test:
	pipenv run pytest

start:
	brew services start mongodb-community@5.0

stop:
	brew services stop mongodb-community@5.0

restart:
	brew services restart mongodb-community

flask:
	flask run

shell:
	pipenv shell

flake8:
	pipenv run flake8

isort:
	pipenv run isort

reservations:
	pipenv run python3 scripts/create_reservations.py

clean:
	pipenv run python3 scripts/delete_reservations.py; pipenv run python3 scripts/delete_books.py

setup:
	pipenv run python3 scripts/delete_books.py; pipenv run python3 scripts/delete_reservations.py; pipenv run python3 scripts/create_books.py; pipenv run python3 scripts/create_reservations.py

clean_books:
	pipenv run python3 scripts/delete_books.py

clean_res:
	pipenv run python3 scripts/delete_reservations.py

create_books:
	pipenv run python3 scripts/create_books.py
	
setup_books:
	pipenv run python3 scripts/delete_books.py; pipenv run python3 scripts/create_books.py
