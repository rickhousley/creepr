""" Test happn module """

import happn
import json
import pprint

token = 'CAAGm0PX4ZCpsBAEZCnObazwW05uWsgL1AduIn4KzdQcsuqfqVrcYb46MBsgZBgiVlqbRFdVe8IyFwGE1FleX5ue7tyRZBm1bp70O3lPjrPYcFosPmAzeEmY4sjDIQzShGvlUTpuiU0IZBrVjP5TKZAgwHZAnkDTs8L8HurFRKDWybXmZAhOtGE7Sn5L7htdnxnrRty3KZC4DGkl6PTJLangDR1HRjzFGVCqcZD'
user = happn.User(token)

settings = {
	"age": 83, 
    "birth_date": "1922-01-01T00:00:00-0500", 
    "credits": 40, 
    "display_name": "ThroatpipeJackson", 
    "first_name": "ThroatpipeJackson", 
    "fb_id" : 1346023834
}
test = 	user.set_settings(settings)

