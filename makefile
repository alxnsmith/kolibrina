ENV = . ./venv/bin/activate ; \
	  cd ./project

CREATE_ENV = python3.9 -m venv ./venv ; \
			 $(ENV) ; \
			 pip install -U pip ; \
			 pip install -r requirements.txt



ENV_SELENIUM = . ./bin/selenium/venv/bin/activate


MIGRATIONS = python3.9 manage.py makemigrations ; \
			 python3.9 manage.py migrate




init:
	$(CREATE_ENV) ; \
	$(MIGRATIONS) ; \
	python3.9 manage.py init ; \
	cd .. ; \
	python3.9 ./bin/initProject.py ; \



init_selenium:
	python3.9 -m venv ./bin/selenium/venv ; \
	$(ENV_SELENIUM) ; \
	cd bin/selenium ; \
	pip install -U pip ; \
	pip install -r requirements.txt ; \
	python3.9 get_chromedriver.py


migrate:
	$(ENV) ; \
	$(MIGRATIONS)

dev:
	$(ENV) ; \
	python3.9 manage.py runserver --settings=Kolibrina.settings_dev 127.0.0.1:8002

shell:
	$(ENV) ; \
	python3.9 manage.py shell

start_daphne:
	$(ENV) ; \
    daphne -p 8001 Kolibrina.asgi\:application

clean_migrations:
	$(ENV) ; \
	cd ../bin ; \
	python3.9 clean_migrations.py

createsuperuser:
	$(ENV) ; \
	$(CREATESUPERUSER)


add_marafon_EL:
	$(ENV_SELENIUM) ; \
	python3.9 ./bin/selenium/add_marafon_EL.py
