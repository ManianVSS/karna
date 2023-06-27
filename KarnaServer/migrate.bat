python manage.py makemigrations api
python manage.py migrate

python manage.py shell -c "from create_super_user import create_super_user; create_super_user()"
