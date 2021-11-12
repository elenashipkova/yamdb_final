import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    if value < 1500 or value > datetime.datetime.now().year:
        raise ValidationError(
            'Год должен быть не меньше 1500 и не больше текущего',
            params={'value': value},
        )
