from reporting.models import User
from reporting.models import Organisation

User.objects.filter(username='restadmin').delete();\
User.objects.create_superuser('restadmin', 'rest@test.com', 'restinpeace')

Organisation.objects.filter(fullName="Rimu Industries REST").delete()
org = Organisation.objects.create(fullName="Rimu Industries REST")
User.objects.filter(username='resttester').delete()
User.objects.create_user('resttester', 'rest@test.com', 'testrester', organisation=org)
