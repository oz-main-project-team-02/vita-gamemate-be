### test.sh 파일 실행 방법
``` chmod +x ./scripts/test.sh ``` 

``` ./scripts/test.sh ```

### gitmessage 등록 방법
``` git config --local commit.template .gitmessage.txt ```


### 개발 진행 방법
develop 브랜치에서 -> feature/기능이름 브랜치를 만든 후 이동하여 개발 진행
``` git checkout develop ```

``` git checkout -b feature/user(기능이름) ```

기능 개발 완료 되었다면

``` git push origin feature/user(기능이름) ```

푸쉬이후 깃허브에서 develop 브랜치로 풀리퀘스트 생성


``` 
sudo docker stop $(sudo docker ps -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker pull hwangtate/main-project:v1
```

