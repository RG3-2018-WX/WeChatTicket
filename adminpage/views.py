from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from wechat.models import Activity, Ticket


from wechat import models
from wechat.models import Activity, Ticket
from django.utils import timezone
from wechat.views import CustomWeChatView
import uuid
from WeChatTicket import settings
import os

class Login(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login!")


    def post(self):
        self.check_input('username', 'password')
        user = authenticate(username=self.input['username'], password=self.input['password'])
        if user is not None and user.is_active:
             login(self.request, user)
             return
        if not User.objects.filter(username=self.input['username']):
            raise  ValidateError("Username not exist")
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

        list =Activity.objects.filter(status=[0,1])
        
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
			'currentTime':timezone.now().timestamp(),
            'status':i.status
			})
        return output_list


class ActivityDelete(APIView):
    def post(self):
        self.check_input('id')
        if Activity.objects.get(id=self.input['id']):
            activity=Activity.objects.get(id=self.input['id'])
            activity.status=Activity.STATUS_DELETED

        else:
            raise LogicError()



class ActivityCreate(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")
        self.check_input("name", "key", "place", "description", "picUrl", "startTime",
                         "endTime", "bookStart", "bookEnd", "totalTickets", "status")
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
                    remain_tickets=self.input['totalTickets'],
                    )
        obj.save()
        if not Activity.objects.get(self.input['name']):
            raise LogicError()


class ImageUpload(APIView):

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input("image")
        try:
            image = self.input["image"][0]
            name = str(uuid.uuid1()) + image.name
            file = open('./static/uimg/' + name, 'wb')
            for chunk in image.chunks():
                file.write(chunk)
            file.close()
            path = 'uimg/' + name
            url = os.path.join(settings.CONFIGS["SITE_DOMAIN"], path)
            return url
        except:
            raise ValidateError()


class ActivityDetail(APIView):
    def get(self):
        self.check_input('id')
        activity = Activity.objects.get(id=self.input('id'))
        if activity:
            data = {'name': activity.name,
                    'key': activity.key,
                    'description': activity.description,
                    'startTime': activity.start_time.timestamp(),
                    'endTime': activity.end_time.timestamp(),
                    'place': activity.place,
                    'bookStart': activity.book_start.timestamp(),
                    'bookEnd': activity.book_end.timestamp(),
                    'totalTicket': activity.total_tickets,
                    'picUrl': activity.pic_url,
                    'remainTicket': activity.remain_tickets,
                    'usedTicket':activity.total_tickets-activity.remain_tickets,
                    'currentTime': timezone.now().timestamp()
                    }
            
            return data
        else:
            raise InputError()



    def post(self):

        self.check_input('id')
        activity = Activity.objects.get(id=self.input['id'])
        old_activity=activity
        if activity.status==0:
            activity.name=self.input['name']
            activity.place=self.input['place']
            activity.book_end=self.input['bookEnd']
            activity.book_start=self.input['bookStart']
            activity.status=self.input['status']

        activity.pic_url=self.input['picURL']
        activity.description=self.input['description']
        if timezone.now()<activity.end_time:
            activity.start_time=self.input['startTime']
            activity.end_time = self.input['endTime']
        if timezone.now()<activity.book_start:
            activity.total_tickets=self.input['totalTicket']
        activity.save()
        if old_activity==activity:
            raise InputError()
        else:
            return 0
class ActivityMenu(APIView):

    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please Login First!")

        list = Activity.objects.filter(status=1)
        datalist=[]
        for data in list:

            data_result = {'name': data.name,
                    'id': data.id,
                    'menuIndex':0
                    }

            data_result=json.dumps(data_result)
            datalist.append(data_result)
        datalist.reverse()
        if len(datalist) < 5:
            for i in range(0, len(datalist)):
                datalist[i]["menuIndex"] = 5 - i
        else:
            for i in range(0, len(datalist)):
                datalist[i]["menuIndex"] = max(5 - i, 0)
        return datalist



    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        idList = self.input
        for data in Activity.objects.filter(status=Activity.STATUS_PUBLISHED):
            data.status = 0
        activityList = []
        for id in idList:
            try:
                activity = Activity.objects.get(id=id)
                activity.status = 1
                activity.save()
                activityList.append(activity)
            except:
                raise ValidateError("no such activity")
        CustomWeChatView.update_menu(activityList)


class ActivityCheckin(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")
        self.check_input('actId')
        studentId = self.input.get['studentId']
        uniqueId = self.input.get['ticket']
        if studentId == None and uniqueId == None:
            raise ValidateError('info loss')
        if studentId != None and uniqueId != None:
            raise ValidateError()
        ticket = None
        try:
            if studentId != None:
                ticket = Ticket.objects.get(studentId=studentId)
            else:
                ticket = Ticket.objects.get(unique_id=uniqueId)
        except:
            raise ValidateError('invalid Ticket')
        if ticket.status == Ticket.STATUS_USED:
            raise ValidateError('ticket Used!')
        if ticket.status == Ticket.STATUS_CANCELLED:
            raise ValidateError('ticket Canceled!')
        ticket.status = Ticket.STATUS_USED
        ticket.save()
        data = {'ticket': ticket.unique_id, 'studentId': ticket.student_id}
        return data

# Create your views here.
