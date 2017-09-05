from reporting.models import User
from reporting.models import Organisation, Trip, Port, Vessel

User.objects.filter(username='restadmin').delete();\
User.objects.create_superuser('restadmin', 'restadmin@test.com', 'restinpeace')

orgs = Organisation.objects.filter(fullName="Rimu Industries REST")
for o in orgs:
    Trip.objects.filter(organisation=o).delete()
    Port.objects.filter(organisation=o).delete()
    Vessel.objects.filter(organisation=o).delete()
orgs.delete()
org = Organisation.objects.create(fullName="Rimu Industries REST")
User.objects.filter(username='resttester').delete()
User.objects.create_user('resttester', 'rest@test.com', 'testrester', organisation=org)

org = Organisation.objects.create(fullName="Hackers Inc.")
User.objects.filter(username='resthacker').delete();\
User.objects.create_user('resthacker', 'resthack@test.com', 'testhack', organisation=org)
