from datetime import datetime

from rest_framework.fields import DateTimeField, DecimalField


class BaseTestCase:

    @staticmethod
    def date_time_str(date_time: datetime) -> str:
        return DateTimeField().to_representation(date_time)

    @staticmethod
    def debt_to_str(debt: DecimalField) -> str:
        return DecimalField(max_digits=8, decimal_places=2).to_representation(debt)
