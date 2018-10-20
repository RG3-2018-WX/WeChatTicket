from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from wechat.models import Activity, Ticket


import datetime

class Login(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            print("Error Raised")
            raise ValidateError("Please Login!")
        return 0

    def post(self):

        self.check_input('username', 'password')
        user = authenticate(username=self.input['username'], password=self.input['password'])
        if user is not None and user.is_active:
             login(self.request, user)
             return 0

        else:
            raise ValidateError("wrong password")


class Logout(APIView):

    def post(self):
        if not self.request.user.is_authenticated():
            raise LogicError('no user is online')
        else:
            logout(self.request)


class ActivityList(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input('id')

        list = Activity.get_status_ge_0()
        
        output_list = []
        for i in list:
			output_list.append({
			'id':i.id,
			'name':i.name,
			'description':i.description,
			'startTime':i.start_time.timestamp(),
			'endTime':i.end_time.timestamp(),
			'place':i.place,
			'bookStart':i.book_start.timestamp(),
			'bookEnd':i.book_end.timestamp(),
			'currentTime':datetime.datetime.now().timestamp()
			
			})
        



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
