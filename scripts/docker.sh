set -eo pipefail

COLOR_GREEN=`tput setaf 2;`
COLOR_NC=`tput sgr0;`

echo "Starting build & push"
docker buildx build --platform linux/amd64 -t hwangtate/main-project:v1 --push .
echo "OK"
echo "${COLOR_GREEN}Image pushed successfully!${COLOR_NC}"