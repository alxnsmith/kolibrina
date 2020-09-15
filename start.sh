cd ~/Projects/kolibrinaMAIN
until [[ $VIRTUAL_ENV == "/home/nillkizz/Projects/kolibrinaMAIN/env3.8" ]]; do 
    source ./env3.8/bin/activate
done
cd project
python3.8 manage.py runserver 0.0.0.0:8080
