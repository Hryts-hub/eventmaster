# eventmaster
Here is REST API for simple application eventmaster. 
Its supports authorization by email, authentication by token, creating events with remind, events statistic by day, 
by month and holidays statistic for users country by month.

You can clone the project and run it using SQLite or 
in Docker using PostgreSQL (needs adding docker-compose.yml and django_docker_file).
In manage.py you should set DJANGO_SETTINGS_MODULE with settings.py you would like use. 

### To test project site:

you can visit endpoints or put the code below into the jupyternotebook.

```Python
from requests import get, post

# registration
# country examples: belarus, bonaire-st-eustatius-saba, central-african-republic, sao-tome-and-principe, ...
# "offset":"3" or "0" (country and offset fields do not required)
# "0", 'Greenwich Mean time'
# "3", '3 hours'
data = {
    "email":"...@gmail.com", 
    "username":"...", 
    "password":"...", 
    "first_name":"...",
    "last_name":"...", 
    "country":"poland",
    "offset":"3"
}
response = get("https://blackdesert.ololosha.xyz/comrades/registration/",)
print(response) # <Response [405]>
response = post("https://blackdesert.ololosha.xyz/comrades/registration/", data=data)
print(response) # <Response [201]>
response.json()

# activation
# check email to get link
activation_link = "https://blackdesert.ololosha.xyz/comrades/activation/xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
webtoken = "xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
response = get(activation_link, )
print(response) # <Response [405]>
# login: enter email or username
data = {
    "login": "...@gmail.com"
}
response = post(f"https://blackdesert.ololosha.xyz/comrades/activation/{webtoken}", data=data)
print(response) # <Response [202]>

# login
response = get("https://blackdesert.ololosha.xyz/comrades/login/",)
print(response) # <Response [405]>
# login: enter email or username to get token by mail
data = {
    'login': "...@gmail.com",
    'password': "...",
}
response = post("https://blackdesert.ololosha.xyz/comrades/login/", data=data)
print(response) # <Response [200]>

# test create event
token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
response = get("https://blackdesert.ololosha.xyz/events/list_create_event/", headers=headers)
print(response) # <Response [200]>
#         "0", 'Do not remind'
#         "3600", '1 hour'
#         "7200", '2 hours'
#         "14400", '4 hours'
#         "86400", '1 day'
#         "604800", '1 week'
data = {
    "event":"test ....",
    "date_event":"2021-02-16",
    "start_time":"20:59",
    "end_time":"23:30",
    "remind": "3600"
}
response = post("https://blackdesert.ololosha.xyz/events/list_create_event/", headers=headers, data=data)
print(response) # <Response [201]>
response.json()

# statistic by user
headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
response = get("https://blackdesert.ololosha.xyz/events/statistic_by_user/", headers=headers)
print(response) # <Response [200]>
response.json()

# statistic by day
data = {
    "date_event":"2021-08-08",
}
headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
response = get("https://blackdesert.ololosha.xyz/events/statistic_day/", headers=headers, data=data)
print(response) # <Response [200]>
response.json()

# statistic by month
data = {
    "month":"2021-02",
}
headers={"Authorization": "Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
response = get("https://blackdesert.ololosha.xyz/events/statistic_month/", headers=headers, data=data)
print(response) # <Response [200]>
response.json()

# holidays by month
data = {
    "month":"2021-05",
}
headers={"Authorization": "Token 7912ede2bfa2066ddbc74e6a25b672160f111db7"}
response = get("https://blackdesert.ololosha.xyz/events/holidays_month/", headers=headers, data=data)
response.json()
```
### To test project with SQLite:
1. Clone the project, create virtual environment.
2. Create file .env in SQLite_settings folder
3. Put in .env:
```
export DJANGO_EMAIL_HOST_USER=...@gmail.com
export DJANGO_EMAIL_HOST_PASSWORD=...
export DJANGO_SECRET_KEY=...
```
4.In manage.py uncomment (another DJANGO_SETTINGS_MODULE should be commented).
```
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventmaster.SQLite_settings.settings')
```
5.Commands:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### To test project with Docker:
1. Clone the project
2. In manage.py uncomment (another DJANGO_SETTINGS_MODULE should be commented).
```
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventmaster.Postgre_settings.settings')
```
3.Add docker-compose.yml, django_docker_file and db_keys.txt
4.db_keys.txt:
```
POSTGRES_PASSWORD=...
POSTGRES_USER=...
POSTGRES_DB=...
EMAIL_HOST_USER=...@gmail.com
EMAIL_HOST_PASSWORD=...
SECRET_KEY=...
```
5.django_docker_file:
```
FROM ubuntu:20.04


RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install python3-pip
COPY ./eventmaster/requirements.txt /scripts/
RUN pip3 install -r /scripts/requirements.txt

RUN mkdir /eventmaster
WORKDIR /eventmaster
```
6.docker-compose.yml:
```
version : "3"


services:
  web:
    build:
      context: .
      dockerfile: django_docker_file
    container_name: django_calendar
    volumes:
      - ./eventmaster:/eventmaster
    ports:
      - "8000:8000"
    command: sh -c "python3 manage.py migrate & python3 manage.py runserver 0.0.0.0:8000"
    env_file:
      - db_keys.txt
    depends_on:
      - db
      - cache

  db:
    image: postgres:latest
    container_name: calendar_db
    env_file:
      - db_keys.txt

  adminer:
    image: adminer:latest
    container_name: calendar_adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

  cache:
    image: redis:latest
    container_name: calendar_cache

  celery:
    build:
      context: .
      dockerfile: django_docker_file
    container_name: calendar_celery
    volumes:
      - ./eventmaster:/eventmaster
    env_file:
      - db_keys.txt
    depends_on:
      - db
      - cache
    command: sh -c "celery -A eventmaster worker -l INFO -B"
```
7.Commands:
```
docker-compose build
docker-compose up
```
    



