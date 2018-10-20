from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from wechat.models import Activity,Ticket

class Login(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login!")

    def post(self):
        self.check_input('username', 'password')
        user = authenticate(username=self.input['username'], password=self.input['password'])
        if user is not None:
            if user.is_active:
                login(self, user)




class Logout(APIView):
    def post(self):
        logout(self)

class ActivityList(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise  ValidateError("Please Login First!")
        self.check_input('id')

        list = Activity.get_status_ge_0()


class ActivityDelete(APIView):
    def post(self):
        pass

class ActivityCreate(APIView):
    def post(self):
        pass

class ImageUpload(APIView):
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
