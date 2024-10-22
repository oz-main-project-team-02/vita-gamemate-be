#!/bin/bash
#DJANGO_APP = "djangoProject"

# 가상 환경 활성화
source ~/.bashrc
pyenv activate django_app

# 작업 디렉토리 이동
cd /app/src

# 데이터베이스 마이그레이션 (SKIP_MIGRATIONS 환경 변수에 따라 실행)
if [ "$SKIP_MIGRATIONS" != "True" ]; then
  poetry run python manage.py migrate --no-input
fi

# 정적 파일 수집
poetry run python manage.py collectstatic --no-input

# 명령행 인자로 전달된 명령 실행
exec "$@"
