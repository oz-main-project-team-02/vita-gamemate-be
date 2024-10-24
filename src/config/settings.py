import os
from datetime import timedelta
from pathlib import Path

import pymysql
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-@67tlej#l=ql#!-o0m&9+x%k+nz0e2s-a0+&jdwjmlx1m1@nx%")
DEBUG = True

# ALLOWED_HOSTS = [
#     "resdineconsulting.com",
#     "localhost",
#     "localhost:5173",
#     "127.0.0.1:5173",
#     "127.0.0.1",
# ]

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third
    "corsheaders",
    "channels",
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "storages",
    "django_extensions",
    # own
    "users.apps.UsersConfig",
    "wallets.apps.WalletsConfig",
    "reviews.apps.ReviewsConfig",
    "games.apps.GamesConfig",
    "chats.apps.ChatsConfig",
    "mates.apps.MatesConfig",
    "game_requests.apps.GameRequestsConfig",
    "payments.apps.PaymentsConfig",
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
ASGI_APPLICATION = "config.asgi.application"

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  # 쿠키 등 credential 정보 허용
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "cache-control",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "refresh_token",
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = [
    "https://localhost",  # localhost 추가
    "http://localhost",  # HTTP로도 접근하는 경우
    "https://127.0.0.1",  # 127.0.0.1 추가
    "http://127.0.0.1",  # HTTP 127.0.0.1 추가
    "https://43.202.32.218/",
    "http://43.202.32.218/",
    "http://resdineconsulting.com",
    "https://resdineconsulting.com",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

JWT_ACCESS_TOKEN_EXPIRE = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRE = timedelta(days=7)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": JWT_ACCESS_TOKEN_EXPIRE,
    "REFRESH_TOKEN_LIFETIME": JWT_REFRESH_TOKEN_EXPIRE,
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
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("RDS_HOSTNAME"),
        "NAME": os.environ.get("RDS_DB_NAME"),
        "USER": os.environ.get("RDS_USERNAME"),
        "PASSWORD": os.environ.get("RDS_PASSWORD"),
        "PORT": os.environ.get("RDS_PORT", 5432),
        "OPTIONS": {
            "client_encoding": "UTF8",  # UTF-8 문자셋 설정
        },
        "TEST": {
            "NAME": "test_postgres_new",
        },
    }
}

REDIS_HOST = os.environ.get("REDIS_HOST", "0.0.0.0")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://:{os.environ.get('REDIS_PASSWORD', '')}@redis:6379/0"],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {"level": "ERROR", "filters": ["require_debug_false"], "class": "django.utils.log.AdminEmailHandler"},
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
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

KAKAO_CONFIG = {
    # key
    "REST_API_KEY": os.getenv("KAKAO_REST_API_KEY"),
    "CLIENT_SECRET_KEY": os.getenv("KAKAO_CLIENT_SECRET_KEY"),
    # uri
    "LOGIN_URI": "https://kauth.kakao.com/oauth/authorize",
    "TOKEN_URI": "https://kauth.kakao.com/oauth/token",
    "PROFILE_URI": "https://kapi.kakao.com/v2/user/me",
    "REDIRECT_URI": os.getenv("KAKAO_REDIRECT_URI"),
    # type
    "GRANT_TYPE": "authorization_code",
    "CONTENT_TYPE": "application/x-www-form-urlencoded;charset=utf-8",
}

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_LOCATION = "static"

# S3에 정적 파일을 저장하도록 설정
STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}/{AWS_LOCATION}/"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
