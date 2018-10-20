from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from wechat.models import Activity, Ticket
import json
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

        list = Activity.objects.filter(status=[0,1])
        datalist=[]
        for data in list:
            data_result = {'name': data.name,
                    'id': data.id,
                    'description': data.description,
                    'startTime': data.start_time,
                    'endTime': data.end_time,
                    'place': data.place,
                    'bookStart': data.book_start,
                    'bookEnd': data.book_end,
                    'status':data.status,
                    'currentTime': datetime.datetime.now()
                    }
            data_result=json.dumps(data_result)
            datalist.append(data_result)
        return datalist



class ActivityDelete(APIView):
    def post(self):
        self.check_input('id')
        if Activity.objects.get(id=self.input('id')):
            Activity.objects.get(id=self.input('id')).delete()
            return 0
        else:
            raise LogicError()


class ActivityCreate(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        obj=Activity( name = self.input['name'],
                    key = self.input['key'],
                    description = self.input['description'],
                    start_time = self.input['startTime'],
                    end_time = self.input['endTime'],
                    place = self.input['palce'],
                    book_start = self.input['bookStart'],
                    book_end = self.input['bookEnd'],
                    total_tickets = self.input['totalTickets'],
                    status = self.input['status'],
                    )
        obj.save()
        if Activity.objects.get(self.input['name']):
            return obj.id
        else:
            raise LogicError()


class ImageUpload(APIView):
    def post(self):
        pass


class ActivityDetail(APIView):
    def get(self):
        self.check_input('id')
        activity = Activity.objects.get(id=self.input('id'))
        if activity:
            data = {'name': activity.name,
                    'key': activity.key,
                    'description': activity.description,
                    'startTime': activity.start_time,
                    'endTime': activity.end_time,
                    'place': activity.place,
                    'bookStart': activity.book_start,
                    'bookEnd': activity.book_end,
                    'totalTicket': activity.total_tickets,
                    'picUrl': activity.pic_url,
                    'remainTicket': activity.remain_tickets,
                    'usedTicket':0,
                    'currentTime': datetime.datetime.now()
                    }
            data = json.dumps(data)
            return data
        else:
            raise InputError()



    def post(self):

        self.check_input('id')
        activity = Activity.objects.get(id=self.input('id'))
        old_activity=activity
        if activity.status==0:
            activity.name=self.input('name')
            activity.place=self.input('place')
            activity.book_end=self.input('bookEnd')
            activity.book_start=self.input('bookStart')
            activity.status=self.input('status')

        activity.pic_url=self.input('picURL')
        activity.description=self.input('description')
        if datetime.datetime.now()<activity.end_time:
            activity.start_time=self.input('startTime')
            activity.end_time = self.input('endTime')
        if datetime.datetime.now()<activity.book_start:
            activity.total_tickets=self.input('totalTicket')
        activity.save()
        if old_activity==activity:
            raise InputError()
        else:
            return 0
class ActivityMenu(APIView):
    i=0
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")

        list = Activity.objects.filter(status=1)
        datalist=[]
        for data in list:

            data_result = {'name': data.name,
                    'id': data.id,
                    'menuIndex':ActivityMenu.i
                    }
            ActivityMenu.i=ActivityMenu.i+1
            data_result=json.dumps(data_result)
            datalist.append(data_result)
        return datalist

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        activity=Activity.objects.get(self.input('id'))
        pass



class ActivityCheckin(APIView):
    def post(self):
        pass

# Create your views here.
