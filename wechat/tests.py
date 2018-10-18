import datetime
import json


from django.test import TestCase
from .models import User,Activity,Ticket
from django.test import Client
from userpage.views import *

class WechatTest(TestCase):

    def before_test(self):
        user_to_add = User(open_id = '1',student_id = '2016013237')
        user_to_add.save()

        activity_to_add =  Activity(
        name = '1',
        key='1-key',
        description = 'desc',
        start_time = datetime.datetime.now(),
        end_time = datetime.datetime.now() + datetime.timedelta(hours = 1),
        place = "here",
        book_start = datetime.datetime.now() - datetime.timedelta(days = 1),
        book_end = datetime.datetime.now() - datetime.timedelta(hours = 1),
        total_tickets = 100,
        pic_url = "",
        remain_tickets = 50,
        status = Activity.STATUS_PUBLISHED
        )
        activity_to_add.save()

        ticket_to_add = Ticket(
        student_id = 1,
        unique_id = 1,
        activity = activity_to_add,
        status = 1
        )
        ticket_to_add.save()



    def test_(self):

        self.assertEqual(1,1)
	
	
    def test_user_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/user/bind/',{'openid':'1'})
        json_text = json.loads(d.content)
        self.assertEqual(json_text['data'], '2016013237')

    def test_user_not_exsit(self):
        self.before_test()
        user = User(open_id='2')
        user.save()
        c = Client()
        d = c.post('/api/u/user/bind/', {'openid': '2','student_id':'2016013238','password':"123456"})
        self.assertEqual(d.status_code, 200)

        c = Client()
        d = c.get('/api/u/user/bind/', {'openid': '2'})
        json_text = json.loads(d.content)
        self.assertEqual(json_text['data'], '2016013238')


# Create your tests here.
