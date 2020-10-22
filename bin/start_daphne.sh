docker start redis
source ../env/bin/activate
cd ../project
daphne -p 8001 Kolibrina.asgi:application
