import redis
import time
import jwt

import datetime

from django.conf import settings

from .models import User

ACTIVITY_DB = 1


def get_activity(key, db_number=ACTIVITY_DB):
    db = redis.Redis(host='localhost', port=6379, db=db_number)
    return datetime.datetime.fromtimestamp(float(db.get(key).decode('utf-8')))


def set_activity(key, db_number=ACTIVITY_DB):
    db = redis.Redis(host='localhost', port=6379, db=db_number)
    db.set(key, time.time())
    db.set_response_callback('GET', float)


def get_user_by_jwt(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256', )
        return User.objects.get(id=decoded.get('user_id'))
    except:
        pass


def check_and_convert_date_to_object(date_from):
    if date_from:
        return datetime.datetime.strptime(date_from, '%Y-%m-%d').date()


def get_like_stats_by_days(date_from, date_to, likes):
    response = {}
    while date_from <= date_to:
        response[str(date_from)] = likes.filter(date_created__date=date_from).count()
        date_from += datetime.timedelta(days=1)
    return response