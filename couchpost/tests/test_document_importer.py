import unittest
from couchpost.models import PendingDocument
from django.contrib.auth.models import User
from couchpost.document_importer import CouchDBDocumentImporter


class TestDocumentImporter(unittest.TestCase):

    def test_docs(self):
        u = User(id=77, username="test_dummy")
        d = PendingDocument(user=u, doc={"document_type": "fishserveEvent",
                                         "event_type": "tripStart",
                                         "json": "{fishserve: 'sucks'}",
                                         "headers": {"fish": "head"}})

        model = CouchDBDocumentImporter().process_document(d)

        self.assertEqual(model.creator.id, u.id)
