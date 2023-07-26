# Lab 32: Lab: Permissions & Postgresql

Author: **Almothana Almasri**

## Overview

Let’s move our site closer to production grade by adding Permissions and Postgresql Database.

## RUN

```bash
docker-compose up 
```

`CTRL +C` to quit

## Configuration

```bash
docker-compose run web python manage.py createsuperuser
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate  
docker-compose run web python manage.py test
```