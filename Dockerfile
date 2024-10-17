# 1. 기본 Python 이미지를 지정합니다.
FROM python:3.12-slim
# Python 3.12 환경을 기반으로 컨테이너를 만들기 위해서
# slim 태그로 더 작은 이미지를 사용하여 성능과 효율성을 높이기 위한 선택

# 2. 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    pkg-config \
    nano \
    lsof \
    nginx \
    certbot \
    && rm -rf /var/lib/apt/lists/*

# 3. pyenv 설치 및 환경 설정
RUN curl https://pyenv.run | bash
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
RUN rm -rf ~/.pyenv/plugins/pyenv-virtualenv && git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# 4. Python 버전 설치 및 가상 환경 생성
RUN /bin/bash -c "source ~/.bashrc && pyenv install 3.12.1"
RUN /bin/bash -c "source ~/.bashrc && pyenv virtualenv 3.12.1 django_app"
# 매번 가상 환경을 수동으로 활성화하지 않고도, 해당 환경에서 작업할 수 있게 설정됨
RUN echo 'pyenv activate django_app' >> ~/.bashrc

# 5. Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# 6. 프로젝트 파일 복사 및 의존성 설치
WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
RUN /bin/bash -c "source ~/.bashrc && pyenv activate django_app && poetry install --no-root"

# 7. 프로젝트 소스 코드 복사
COPY . /app

# 8. ENTRYPOINT 설정
COPY scripts/entrypoint.sh /app/entrypoint.sh
COPY resources/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY resources/cert/fullchain.pem /etc/letsencrypt/live/resdineconsulting.com/fullchain.pem
COPY resources/cert/privkey.pem /etc/letsencrypt/live/resdineconsulting.com/privkey.pem

RUN chmod +x /app/entrypoint.sh
CMD ["/bin/bash", "/app/scripts/entrypoint.sh"]

#RUN chmod +x /app/scripts/certbot.sh

# 9. Gunicorn이 8000 포트에서 수신하도록 EXPOSE
EXPOSE 8000