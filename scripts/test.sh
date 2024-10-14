#!/usr/bin/env bash
# 오른쪽 명령어를 터미널에 입력해주세요 -> chmod +x scripts/test.sh
set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;`

echo "Starting black"
poetry run black .
echo "${COLOR_GREEN}OK${COLOR_NC}"

echo "Starting isort"
poetry run isort .
echo "${COLOR_GREEN}OK${COLOR_NC}"

echo "Starting test with coverage"
poetry run coverage run src/manage.py test
poetry run coverage report -m

echo "${COLOR_GREEN}All tests passed successfully!${COLOR_NC}"