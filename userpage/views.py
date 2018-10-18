from codex.baseerror import *
from codex.baseview import APIView
import re
from wechat.models import User,Ticket,Activity


class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed

        """
        if re.fullmatch(r"[0-9]{10}",self.input['student_id']) is None:
            raise ValidateError("Student Id not legal.")
        raise NotImplementedError('You should implement UserBind.validate_user method')

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
        pass

class TicketDetail(APIView):
    def get(self):
        pass
