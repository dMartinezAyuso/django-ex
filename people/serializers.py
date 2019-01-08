from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import People
from my_innerapps_api.common.util.helper import DateHelper

def validate_start_and_end_dates(start_date, end_date, validation_type='serializer'):
    message = "Start date cannot precede end date"
    dh_end_date = DateHelper(end_date)
    if dh_end_date.isBeforeThan(start_date):
        if validation_type == 'model':
            raise ValidationError(message)
        else:
            raise serializers.ValidationError(message)


class PeopleSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if 'end_date' in data:
            validate_start_and_end_dates(data['start_date'], data['end_date'])
        return data

    class Meta:
        fields = ('id', 'name', 'surname', 'code', 'start_date', 'end_date', 'is_active')
        model = People