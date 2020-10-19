docker start redis
source ../venv/bin/activate
cd ../project
daphne -p 8001 Kolibrina.asgi:application
