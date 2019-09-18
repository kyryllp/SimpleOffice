import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from skills.models import Skill
from skills.serializers import SkillSerializer

client = Client()


class GetAllSkillsTest(TestCase):
    """ Test module for getting all skills """

    def setUp(self) -> None:
        Skill.objects.create(
            name='JS'
        )
        Skill.objects.create(
            name='Python'
        )
        Skill.objects.create(
            name='Django'
        )

    def test_get_all_skills(self):
        response = client.get(reverse('skills-list'))
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleSkillTest(TestCase):
    """ Test module for getting single skill """

    def setUp(self) -> None:
        self.js = Skill.objects.create(
            name='JS'
        )

    def test_get_valid_single_skill(self):
        response = client.get(
            reverse('skills-detail', kwargs={'pk': self.js.pk}))
        skill = Skill.objects.get(pk=self.js.pk)
        serializer = SkillSerializer(skill)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_skill(self):
        response = client.get(
            reverse('skills-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewSkillTest(TestCase):
    """ Test module for inserting a new skill """

    def setUp(self):
        self.valid_payload = {
            'name': 'JS',
        }
        self.invalid_payload = {
            'name': '',
        }

    def test_create_valid_skill(self):
        response = client.post(
            reverse('skills-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_skill(self):
        response = client.post(
            reverse('skills-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleSkillTest(TestCase):
    """ Test module for updating an existing skill record """

    def setUp(self):
        self.js = Skill.objects.create(
            name='JS'
        )
        self.valid_payload = {
            'name': 'Python',
        }
        self.invalid_payload = {
            'name': '',
        }

    def test_valid_update_skill(self):
        response = client.put(
            reverse('skills-detail', kwargs={'pk': self.js.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_skill(self):
        response = client.put(
            reverse('skills-detail', kwargs={'pk': self.js.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleSkillTest(TestCase):
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