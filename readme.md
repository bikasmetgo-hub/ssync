uvicorn app.main:app --reload


uvicorn app.main:app --host 0.0.0.0 --port 10000

alembic revision -m "add other" --autogenerate
alembic upgrade head