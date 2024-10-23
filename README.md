# stat_track

Single repo that contains two Django projects. Both are dockerized and can be run with docker-compose. Two apps are communicating via Django Rest Framework. Using PostgreSQL as database. Celery is used for scheduled tasks. Redis is used as cache to reduce the load for API.

Bootstrap 5 is used for better visual style. Some JavScript on client side and JS library for building charts.

How to run:
prepare your environment variables.
run:
docker-compose up -d

env variables:
WARGAMING_API_KEY - your World of Tanks API key. Can be generated here: https://developers.wargaming.ne
DJANGO_LOG_LEVEL - desired log level for Django logger (INFO is default)
