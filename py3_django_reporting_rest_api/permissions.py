from django.contrib.auth.backends import ModelBackend
from rest_framework.permissions import DjangoModelPermissions

_group_permissions = {
    'skipper': {
        'reporting': [
            'read_fishcatch',
            'add_fishcatch',
            'change_fishcatch',
            'delete_fishcatch',
            'read_fishingevent',
            'add_fishingevent',
            'change_fishingevent',
            'delete_fishingevent',
            'read_nonfishingevent',
            'add_nonfishingevent',
            'change_nonfishingevent',
            'delete_nonfishingevent',
            'read_port',
            'add_port',
            'change_port',
            'delete_port',
            'read_trip',
            'add_trip',
            'change_trip',
            'delete_trip',
            'read_vessel',
            'add_vessel',
            'change_vessel',
            'delete_vessel',
        ]
    }
}

def _flatten_permissions():
    # transform the permission structure only once at the server start
    fp = {}
    for group, apps in _group_permissions.items():
        fp[group] = []
        for (perm_app, perm_list) in apps.items():
            for perm in perm_list:
                fp[group].append("%s.%s" % (perm_app, perm))
    return fp

_group_permissions_flattened = _flatten_permissions()

class UserGroupBackend(ModelBackend):
    def get_all_permissions(self, user_obj, obj=None):
        # list all user's permissions based on the hardcoded list above
        perms = []
        for g in user_obj.groups.all():
            perms.extend(_group_permissions_flattened.get(g.name, []))
        return perms


class ReadWriteModelPermissions(DjangoModelPermissions):
    def __init__(self):
        # django's standard permission model doesn't have the concept of "read" permission - so let's create it here.
        self.perms_map['GET'] = ['%(app_label)s.read_%(model_name)s']
