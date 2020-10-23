ENV = 
	. ./env/bin/activate ; \
    	cd ./project 

MIGRATIONS =
	python3.9 manage.py makemigrations ; \
			python3.9 manage.py migrate

CREATESUPERUSER =
	$(ENV) ; \
				 echo "from django.contrib.auth import get_user_model; User = get_user_model(); "User.objects.create_superuser(username='admin',email='admin@kolibrina.ru', password='admin')" | python3.9 manage.py shell


CREATE_ENV = 
	python3.9 -m venv ./env ; \
	$(ENV) ; \
    pip install -U pip ; \
    pip install -r requirements.txt ; \


init:
	$(CREATE_ENV) ; \
	$(MIGRATIONS) ; \
	$(CREATESUPERUSER) ; \
	cd ./bin ; \
	python3.9 initProject.py


migrate:
	$(ENV) ; \
	$(MIGRATIONS)


start_daphne:
	$(ENV) ; \
    daphne -p 8001 Kolibrina.asgi\:application

