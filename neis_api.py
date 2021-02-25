import os

import requests

NEIS_KEY = os.environ['NEIS_KEY']  # OS 환경변수에 api 키 등록 필요


def get_sch_info(sch_name):  # 학교 종류, 코드, 교육청 코드를 가져옴
    url = 'https://open.neis.go.kr/hub/schoolInfo'
    params = {
        'Key': NEIS_KEY,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 8,
        'SCHUL_NM': sch_name
    }
    r = requests.get(url, params).json()

    if 'schoolInfo' in r:
        d = dict()
        for sch in r['schoolInfo'][1]['row']:
            d[sch['SCHUL_NM']] = {
                'sch_kind': sch['SCHUL_KND_SC_NM'],
                'sch_code': sch['SD_SCHUL_CODE'],
                'gyc_code': sch['ATPT_OFCDC_SC_CODE']
            }
        return d
    return None


def get_sch_meal(gyc_code, sch_code, meal_date):  # 식단 정보를 가져옴
    url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    params = {
        'Key': NEIS_KEY,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 8,
        'ATPT_OFCDC_SC_CODE': gyc_code,
        'SD_SCHUL_CODE': sch_code,
        'MLSV_YMD': meal_date
    }
    r = requests.get(url, params).json()

    if 'mealServiceDietInfo' in r:
        meal = r[
            'mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        target = ('.', '\'', '`', ',', '*', '#', '-', '<div>', '</div>',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        for c in target:
            meal = meal.replace(c, '')
        meal = meal.replace('<br/>', '\n')
        meal = [line for line in meal.split('\n') if line.strip() != '']
        return meal
    return None


def get_sch_timetable(gyc_code, sch_code, grade, classname, rdate):
    url = 'https://open.neis.go.kr/hub/hisTimetable'
    params = {
        'Key': NEIS_KEY,
        'Type': 'json',
        'pIndex': 1,
        'pSize': 8,
        'ATPT_OFCDC_SC_CODE': gyc_code,
        'SD_SCHUL_CODE': sch_code,
        'GRADE': grade,
        'CLASS_NM': classname,
        'ALL_TI_YMD': rdate
    }
    r = requests.get(url, params).json()

    if 'hisTimetable' in r:
        timetable = list()
        for perio in r['hisTimetable'][1]['row']:
            timetable.append(perio['ITRT_CNTNT'])
        return timetable
    return None


def get_sch_classinfo(gyc_code, sch_code, grade):
    url = 'https://open.neis.go.kr/hub/classInfo'
    params = {
        'Key': NEIS_KEY,
        'Type': 'json',
        'pIndex': 1,
        'ATPT_OFCDC_SC_CODE': gyc_code,
        'SD_SCHUL_CODE': sch_code,
        'GRADE': grade,
    }
    r = requests.get(url, params).json()

    if 'classInfo' in r:
        classset = set()
        for cl in r['classInfo'][1]['row']:
            classset.add(int(cl['CLASS_NM']))
        return sorted(classset)
    return None


# def get_iui_weather():
#     url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst"


# sch = get_sch_info('이의고등학교')['이의고등학교']
# print(get_sch_meal(sch['gyc_code'], sch['sch_code'], '20210105'))
# print(get_sch_timetable(sch['gyc_code'],
#                         sch['sch_code'], '2', '11', '20210107'))
# print(get_sch_classinfo(sch['gyc_code'], sch['sch_code'], '2'))
