ENV = . ./venv/bin/activate ; cd ./project

CREATE_ENV = python3.9 -m virtualenv venv ; \
			 $(ENV) ; \
			 pip install -U pip ; \
			 pip install -r requirements.txt

ENV_SELENIUM = . ./bin/selenium/venv/bin/activate

MIGRATIONS = python3.9 manage.py makemigrations ; \
			 python3.9 manage.py migrate

COLLECT_STATIC = $(SETTINGS_PROD) ; \
				 python3.9 manage.py collectstatic

RUNSERVER_DEV = python3.9 manage.py runserver --settings=Kolibrina.settings_dev 127.0.0.1:8002
START_DAPHNE = daphne -p 8001 Kolibrina.asgi\:application

#-----------CELERY----------------------------------------#
SETTINGS_DEV = export DJANGO_SETTINGS_MODULE=Kolibrina.settings_dev
SETTINGS_PROD = export DJANGO_SETTINGS_MODULE=Kolibrina.settings
CELERY_WORKER = python3.9 -m celery -A Kolibrina worker -l info
CELERY_BEAT = python3.9 -m celery -A Kolibrina beat -l info
#-----------CELERY----------------------------------------#
dev:
	$(ENV) ; \
	$(SETTINGS_DEV) ; \
	$(RUNSERVER_DEV)
init_prod:
	$(CREATE_ENV) ; \
	$(MIGRATIONS) ; \
	$(COLLECT_STATIC) ; \
	python3.9 manage.py init ; \
	cd .. ; \
	python3.9 ./bin/initProject.py

init_dev:
	$(CREATE_ENV) ; \
	$(MIGRATIONS) ; \
	python3.9 manage.py init -d 1 ; \
	cd .. ; \
	python3.9 ./bin/initProject.py


collectstatic:
	$(ENV) ; \
	$(SETTINGS_PROD) ; \
	$(COLLECT_STATIC)


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

celery_worker_prod:
	$(ENV) ; \
	$(SETTINGS_PROD) ; \
	$(CELERY_WORKER)
celery_worker_dev:
	$(ENV) ; \
	$(SETTINGS_DEV) ; \
	$(CELERY_WORKER)

celery_beat_prod:
	$(ENV) ; \
	$(SETTINGS_PROD) ; \
	$(CELERY_BEAT)

celery_beat_dev:
	$(ENV) ; \
	$(SETTINGS_DEV) ; \
	$(CELERY_BEAT)
shell_dev:
	$(ENV) ; \
	$(SETTINGS_DEV) ; \
    python3.9 manage.py shell
shell_prod:
	$(ENV) ; \
	$(SETTINGS_PROD) ; \
    python3.9 manage.py shell
start_daphne:
	$(ENV) ; \
	$(SETTINGS_PROD) ; \
	$(START_DAPHNE)


clean_all:
	$(ENV) ; \
	cd ../bin ; \
	python3.9 clean_migrations.py; \
	python3.9 clean_cache.py

clean_migrations:
	$(ENV) ; \
	cd ../bin ; \
	python3.9 clean_migrations.py

clean_cache:
	$(ENV) ; \
	cd ../bin ; \
	python3.9 clean_cache.py

createsuperuser:
	$(ENV) ; \
	$(CREATESUPERUSER)


add_marafon_EL:
	$(ENV_SELENIUM) ; \
	python3.9 ./bin/selenium/add_marafon_EL.py

add_tournament_EL:
	$(ENV_SELENIUM) ; \
	python3.9 bin/selenium/add_tournament_week.py

zip:
	zip -r kolibrina.zip . -x '*/venv/*' 'venv/*' '.git/*' '.idea/*' '.gitignore' '*/__pycache__/*' '*/db.sqlite3' 'README.md';


cold_start_prod:
	tmux new -s prod -d ; \
	tmux split-window -v -t prod:1.1 ; \
	tmux split-window -h -t prod:1.2 ; \
	tmux split-window -v -t prod:1.3 ; \
	tmux send-keys -t prod:1.4 '$(ENV)' Enter ; \
	tmux send-keys -t prod:1.4 '$(SETTINGS_PROD)' Enter ; \
	tmux send-keys -t prod:1.4 '$(CELERY_BEAT)' Enter ; \
	tmux send-keys -t prod:1.3 '$(ENV)' Enter ; \
	tmux send-keys -t prod:1.3 '$(SETTINGS_PROD)' Enter ; \
	tmux send-keys -t prod:1.3 '$(CELERY_WORKER)' Enter ; \
	tmux send-keys -t prod:1.2 '$(ENV)' Enter ; \
	tmux send-keys -t prod:1.2 '$(SETTINGS_PROD)' Enter ; \
	tmux send-keys -t prod:1.2 'redis-cli' Enter ; \
	tmux send-keys -t prod:1.1 '$(ENV)' Enter ; \
	tmux send-keys -t prod:1.1 '$(SETTINGS_PROD)' Enter ; \
	tmux send-keys -t prod:1.1 '$(START_DAPHNE)' Enter ; \
	tmux attach -t prod


cold_start_dev:
	tmux new -s dev -d ; \
	tmux split-window -v -t dev:1.1 ; \
	tmux split-window -h -t dev:1.2 ; \
	tmux split-window -v -t dev:1.3 ; \
	tmux send-keys -t dev:1.4 '$(ENV)' Enter ; \
	tmux send-keys -t dev:1.4 '$(SETTINGS_DEV)' Enter ; \
	tmux send-keys -t dev:1.4 '$(CELERY_BEAT)' Enter ; \
	tmux send-keys -t dev:1.3 '$(ENV)' Enter ; \
	tmux send-keys -t dev:1.3 '$(SETTINGS_DEV)' Enter ; \
	tmux send-keys -t dev:1.3 '$(CELERY_WORKER)' Enter ; \
	tmux send-keys -t dev:1.2 '$(ENV)' Enter ; \
	tmux send-keys -t dev:1.2 '$(SETTINGS_DEV)' Enter ; \
	tmux send-keys -t dev:1.2 'redis-cli' Enter ; \
	tmux send-keys -t dev:1.1 '$(ENV)' Enter ; \
	tmux send-keys -t dev:1.1 '$(SETTINGS_DEV)' Enter ; \
	tmux send-keys -t dev:1.1 '$(RUNSERVER_DEV)' Enter ; \
	tmux attach -t dev
