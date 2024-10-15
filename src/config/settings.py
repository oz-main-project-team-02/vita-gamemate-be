import os
from datetime import timedelta
from pathlib import Path

import pymysql
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-@67tlej#l=ql#!-o0m&9+x%k+nz0e2s-a0+&jdwjmlx1m1@nx%")

DEBUG = True

ALLOWED_HOSTS = ["ec2-43-202-32-218.ap-northeast-2.compute.amazonaws.com", "localhost:5173"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # own
    "users.apps.UsersConfig",
    "wallets.apps.WalletsConfig",
    "reviews.apps.ReviewsConfig",
    "games.apps.GamesConfig",
    "chats.apps.ChatsConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEST_DISCOVER_PATTERN = "test*.py"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False

AUTH_USER_MODEL = "users.User"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

CSRF_TRUSTED_ORIGINS = [
    "https://localhost",  # localhost 추가
    "http://localhost",  # HTTP로도 접근하는 경우
    "https://127.0.0.1",  # 127.0.0.1 추가
    "http://127.0.0.1",  # HTTP 127.0.0.1 추가
    "https://43.202.32.218/",
    "http://43.202.32.218/",
    "http://ec2-43-202-32-218.ap-northeast-2.compute.amazonaws.com",
    "https://ec2-43-202-32-218.ap-northeast-2.compute.amazonaws.com",
]

SERVER_PROTOCOL = "https"
SERVER_DOMAIN = "0.0.0.0:443"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Vita API",
    "DESCRIPTION": '게임 매칭 서비스 "Vita(비타)"의 API 입니다.',
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # "SECURITY_DEFINITIONS": {
    #     "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header", "description": "Bearer token을 입력하세요"}
    # },
    "SECURITY": [
        {
            "name": "Authorization",
            "type": "http",
            "scheme": "Bearer",
            "bearerFormat": "Opaque",
        },
    ],
    # "SWAGGER_UI_SETTINGS": {
    #     "persistAuthorization": True,
    # },  # 인증 정보 유지
    # "SWAGGER_UI_SETTINGS": {
    #     "deepLinking": True,
    #     "persistAuthorization": True,
    #     "displayOperationId": True,
    # },
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest",
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST"),
        "PORT": os.getenv("MYSQL_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6377",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CHARSET": "utf-8",
            "DECODE_RESPONSES": True,
            "PASSWORD": os.getenv("REDIS_PASSWORD"),
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

GOOGLE_CONFIG = {
    # key
    "CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET"),
    # uri
    "PROFILE_URI": "https://www.googleapis.com/oauth2/v3/userinfo",
    "GENDER_URI": "https://www.googleapis.com/oauth2/user",
    "LOGIN_URI": "https://accounts.google.com/o/oauth2/v2/auth",
    "TOKEN_URI": "https://oauth2.googleapis.com/token",
    "REDIRECT_URI": os.getenv("GOOGLE_REDIRECT_URI"),
    "SCOPE": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/user.gender.read",
    # type
    "GRANT_TYPE": "authorization_code",
    "CONTENT_TYPE": "application/x-www-form-urlencoded",
    # host
    "HOST": "oauth2.googleapis.com",
}

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
