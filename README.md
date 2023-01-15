# Installation

## Getting Started the first thing to do is to clone the repository:

```bash
$ git clone https://github.com/dejetem/fast.git
$ cd fast
```

## .env

```bash
$ create .env file and add
$ DATABASE_URL
$ DB_USER
$ DB_PASSWORD
$ DB_NAME
$ PGADMIN_EMAIL
$ PGADMIN_PASSWORD
```

## start docker

```bash
$ docker-compose build 
$ docker-compose up
```

## run Migration

```bash
$ docker-compose run app alembic revision --autogenerate -m "Migration"
$ docker-compose run app alembic upgrade head
```

## Open your a tab on your browser and input this url 
```bash
$ http://127.0.0.1:8000/ - base url
$ http://localhost:8000/docs - swagger documentation
$ http://localhost:8000/redoc - redoc documentation
```

## sample for creating a product
``` json
{
  "name": "string",
  "sku": "string",
  "category": "string",
  "price": {
   "original": 50000,
   "discount_percentage": "30%",
   "currency": "USD"
  }
}
```
