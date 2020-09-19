cd ~/PycharmProjects/kolibrinaMain
until [[ $VIRTUAL_ENV == "/home/nillkizz/PycharmProjects/kolibrinaMain/venv" ]]; do 
    source ./venv/bin/activate
done
cd project
python manage.py runserver 0.0.0.0:8000
