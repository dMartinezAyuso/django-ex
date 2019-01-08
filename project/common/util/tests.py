from datetime import date
from django.test import TestCase
from .helper import DateHelper

class DateHelperTests(TestCase):

    def setUp(self):
        self.sample_dates = {
            'older_date': '2010-05-24',
            'init_date': '2015-05-24',
            'newest_date': '2020-05-24'
        }
        self.dh = DateHelper(self.sample_dates['init_date'])

    def test_is_after_than(self):
        self.assertTrue(self.dh.isAfterThan(self.sample_dates['older_date']))
        self.assertFalse(self.dh.isAfterThan(self.sample_dates['newest_date']))

    def test_is_after_than_today(self):
        self.assertFalse(self.dh.isAfterThanToday())

    def test_is_before_than(self):
        self.assertFalse(self.dh.isBeforeThan(self.sample_dates['older_date']))
        self.assertTrue(self.dh.isBeforeThan(self.sample_dates['newest_date']))

    def test_is_before_than_today(self):
        self.assertTrue(self.dh.isBeforeThanToday())