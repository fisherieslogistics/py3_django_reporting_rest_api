from django.test.testcases import TestCase
from reporting.models import Organisation, User, Port, Vessel, Species


class CatchHubTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super(CatchHubTestCase, cls).setUpTestData()

        cls.org = Organisation(fullName="Test inc.")
        cls.org.save()

        cls.user = User(username="test_dummy", organisation=cls.org)
        cls.user.save()

        cls.port = Port(name="Porter Port", organisation=cls.org)
        cls.port.save()

        cls.vessel = Vessel(name="Boaty Mc Boatface", registration=123, organisation=cls.org)
        cls.vessel.save()

        Species.objects.create(code="XXX")
