from django.test import TestCase
import datetime
from .models import User,Activity,Ticket


class WechatTest(TestCase):

    user_to_add = User(open_id = 1,student_id = 1)
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
        self.assertEqual(1, 1)

    def test_user_not_exsit(self):
        self.assertEqual(1, 1)




# Create your tests here.
