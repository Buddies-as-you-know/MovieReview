import os

# settings.pyからそのままコピー
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "django-insecure-g1wl1jobb0c%x)=(%%!*5u5t-#4c%yyy*j+^w5a7c$*r-y#tqc"
# settings.pyからそのままコピー
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

DEBUG = True  # ローカルでDebugできるようになります
