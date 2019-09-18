import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from members.models import Member, WorkHours
from members.serializers import MemberSerializer, WorkHoursSerializer
from projects.models import Project
from skills.models import Skill

client = Client()


class GetAllMembersTest(TestCase):
    """ Test module for getting all members """

    def setUp(self) -> None:
        """ For the convenience member is created only with two fields """
        Member.objects.create(
            first_name='Vasya',
            last_name='Pupkin',
        )

    def test_get_all_members(self):
        response = client.get(reverse('members-list'))
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMembersByFilters(TestCase):

    def setUp(self) -> None:
        self.js = Skill.objects.create(
            name='js'
        )

        self.project = Project.objects.create(
            name='project'
        )

        self.member = Member.objects.create(
            first_name='Vasya',
            last_name='Pupkin',
        )

        self.work_hours = WorkHours.objects.create(
            start="00:00:00",
            end="23:59:59",
            timezone="Europe/Kiev"
        )

        self.member.skills.set(Skill.objects.all())  # The only way to assign to the ManyToMany field
        self.member.project = self.project
        self.member.workhours = self.work_hours
        self.member.save()

        self.member2 = Member.objects.create(
            first_name='Petr',
            last_name='Petrov',
            on_holidays_till='3000-09-20'
        )

    def test_get_by_skills(self):
        response = client.get(reverse('members-list') + '?skills={}'.format(self.js.name))
        self.assertEqual(response.data['count'], 1)

    def test_get_by_project(self):
        response = client.get(reverse('members-list') + '?project={}'.format(self.project.pk))
        print(response)
        self.assertEqual(response.data['count'], 1)

    def test_get_by_holidays(self):
        response = client.get(reverse('members-list') + '?holidays=True')
        self.assertEqual(response.data['count'], 1)

    def test_get_by_is_working(self):
        response = client.get(reverse('members-list') + '?is_working=True')  # no matter what time it is
        # there is only gonna be one record in the response
        self.assertEqual(response.data['count'], 1)


class GetSingleMemberTest(TestCase):
    """ Test module for getting single member """

    def setUp(self) -> None:
        self.member = Member.objects.create(
            first_name='Vasya',
            last_name='Pupkin',
        )

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('members-detail', kwargs={'pk': self.member.pk}))
        member = Member.objects.get(pk=self.member.pk)
        serializer = MemberSerializer(member)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('members-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewMemberTest(TestCase):
    """ Test module for inserting a new member """

    def setUp(self):
        self.valid_payload = {
            "first_name": "Test",
            "last_name": "User"
        }

        self.invalid_payload = {
            'first_name': 'Vasya',
            'last_name': '',
        }

    def test_create_valid_member(self):
        response = client.post(
            reverse('members-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_member(self):
        response = client.post(
            reverse('members-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AssignMemberToProjectTest(TestCase):  # TODO

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='project'
        )

        self.member = Member.objects.create(
            first_name='Vasya',
            last_name='Pupkin',
            project=self.project
        )

        self.project2 = Project.objects.create(
            name='project2'
        )

        self.valid_payload = {
            "id": 2
        }

        self.invalid_payload = {
            "id": ""
        }

    def test_assigning_member_to_project(self):
        response = client.post(
            reverse('members-assign-to-project', kwargs={'pk': self.member.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_assigning_member_to_project(self):
        response = client.post(
            reverse('members-assign-to-project', kwargs={'pk': self.member.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleMemberTest(TestCase):
    """ Test module for updating an existing member record """

    def setUp(self):
        self.member = Member.objects.create(
            first_name='Vasya',
            last_name='Pupkin',
        )
        self.valid_payload = {
            "first_name": "Vasiliy",
            "last_name": "Pupkin",
        }
        self.invalid_payload = {
            'first_name': '',
        }

    def test_valid_update_member(self):
        response = client.put(
            reverse('members-detail', kwargs={'pk': self.member.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_member(self):
        response = client.put(
            reverse('members-detail', kwargs={'pk': self.member.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleMemberTest(TestCase):
    """ Test module for deleting an existing member record """

    def setUp(self):
        self.member = Member.objects.create(
            first_name='Vasya',
            last_name='Pupkin',
        )

    def test_valid_delete_member(self):
        response = client.delete(
            reverse('members-detail', kwargs={'pk': self.member.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_member(self):
        response = client.delete(
            reverse('members-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# ===================================== Work Hours Tests =====================================


class GetAllWorkHoursInstancesTest(TestCase):
    """ Test module for getting all workhours records """

    def setUp(self) -> None:
        WorkHours.objects.create(
            start="00:00:00",
            end="23:59:59",
            timezone="Europe/Kiev"
        )

    def test_get_all_skills(self):
        response = client.get(reverse('workhours-list'))
        workhours = WorkHours.objects.all()
        serializer = WorkHoursSerializer(workhours, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleWorkHoursInstanceTest(TestCase):
    """ Test module for getting single workhours record """

    def setUp(self) -> None:
        self.work_hours = WorkHours.objects.create(
            start="00:00:00",
            end="23:59:59",
            timezone="Europe/Kiev"
        )

    def test_get_valid_single_puppy(self):
        response = client.get(reverse('workhours-detail', kwargs={'pk': self.work_hours.pk}))
        workhours = WorkHours.objects.get(pk=self.work_hours.pk)
        serializer = WorkHoursSerializer(workhours)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('workhours-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewWorkHoursInstanceTest(TestCase):
    """ Test module for inserting a new workhours record """

    def setUp(self):
        self.valid_payload = {
            "start": "09:00:00",
            "end": "18:00:00"
        }

        self.invalid_payload = {
            "start": "",
            "end": ""
        }

    def test_create_valid_skill(self):
        response = client.post(
            reverse('workhours-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_skill(self):
        response = client.post(
            reverse('workhours-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleWorkHoursInstanceTest(TestCase):
    """ Test module for updating an existing workhours record """

    def setUp(self):
        self.work_hours = WorkHours.objects.create(
            start="00:00:00",
            end="23:59:59",
            timezone="Europe/Kiev"
        )

        self.valid_payload = {
            "start": "18:00:00",
            "end": "23:00:00"
        }

        self.invalid_payload = {
            "start": ""
        }

    def test_valid_update_workhours(self):
        response = client.put(
            reverse('workhours-detail', kwargs={'pk': self.work_hours.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_workhours(self):
        response = client.put(
            reverse('workhours-detail', kwargs={'pk': self.work_hours.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleWorkHoursInstanceTest(TestCase):
    """ Test module for deleting an existing skill record """

    def setUp(self):
        self.js = Skill.objects.create(
            name='JS'
        )

    def test_valid_delete_skill(self):
        response = client.delete(
            reverse('skills-detail', kwargs={'pk': self.js.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_skill(self):
        response = client.delete(
            reverse('skills-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
