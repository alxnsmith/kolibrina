# kolibrinaMain
<h1>To start project:</h1>
<ul>
  <li>Install&Run docker</li>
  <li>docker run -p 6379:6379 redis</li> #run redis
  <li>sudo apt update && sudo apt upgrade && sudo apt install python3 python3-dev python3-pip python3-venv git</li> #install software
<li>git clone https://login:password@github.com/Nillkizz/kolibrinaMAIN.git && mkdir -p kolibrinaMAIN/project/static/mediacontent/users</li> #init project
  <li>python3 -m venv kolibrinaMAIN/koliVENV && source ./kolibrinaMAIN/koliVENV/bin/activate</li> #create&activate venv
  <li>pip3 install -r kolibrinaMAIN/project/requirements.txt</li> #install moules
  <li>python3 kolibrinaMAIN/project/manage.py makemigrations && python3 kolibrinaMAIN/project/manage.py migrate</li> #makemigrations&migrate
  <li>python3 kolibrinaMAIN/project/manage.py runserver</li> #run local server
  <li></li>
</ul>
