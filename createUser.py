from django.contrib.auth.models import User
user = User.objects.create_user('admin', 'xiaoxd16@163.com', '12345678')
user.save()