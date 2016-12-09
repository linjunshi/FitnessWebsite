#!/usr/bin/sh

echo "drop database cs4920;" | mysql -uroot
echo "create database cs4920;" | mysql -uroot
rm -rf fitness/migrations
python manage.py makemigrations fitness
python manage.py migrate
python manage.py shell < insert_data/insert_users.py
python manage.py shell < insert_data/insert_cate.py
