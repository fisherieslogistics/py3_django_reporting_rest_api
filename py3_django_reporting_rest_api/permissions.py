from django.contrib.auth.backends import ModelBackend
from rest_framework.permissions import DjangoModelPermissions

_group_permissions = {
    'superuser': [],
    'skipper': [
        'reporting.read_fishcatch',
        'reporting.add_fishcatch',
        'reporting.change_fishcatch',
        'reporting.delete_fishcatch',
        'reporting.read_fishingevent',
        'reporting.add_fishingevent',
        'reporting.change_fishingevent',
        'reporting.delete_fishingevent',
        'reporting.read_nonfishingevent',
        'reporting.add_nonfishingevent',
        'reporting.change_nonfishingevent',
        'reporting.delete_nonfishingevent',
        'reporting.read_port',
        'reporting.add_port',
        'reporting.change_port',
        'reporting.delete_port',
        'reporting.read_trip',
        'reporting.add_trip',
        'reporting.change_trip',
        'reporting.delete_trip',
        'reporting.read_vessel',
        'reporting.add_vessel',
        'reporting.change_vessel',
        'reporting.delete_vessel',
    ]
}
class UserGroupBackend(ModelBackend):
    def get_all_permissions(self, user_obj, obj=None):
        perms = []
        for g in user_obj.groups.all():
            perms.extend(_group_permissions[g.name])
        return perms


class ReadWriteModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.read_%(model_name)s']
