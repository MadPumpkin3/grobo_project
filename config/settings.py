"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "myapps/templates"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-()7xt93075zpr$2lewb39648%p^mo-&xsf+!u932rf7sg!$zx)'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Local apps
    'myapps.users',
    'myapps.posts',
    'myapps.feeds',
    'myapps.ai_data',
    'myapps.common',
    
    # Third party apps
    'django_extensions',
    'django_apscheduler',
    
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'grobo_db', # 데이터베이스명
        'USER': 'grobo',
        'PASSWORD': 'Fpdjxpa37!',
        # 유동ip라서 주기적으로 수정 필요(나중에 고정 ip 삽입)
        'HOST': '52.78.69.215',
        'PORT': '3306',
        # mysql과 DBeaver 연결시 필수 사항 > 서버의 /etc/mysql/mysql.conf.d/mysqld.cnf 파일에서 port 활성화 및 port = 3306, 
        # bind-address = 0.0.0.0 으로 외부 ip에서도 접속 가능하도록 수정
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myapps/static'),
]
# 디렉터리 위치를 리스트 형태로 감싸면, 나중에 추가적인 디렉터리 위치를 넣을 수 있다.

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'myapps/media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# 사용자 정의 인증이 필요할 때, 사용자 정의 인증 백엔드를 만들고 아래에 추가하면 된다.
# 현재 있는 것은 기본 사용자 정의 백엔드이다.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# 스케줄러 기본 설정(스케줄러 사용 보류 - 사유: 불필요한 리소스 사용량 증가 고려)
# 스케줄러 런타임 타임스탬프 표시를 위한 형식 문자열
# APSCHEDULER_DATETIME_FORMAT  =  "N j, Y, f:s a"

# 스케줄러 작동시 작업 시간이 오래 걸리면 자동으로 멈추는 설정(최대 실행 시간)
# APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# apscheduler를 스케줄러 인스턴스의 기본으로 사용한다는 설정
# SCHEDULER_DEFAULT = True