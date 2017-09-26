from couchpost.models import PendingDocument
from couchpost.document_importer import CouchDBDocumentImporter, Status
from reporting.models import Trip, FishingEvent, NonFishingEvent, FishCatch,\
    VesselLocation
from fishserve.models import FishServeEvents
import uuid
from django.utils import timezone
from couchpost.tests.testcase import CatchHubTestCase


class TestDocumentImporter(CatchHubTestCase):

    def test_fishserve(self):
        d = PendingDocument(user=self.user,
                            doc={"document_type": "fishserveEvent",
                                 "event_type": "tripStart",
                                 "json": "{fishserve: 'sucks'}",
                                 "headers": {"fish": "head"}})

        model = CouchDBDocumentImporter().process_document(d)

        self.assertIsInstance(model, FishServeEvents)
        self.assertEqual(model.creator.id, self.user.id)
        self.assertEqual(model.event_type, "tripStart")
        self.assertEqual(model.json, d.doc["json"])
        self.assertEqual(model.headers, d.doc["headers"])

    def _get_trip(self):
        return {"id": str(uuid.uuid4()),
                "organisation_id": str(self.org.id),
                "RAId": "Raiden",
                "personInCharge": "Raiden",
                "startTime": timezone.now().isoformat(),
                "endTime": timezone.now().isoformat(),
                "ETA": timezone.now().isoformat(),
                "startLocation": "POINT(45 45)",
                "unloadPort_id": str(self.port.id),
                "vessel_id": str(self.vessel.id)}

    def test_trip(self):
        trip = self._get_trip()
        trip["document_type"] = "trip"

        pd = PendingDocument(user=self.user, doc=dict(trip))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, Trip)
        self.assertEqual(model.creator.id, self.user.id)
        self.assertEqual(model.organisation_id, str(self.org.id))
        self.assertEqual(model.RAId, "Raiden")
        self.assertEqual(model.startTime, trip["startTime"])
        self.assertEqual(model.startLocation.coords, (45.0, 45.0))

        trip['organisation_id'] = str(uuid.uuid4())  # non-existent org
        pd = PendingDocument(user=self.user, doc=dict(trip))
        model = CouchDBDocumentImporter().process_document(pd)
        self.assertIsNone(model)
        self.assertEqual(pd.process_status, Status.ERROR.value)
        self.assertIn("Organisation ID", pd.details)

    def _get_fishevent(self, trip):
        return {"id": str(uuid.uuid4()),
                "RAId": "Raiden",
                "targetSpecies_id": "XXX",
                "vesselNumber": "123",
                "trip_id": str(trip.id),
                "eventSpecificDetails": {"sun": "shining"}}

    def test_fishingevent(self):
        trip = Trip.objects.create(creator=self.user, **self._get_trip())
        event = self._get_fishevent(trip)
        event["document_type"] = "fishingEvent"

        pd = PendingDocument(user=self.user, doc=dict(event))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, FishingEvent)
        self.assertEqual(model.creator.id, self.user.id)
        self.assertEqual(model.eventSpecificDetails, event["eventSpecificDetails"])

    def test_fishcatch(self):
        trip = Trip.objects.create(creator=self.user, **self._get_trip())
        event = FishingEvent.objects.create(creator=self.user, **self._get_fishevent(trip))

        catch = {"document_type": "fishCatch",
                 "fishingEvent_id": event.id,
                 "weightKgs": 50,
                 "species_id": "XXX"}

        pd = PendingDocument(user=self.user, doc=dict(catch))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, FishCatch)
        self.assertEqual(model.weightKgs, 50)

    def test_nonfishingevent(self):
        trip = Trip.objects.create(creator=self.user, **self._get_trip())
        event = {"document_type": "nonFishingEvent",
                 "id": str(uuid.uuid4()),
                 "nonFishProtectedSpecies_id": "XXX",
                 "estimatedWeightKg": 20,
                 "tags": ["1234"],
                 "isVesselUsed": True,
                 "archived": False,  # TODO add default to the model
                 "completed": timezone.now().isoformat(),  # TODO fix the model
                 "completedDateTime": timezone.now().isoformat(),
                 "eventHeader": {},  # what is this for?
                 "eventVersion": timezone.now().isoformat(),  # what is this for?
                 "trip_id": str(trip.id)}

        pd = PendingDocument(user=self.user, doc=dict(event))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, NonFishingEvent)

    def test_vessellocation(self):
        loc = {"document_type": "vesselLocation",
               "vessel_id": str(self.vessel.id),
               "timestamp": timezone.now().isoformat(),
               "location": "POINT(40 40)"}

        pd = PendingDocument(user=self.user, doc=dict(loc))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, VesselLocation)
        self.assertEqual(model.timestamp, loc["timestamp"])
        self.assertEqual(model.location.coords, (40.0, 40.0))
