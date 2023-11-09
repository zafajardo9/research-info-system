# PUPRIZ


## Backend

1. Before run our project install poetry to your pc check here https://python-poetry.org/
2. Run virtual environment or venv folder just using script `.\venv\Scripts\activate` on windows
NOTE: Use 'alembic revision -m "Update Table"' when adding
3. Generate table to your database go to backend folder run  `alembic upgrade head`
4. Run backend using script `poetry run start`


## DEV
1. pip install poetry
2. poetry add uvicorn fastapi sqlalchemy==1.4.49 sqlmodel asyncpg psycopg2 alembic jose passlib Crypto
3. poetry export -f requirements.txt --without-hashes > requirements.txt
4. pip install -r requirements.txt

## Frontend

1. Run frontend `npm start`
