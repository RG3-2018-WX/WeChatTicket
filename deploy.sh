cd /home/ubuntu/WeChatTicket
echo "pull code"
git pull origin master
cp configs.example.json configs.json
python deploy.py

echo "start djnago project"
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:80
