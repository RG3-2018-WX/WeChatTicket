from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import User,Ticket,Activity
import json
import datetime

class UserBind(APIView):

    def validate_user(self):
        self.check_input('student_id','password')
        user=User.objects.get(student_id=self.input['student_id'])
        if user.password==self.input['password']:
           
        else:
            raise ValidateError()

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()

class ActivityDetail(APIView):
    def get(self):
        self.check_input('id')
        activity=Activity.objects.get(key=self.input('id'))
        if activity.status==1:
            data={'name':activity.name,
                  'key':activity.key,
                  'description':activity.description,
                  'startTime':activity.start_time,
                  'endTime':activity.end_time,
                  'place':activity.place,
                  'bookStart':activity.book_start,
                  'bookEnd':activity.book_end,
                  'totalTicket':activity.total_tickets,
                  'picUrl':activity.pic_url,
                  'remainTicket':activity.remain_tickets,
                  'currentTime':datetime.datetime.now()
                  }
            data=json.dumps(data)
            return data
        else:
            raise InputError('Activity is not active')
class TicketDetail(APIView):
    def get(self):
        self.check_input('openid','ticket')
        ticket=Ticket.objects.get(unique_id=self.input('ticket'))
        data={  'activityName':ticket.activity.name,
                'place':ticket.activity.place,
                'activityKey':ticket.activity.key,
                'uniqueId':ticket.unique_id,
                'startTime':ticket.activity.start_time,
                'endTime':ticket.activity.end_time,
                'currentTime':datetime.datetime.now(),
                'status':ticket.status
                }
        data=json.dumps(data)
        return data
