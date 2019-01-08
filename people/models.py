from django.db import models
from my_innerapps_api.common.util.helper import DateHelper


class People(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    code = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def clean(self):
        from .serializers import validate_start_and_end_dates
        if self.end_date:
            validate_start_and_end_dates(self.start_date, self.end_date, validation_type='model')


    def save(self, *args, **kwargs):

        self.is_active = True

        if self.end_date:
            dh_end_date = DateHelper(self.end_date)

            if dh_end_date.isBeforeThanToday():
                self.is_active = False

        if self.start_date and self.is_active:
            dh_start_date = DateHelper(self.start_date)
            if dh_start_date.isAfterThanToday():
                self.is_active = False

        super(People, self).save(*args, **kwargs)

