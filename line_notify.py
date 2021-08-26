import requests, datetime

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

from bs4 import BeautifulSoup


'''
This file is used for Project remind
(2021/07/29 Rex Lin)
'''
class Config(object):
    #schedule_job config
    JOBS = [
        {
        'id': 'get_number_of_projects', #identifier
        'func': 'line_notify:get_number_of_projects', #file_name:func_name
        'args': (), #no argument
        'trigger': 'interval', #attribute: interval, cron, date
        'hours': 3, #do the job every 3 hours  #attribute: weeks, days, hours, minutes, seconds
        'next_run_time': datetime.datetime.now() #set this to execute right now
        }
        #you can add more job here
    ]
    SCHEDULER_TIMEZONE = 'Asia/Taipei'  # time zone 
    SCHEDULER_API_ENABLED = True  # enable API if needed

scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Taipei"))

'''
get project numbers from ccm web
'''
def get_number_of_projects():
    url = 'http://127.0.0.1/ccm/connection' #change to your iottalk.tw
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")

    li_all = soup.find_all("li", class_="project-list")
    li_all = li_all[1:] #dicard the first one - Add Project

    project_list = dict()
    for li in li_all:
        project_name = li.select_one("a").get_text()
        p_id = li.select_one("a").get('name')
        project_list[project_name] = p_id

    if len(project_list) > 10:
        line_notify()

'''
send a message to Line Group
'''
def line_notify(): 
    token = '6L3k37MTRh1dUk4OGNJwZ84mBT3riBcA0y3UZ5Nq774'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(token),
        'Connection': 'close'
    }
    payload = {
        'message':'IoTtalk projects of vpython are larger than 10.', 
    }

    res = requests.post('https://notify-api.line.me/api/notify', data = payload, headers = headers)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)  #use_reloader防止flask重複執行job，而造成送兩次request