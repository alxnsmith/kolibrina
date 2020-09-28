cd
cd /home/nillkizz/PycharmProjects/kolibrina
echo "~/PycharmProjects/kolibrina"
until [[ $VIRTUAL_ENV == "/home/nillkizz/PycharmProjects/kolibrina/venv" ]]; do 
    echo "$VIRTUAL_ENV"
    source ./venv/bin/activate
    echo "./venv/bin/activate"
done
echo "done"
cd project
echo "cd project"
echo "running manage.py runserver"
python manage.py runserver 0.0.0.0:8000
