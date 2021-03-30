import datetime
import os

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from neis_api import get_sch_info, get_sch_meal, get_sch_timetable, get_sch_classinfo

URL = os.environ['WEBHOOK_URL']
sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7, minute=30)
def send_message():
    KST = datetime.timezone(datetime.timedelta(hours=9))
    NOW = datetime.datetime.now(KST)
    rdate = NOW.strftime('%Y%m%d')
    sch = get_sch_info('이의고등학교')['이의고등학교']
    today_meal = get_sch_meal(sch['gyc_code'], sch['sch_code'], rdate)

    def tt(cn):
        get_sch_timetable(sch['gyc_code'], sch['sch_code'], '3', cn, rdate)
        return tt

    if today_meal or tt('1'):
        params = {
            "username": "모서리봇",
            "avatar_url": "https://www.vmcdn.ca/f/files/via/import/2017/11/23164825_homer-simpson-doughnut.jpg",
            "allowed_mentions": {"parse": ["everyone"]},
            "content": "@everyone",
            "embeds": [
                {
                    "title": f"🌅 {NOW.strftime('%Y년 %m월 %d일')} {'월화수목금토일'[NOW.weekday()]}요일 🌅",
                    "color": 1127128,
                    "description": '***오늘도 좋은 하루 되세요!***',
                    "fields": [],
                    "footer": {
                        "text": "made with ❤️ by moseoridev",
                        "icon_url": "https://avatars.githubusercontent.com/u/29670244?s=460&v=4"
                    },
                }, ]
        }
        if today_meal:
            nf = {
                "name": "🍽️ 오늘의 급식",
                "value": ', '.join(today_meal),
            }
            params['embeds'][0]['fields'].append(nf)

        if tt('1'):
            for cl in get_sch_classinfo(sch['gyc_code'], sch['sch_code'], '3'):
                np = {
                    "name": f'🧑‍🏫 3학년 {cl}반',
                    'value': ', '.join(tt(str(cl)))
                }
                params['embeds'][0]['fields'].append(np)

        r = requests.post(
            URL,
            json=params
        )

        return True

    else:
        return False


sched.start()
