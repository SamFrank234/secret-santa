from django.test import TestCase
from groups.email_pairings import Emailer
from groups.models import Santa, Party
from datetime import datetime



class createPairingsTestCase(TestCase):

    #TESTS
    
    def setUp(self):
        party = Party.objects.create(name="Test", password="irrelevant", join_deadline=datetime(2023, 1, 1), exchange_date = datetime(2023, 2, 2), spending_limit=1)
        Santa.objects.create(first_name="Gmail", last_name="Frank", email_address="samfrank349@gmail.com", party=party)
        Santa.objects.create(first_name="NYU", last_name="Frank", email_address="sff5097@nyu.edu", party=party)
        Santa.objects.create(first_name="Outlook", last_name="Frank", email_address="sam-frank@outlook.com", party=party)
        emailer = Emailer()
        emailer.email_pairings("Test")

    def test_pairings(self):
        party = Party.objects.get(name="Test")
        santa_list = Santa.objects.filter(party=party)
        for santa in santa_list:
            self.assertFalse(santa.recipient==None)