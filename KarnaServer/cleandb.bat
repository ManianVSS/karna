del /s /q api\migrations
del /s /q data\db.sqlite3
migrate.bat
python manage.py createsuperuser
