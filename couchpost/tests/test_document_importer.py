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
                                 "documentReady": True,
                                 "_id": "whatevs should be ignored",
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
                "personInCharge": "Raiden",
                "startTime": timezone.now().isoformat(),
                "endTime": timezone.now().isoformat(),
                "ETA": timezone.now().isoformat(),
                "startLocation": "POINT(45 45)",
                "unloadPort_id": str(self.port.id),
                "vessel_id": str(self.vessel.id)}

    def test_documentReady(self):
        trip = self._get_trip()
        trip.update({"document_type": "trip"})

        pd = PendingDocument(user=self.user, doc=dict(trip))
        self.assertIsNone(CouchDBDocumentImporter().process_document(pd), "Document not ready, should not be saved.")
        # pending doc must be marked as processed to prevent future retries
        self.assertEqual(pd.process_status, Status.SKIPPED.value)

    def test_trip(self):
        trip = self._get_trip()
        trip.update({"document_type": "trip",
                     "documentReady": True,
                     "_id": "ignorable garbage"})

        pd = PendingDocument(user=self.user, doc=dict(trip))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, Trip)
        self.assertEqual(model.creator.id, self.user.id)
        self.assertEqual(model.organisation_id, str(self.org.id))
        self.assertEqual(model.startTime, trip["startTime"])
        self.assertEqual(model.startLocation.coords, (45.0, 45.0))

        # update the same trip
        pd = PendingDocument(user=self.user, doc=dict(trip))
        pd = PendingDocument(user=self.user, doc=dict(trip))
        model = CouchDBDocumentImporter().process_document(pd)

        # TODO test updating of a trip that belongs to different org (must fail)

        # non-existent org
        trip['organisation_id'] = str(uuid.uuid4())
        pd = PendingDocument(user=self.user, doc=dict(trip))
        model = CouchDBDocumentImporter().process_document(pd)
        self.assertIsNone(model)
        self.assertEqual(pd.process_status, Status.ERROR.value)
        self.assertIn("Organisation ID", pd.details)

    def _get_fishevent(self, trip):
        return {"id": str(uuid.uuid4()),
                "targetSpecies_id": "XXX",
                "vesselNumber": "123",
                "trip_id": str(trip.id),
                "eventSpecificDetails": {"sun": "shining"}}

    def test_fishingevent(self):
        trip = Trip.objects.create(creator=self.user, **self._get_trip())
        event = self._get_fishevent(trip)
        event.update({"document_type": "fishingEvent",
                     "documentReady": True})

        pd = PendingDocument(user=self.user, doc=dict(event))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, FishingEvent)
        self.assertEqual(model.creator.id, self.user.id)
        self.assertEqual(model.eventSpecificDetails, event["eventSpecificDetails"])

        # update event
        pd = PendingDocument(user=self.user, doc=dict(event))
        model = CouchDBDocumentImporter().process_document(pd)

    def test_fishcatch(self):
        trip = Trip.objects.create(creator=self.user, **self._get_trip())
        event = FishingEvent.objects.create(creator=self.user, **self._get_fishevent(trip))

        catch = {"document_type": "fishCatch",
                 "documentReady": True,
                 "id": str(uuid.uuid4()),
                 "_id": "whatevs should be ignored",
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
                 "documentReady": True,
                 "_id": "whatevs should be ignored",
                 "id": str(uuid.uuid4()),
                 "nonFishProtectedSpecies_id": "XXX",
                 "estimatedWeightKg": 20,
                 "tags": ["1234"],
                 "isVesselUsed": True,
                 "archived": False,  # TODO add default to the model
                 "completedDateTime": timezone.now().isoformat(),
                 "trip_id": str(trip.id)}

        pd = PendingDocument(user=self.user, doc=dict(event))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, NonFishingEvent)

    def test_vessellocation(self):
        loc = {"document_type": "vesselLocation",
               "documentReady": True,
               "_id": "whatevs should be ignored",
               "vessel_id": str(self.vessel.id),
               "timestamp": timezone.now().isoformat(),
               "location": "POINT(40 40)"}

        pd = PendingDocument(user=self.user, doc=dict(loc))
        model = CouchDBDocumentImporter().process_document(pd)

        self.assertEqual(pd.process_status, Status.OK.value)
        self.assertIsInstance(model, VesselLocation)
        self.assertEqual(model.timestamp, loc["timestamp"])
        self.assertEqual(model.location.coords, (40.0, 40.0))
