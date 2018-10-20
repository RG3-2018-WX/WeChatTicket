from codex.baseerror import *
from codex.baseview import APIView
from django.utils import timezone
from wechat.models import User,Ticket,Activity
import json
import datetime
import re
class UserBind(APIView):

    def validate_user(self):

        if re.fullmatch(r"[0-9]{10}",self.input['student_id']):
            return
        else:
            raise ValidateError()

    def get(self):
        print("get user bind")
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        print("post user bind")
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()

class ActivityDetail(APIView):
    def get(self):
        self.check_input('id')
        activity=Activity.objects.get(id=self.input['id'])
        if activity.status==1:
            data={'name':activity.name,
                  'key':activity.key,
                  'description':activity.description,
                  'startTime':activity.start_time.timestamp(),
                  'endTime':activity.end_time.timestamp(),
                  'place':activity.place,
                  'bookStart':activity.book_start.timestamp(),
                  'bookEnd':activity.book_end.timestamp(),
                  'totalTicket':activity.total_tickets,
                  'picUrl':activity.pic_url,
                  'remainTicket':activity.remain_tickets,
                  'currentTime':timezone.now().timestamp(),
                  }
            return data
        else:
            raise InputError('Activity is not active')
class TicketDetail(APIView):
    def get(self):
        self.check_input('openid','ticket')
        ticket=Ticket.objects.get(unique_id=self.input['ticket'])
        data={  'activityName':ticket.activity.name,
                'place':ticket.activity.place,
                'activityKey':ticket.activity.key,
                'uniqueId':ticket.unique_id,
                'startTime':ticket.activity.start_time.timestamp(),
                'endTime':ticket.activity.end_time.timestamp(),
                'currentTime':timezone.now().timestamp(),
                'status':ticket.status
                }
        return data
