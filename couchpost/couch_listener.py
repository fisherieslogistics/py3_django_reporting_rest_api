import couchdb
import logging
from django.conf import settings
from couchpost.models import CouchStatus, PendingDocument
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import re
import time

log = logging.getLogger(__name__)


class CouchDBReplicator():
    couch = couchdb.Server(settings.DATABASES['couchdb']['URL'])
    couch.resource.credentials = (settings.DATABASES['couchdb']['USER'], settings.DATABASES['couchdb']['PASSWORD'])

    def __init__(self, db_name):
        self.db_name = db_name
        self.db = self.couch[self.db_name]

    def get_last_seq(self):
        try:
            return CouchStatus.objects.get(pk=self.db_name).db_seq
        except ObjectDoesNotExist:
            return 0

    def update_last_seq(self, seq):
        CouchStatus.objects.update_or_create(
            pk=self.db_name,
            defaults={'db_seq': seq})


class UserDatabaseHandler():
    def accept(self, db_name):
        return re.fullmatch("^user_\d+$", db_name) is not None

    def handle_database_record(self, db_name, doc):
        if doc.get("_deleted", False):
            log.warning("Delete operation is not supported! %s", doc)
        else:
            PendingDocument.objects.create(user_id=int(db_name.split("_")[1]),
                                           doc=doc).save()


class ReplicationHalted(Exception):
    pass


def listen_for_couch_changes():
    global_changes = CouchDBReplicator('_global_changes')
    try:
        # this will listen for all changes happening in couchdb until something breaks (and the function returns)
        for db_change in global_changes.db.changes(feed="continuous", since=global_changes.get_last_seq(), heartbeat=1000, include_docs=False):
            try:
                action, source_db_name = db_change['id'].split(":")  # (e.g. updated:user_xxxx)
                handler = UserDatabaseHandler()  # at the moment we have only one functional handler

                if action == 'updated' and handler.accept(source_db_name):  # this means that some database was updated
                    with transaction.atomic():
                        source_db = CouchDBReplicator(source_db_name)
                        # get changes from the source database from the last replicated sequence
                        for doc_change in source_db.db.changes(feed="normal", since=source_db.get_last_seq(), include_docs=True)['results']:
                            try:
                                log.debug(doc_change['doc'])
                                handler.handle_database_record(source_db_name, doc_change['doc'])
                                # remember last seq from the last processed document
                                source_db.update_last_seq(doc_change['seq'])
                            except:
                                log.exception("Error processing document change: %s", doc_change)
                                raise ReplicationHalted()
                else:
                    log.info("Ignoring action %s on database %s", action, source_db_name)

                global_changes.update_last_seq(db_change['seq'])
            except:
                log.exception("Error processing global change: %s", db_change)
                raise ReplicationHalted()

    except ReplicationHalted:
        pass  # it's already logged
    except:
        log.exception("Something broke, will restart in %ds.", settings.COUCHDB_LISTENER_RETRY_TIMEOUT)
