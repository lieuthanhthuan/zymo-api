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
docker-compose up -d --build

```
---
API Service will be served at http://localhost:3001/

---
## Testing

```bash
docker-compose run web python manage.py test
```
