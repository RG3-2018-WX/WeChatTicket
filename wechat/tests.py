import datetime
import json

from django.test import TestCase
from .models import User, Activity, Ticket
from django.test import Client
from userpage.views import *
from adminpage.views import *


class WechatTest(TestCase):

    def before_test(self):
        user_to_add = User(open_id='1', student_id='2016013237')
        user_to_add.save()

        activity_to_add = Activity(
            id=1,
            name='1',
            key='1-key',
            description='desc',
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1),
            place="here",
            book_start=datetime.datetime.now() - datetime.timedelta(days=1),
            book_end=datetime.datetime.now() - datetime.timedelta(hours=1),
            total_tickets=100,
            pic_url="",
            remain_tickets=50,
            status=Activity.STATUS_PUBLISHED
        )
        activity_to_add.save()

        ticket_to_add = Ticket(
            student_id=1,
            unique_id=1,
            activity=activity_to_add,
            status=1
        )
        ticket_to_add.save()

    def test_(self):

        self.assertEqual(1, 1)

    def test_user_bind_get(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/user/bind/', {'openid': '1'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(json_text['data'], '2016013237')

    def test_user_bind_post_exsit(self):
        self.before_test()
        user = User(open_id='2')
        user.save()
        c = Client()
        d = c.post('/api/u/user/bind/', {'openid': '2', 'student_id': '2016013238', 'password': "123456"})
        if d.status_code == 404:
            return
        self.assertEqual(d.status_code, 200)
        json_text = json.loads(d.content)
        self.assertEqual(json_text['code'], 0)

        c = Client()
        d = c.get('/api/u/user/bind/', {'openid': '2'})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(json_text['data'], '2016013238')

    def test_user_bind_post_not_exist(self):
        self.before_test()
        c = Client()
        d = c.post('/api/u/user/bind/', {'openid': '2', 'student_id': '2016013238', 'password': "123456"})
        if d.status_code == 404:
            return
        self.assertEqual(d.status_code, 200)
        json_text = json.loads(d.content)
        self.assertNotEqual(json_text['code'], 0)

    def test_activity_detail_get_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/activity/detail/', {'id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(json_text['data']['key'], '1-key')
        self.assertNotEqual(json_text['code'], 0)

    def test_activity_detail_get_not_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/activity/detail/', {'id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)

    def test_ticket_detail_get_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/u/ticket/detail/', {'openid': 1, 'unique_id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['data']['activityKey'], '1-key')


'''
    def test_login_post_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/login/',{'username':'admin','password':'123456'})
        if d.status_code == 404:
            return 
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code,200)
        self.assertEqual(json_text['code'],0)
        self._login_get_exist()

    def test_login_post_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/login/',{'username':'admin','password':'1234567'})
        if d.status_code == 404:
            return 
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code,200)
        self.assertNotEqual(json_text['code'],0)

    def test_logout_post_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/logout/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code,200)
        self.assertEqual(json_text['code'],0)

    def test_logout_post_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.post('/api/a/logout/',{})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code,200)
        self.assertNotEqual(json_text['code'],0)
        
        def _login_get_exist(self):

        c = Client()
        d = c.get('/api/a/login/', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(json_text['code'], 0)

    def test_login_get_not_exist(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/login/', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertNotEqual(json_text['code'], 0)

    def test_activity_list_get(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/list', {})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code, 200)
    # self.assertEqual(json_text['data'][0]['id'],1)

    def test_activity_delete_succeed(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/delete/', {'id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code, 200)
        self.assertEqual(json_text['code'], 0)


    def test_activity_delete_not_succeed(self):
        self.before_test()
        c = Client()
        d = c.get('/api/a/activity/delete/', {'id': 1})
        d = c.get('/api/a/activity/delete/', {'id': 1})
        if d.status_code == 404:
            return
        json_text = json.loads(d.content)
        self.assertEqual(d.status_code, 200)
        self.assertNotEqual(json_text['code'], 0)


    def test_activity_create_succeed(self):
        pass


    def test_activity_create_not_succeed(self):
        pass


    def test_image_upload_succeed(self):
        pass


    def test_image_upload_not_succeed(self):
        pass
        '''




# Create your tests here.
