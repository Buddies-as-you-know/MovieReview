
# MovieReview
qiitaに乗せました！！！
https://qiita.com/RyeWiskey/items/29858102806635bb2691

# ローカルでの環境構築方法
個人のSECRET_KEY(MovieReview/local_setting.py)とTMDBのAPIKEYを取得してください.
## requirement.txtで必要なライブラリをダウンロードしてください
```
pip install -r requirements.txt
```
## local環境に設定してください
settings.pyの
```
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}
"""
を
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
```
に変更する。
そして、
```
python manage.py runserver
```
# herokuにデプロイもしています！！！

https://filmer-000.herokuapp.com/


![Animat](https://user-images.githubusercontent.com/69001166/180608078-00dd70de-ab05-45fb-a201-e0556465cc0c.gif)

# 要件設定

[Film_Reviews).pdf](https://github.com/YuminosukeSato/MovieReview/files/9331008/Film_Reviews.pdf)

# 使用技術
python Django 
html
css(bootstrap)
javascript
