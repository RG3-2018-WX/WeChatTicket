cd /home/ubuntu/WeChatTicket
echo "pull code"
git pull origin master
cp configs.example.json configs.json
sudo python3 deploy.py

echo "start djnago project"
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo nohup python3 manage.py runserver 0.0.0.0:80
