# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import *

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class HelpOrSubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe') or \
               self.is_event_click(self.view.event_keys['help'])

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('help_title'),
            'Description': self.get_message('help_description'),
            'Url': self.url_help(),
        })


class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or self.is_event('unsubscribe')

    def handle(self):
        self.user.student_id = ''
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))

class GetTicketHandler(WeChatHandler):

    def check(self):
        return self.is_text('查票') or self.is_event_click(self.view.event_keys['get_ticket'])

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('get_ticket'),
            'Description': self.get_message('ticket_description'),
            'Url': self.url_ticket(),
        })

class RobTicket(WeChatHandler):

    def check(self):
        return self.is_text('抢票')

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('book_header'),
            'Description': self.get_message('ticket_description'),
            'Url': self.url_ticket(),
        })

class BookWhatHandler(WeChatHandler):
    def check(self):
        return self.is_text("抢啥") or self.is_event_click(self.view.event_keys['book_what'])
    def handle(self):
        print("book what")
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        activities = Activity.objects.filter(status = Activity.STATUS_PUBLISHED,book_end__gt=timezone.now()).order_by('-book_end')

        if len(activities):
            output = []
            for activity in activities:
                output.append({
                    'Title':activity.name,
                    'Description':activity.description,
                    'PicUrl':activity.pic_url,
                    'Url':self.url_activity(activity.id)
                })
                return self.reply_news(output)
        else:
            return self.reply_text(self.get_message('book_empty'))