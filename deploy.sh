cd /home/ubuntu/WeChatTicket
echo "pull code"
git pull origin master
cp configs.example.json configs.json
python3 deploy.py

echo "start djnago project"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80
