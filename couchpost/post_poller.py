import couchdb
import logging
from django.conf import settings
from couchpost.models import PostStatus
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.utils import timezone
import datetime
from pytz import utc
import time

log = logging.getLogger(__name__)


class PostgresReplicator():
    couch = couchdb.Server(settings.DATABASES['couchdb']['URL'])
    couch.resource.credentials = (settings.DATABASES['couchdb']['USER'], settings.DATABASES['couchdb']['PASSWORD'])

    def get_last_time(self):
        try:
            return PostStatus.objects.get(pk=self.table_name).table_timestamp
        except ObjectDoesNotExist:
            return datetime.datetime.min.replace(tzinfo=utc)

    def update_last_time(self):
        PostStatus.objects.update_or_create(
            pk=self.table_name,
            defaults={'table_timestamp': self.now})

    def mangle_object(self, row):
        # perform custom transformations on the object
        row["table_name"] = self.table_name
        return row

    def get_id(self, doc):
        return doc['id']

    def get_database_name(self, row):
        return "org_%s" % row['organisation_id']

    def _get_sql_query(self):
        return "select row_to_json({table}) from {table} where updated > %s and updated <= %s".format(table=self.table_name)

    def _replicate_document(self, doc, target_db):
        doc = self.mangle_object(doc)

        doc_id = self.get_id(doc)
        # delete and (possibly) recreate the document... better than dealing with couchdb's revisions
        if doc_id in target_db:
            del target_db[doc_id]
        if [doc['active']]:
            target_db[doc_id] = doc

    def replicate_changes(self):
        self.now = timezone.now()
        sql = self._get_sql_query()

        with connection.cursor() as c:
            c.execute(sql, [self.get_last_time(), self.now])
            log.debug('Found %d changes for table %s.', c.cursor.rowcount, self.table_name)

            for row in c.fetchall():
                doc = row[0]
                log.debug(doc)

                target_db_name = self.get_database_name(doc)
                if target_db_name in self.couch:
                    target_db = self.couch[target_db_name]
                else:
                    log.info('Creating database ' + target_db_name + ' on server')
                    target_db = self.couch.create(target_db_name)

                self._replicate_document(doc, target_db)

        self.update_last_time()


class UsersDatabaseReplicator(PostgresReplicator):
    table_name = "auth_user"

    def _get_sql_query(self):
        return "select row_to_json({table}) from {table} where date_joined > %s and date_joined <= %s".format(table=self.table_name)

    def get_database_name(self, row):
        return "user_%s" % row['id']

    def _replicate_document(self, doc, target_db):
        pass  # nothing to replicate, we only want to create the new databases


class SpeciesReplicator(PostgresReplicator):
    table_name = "reporting_species"

    def get_database_name(self, _row):
        return "master_data"

    def get_id(self, doc):
        return "reporting_species_%s" % doc['code']  # trying to make it globally unique


class VesselsReplicator(PostgresReplicator):
    table_name = "reporting_vessel"


class PortsReplicator(PostgresReplicator):
    table_name = "reporting_port"


REPLICATED_TABLES = [SpeciesReplicator(), VesselsReplicator(), PortsReplicator(), UsersDatabaseReplicator()]


def poll_postgres_for_changes():
    for replicator in REPLICATED_TABLES:
        log.debug('Replicating table ' + replicator.table_name + ' to couch')
        replicator.replicate_changes()
