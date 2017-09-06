from reporting.models import User
from reporting.models import Organisation
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

User.objects.filter(username='restadmin').delete();\
User.objects.create_superuser('restadmin', 'restadmin@test.com', 'restinpeace')

try:
    skipper = Group.objects.get(name='skipper')
except ObjectDoesNotExist:
    skipper = Group.objects.create(name='skipper')

org = Organisation.objects.create(fullName="Rimu Industries REST")
User.objects.filter(username='resttester').delete();\
u = User.objects.create_user('resttester', 'rest@test.com', 'testrester', organisation=org)
u.groups.add(skipper)

org = Organisation.objects.create(fullName="Hackers Inc.")
User.objects.filter(username='resthacker').delete();\
u = User.objects.create_user('resthacker', 'resthack@test.com', 'testhack', organisation=org)
u.groups.add(skipper)
