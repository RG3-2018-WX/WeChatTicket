import json
f = open('configs.json')
json_text = json.load(f,'rw')
json_text['DEBUG'] = False
json_text['IGNORE_WECHAT_SIGNATURE']=True
json_text['WECHAT_TOKEN'] = 'ThisIsAWeChatToken'
json_text['WECHAT_APPID']='wx00c7dcf61bfa893c'
json_text['WECHAT_SECRET']='a52f865317099c91816ad7e778281543'
json_text[DB_PASS'']='123456'
json_text['SITE_DOMAIN'] = 'http://668855.iterator-traits.com/'；
json_text.dump(f)
