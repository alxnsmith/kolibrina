cd
cd /home/nillkizz/Projects/kolibrina
echo "~/Projects/kolibrina"
until [[ $VIRTUAL_ENV == "/home/nillkizz/Projects/kolibrina/venv" ]]; do 
    echo "$VIRTUAL_ENV"
    source ./venv/bin/activate
    echo "./venv/bin/activate"
done
echo "done"
cd project
echo "cd project"
echo "running manage.py runserver"
python3 manage.py runserver 0.0.0.0:8000
