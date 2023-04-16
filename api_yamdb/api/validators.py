import datetime as dt
import re

from django.core.exceptions import ValidationError

from api_yamdb.settings import RESERVED_USERNAMES, VALID_USERNAME


def validate_username(username):
    if username.lower() in RESERVED_USERNAMES:
        raise ValidationError(f'Имя пользователя не может быть {username}.')
    if not re.search(VALID_USERNAME, username):
        unmatched = re.sub(VALID_USERNAME, '', str(username))
        raise ValidationError(f'Обнаружены недопустимые символы: {unmatched}!')


def validate_year(value):
    current_year = dt.date.today().year
    if value > current_year:
        raise ValidationError('Check year value.')
    return value
