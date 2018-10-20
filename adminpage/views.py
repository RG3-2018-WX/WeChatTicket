from django.shortcuts import render
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from wechat.models import Activity,Ticket
global user_status
user_status=0
class Login(APIView):
    global user_status
    def get(self):
        if user_status==1:
            return 0
        else:
            return 1

    def post(self):
        self.check_input('username', 'password')
        user = authenticate(username=self.input['username'], password=self.input['password'])
        if user is not None:
            if user.is_active:
                login(self, user)
                user_status=1
                return 0
            else:
                return 1
        else:
            return 1



class Logout(APIView):
    global user_status
    def post(self):
        if user_status==1:
            logout(self)
            user_status=0
            return 0
        else:
            return 1

class ActivityList(APIView):
    def get(self):
        pass

class ActivityDelete(APIView):
    def post(self):
        pass

class ActivityCreate(APIView):
    def post(self):
        pass

class ActivityUpload(APIView):
    def post(self):
        pass

class ActivityDetail(APIView):
    def get(self):
        pass
    def post(self):
        pass

class ActivityMenu(APIView):
    def get(self):
        pass
    def post(self):
        pass

class ActivityCheckin(APIView):
    def post(self):
        pass
# Create your views here.
