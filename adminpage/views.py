from django.shortcuts import render
from codex.baseview import APIView

from wechat.models import User,Activity,Ticket

class Login(APIView):
    def get(self):
        pass
    def post(self):
        pass

class Logout(APIView):
    def post(self):
        pass

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
