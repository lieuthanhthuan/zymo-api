# zymo-api
COVID-19 Backend REST API Project

## Requirements

Your computer must installed docker and docker-compose

## Installation

Clone this repository into your project:

```bash
git clone https://github.com/lieuthanhthuan/zymo-api.git
```

Build docker images and run containers:

```bash
cd zymo-api
sudo docker-compose up -d --build


```

Create a new postgres database:

```bash
# list all containers and get the containder id of postgres image
docker ps
docker exec -it {docker-container} bash
su postgres
psql postgres
create database zymo;
```

Migrate database and create a new superuser:
```bash
sudo docker-compose run web python manage.py makemigrations
sudo docker-compose run web python manage.py migrate
sudo docker-compose run web python manage.py createsuperuser --username admin

```

Import examples data:
```bash

docker-compose run web python manage.py shell < import_data.py

```

Go to http://localhost:3001/
