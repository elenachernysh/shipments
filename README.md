#TODO
run in docker + wait_for_postgres + create DB & user


Backend:
Python 3.9
AUTH - JWT token

Frontend:
Vue js

API:

GET /api/shipping/?simple_search=test - GET filtered list with pagination

POST /api/shipping/ - CREATE new shipping.
{"title": "title", "description": "description", "status": "draft"}

PATCH /api/shipping/1/ - update shipping.
{"status": "done"}

DELETE /api/shipping/1/