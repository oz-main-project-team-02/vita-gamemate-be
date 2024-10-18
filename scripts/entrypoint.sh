#!/bin/bash
#DJANGO_APP = "djangoProject"

# 가상 환경 활성화
source ~/.bashrc
pyenv activate django_app

cd src

## 데이터베이스 마이그레이션
poetry run python manage.py migrate --no-input
poetry run python manage.py collectstatic --no-input

nginx

# Gunicorn 실행
exec poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000
