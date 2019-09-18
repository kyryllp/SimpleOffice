import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from projects.models import Project
from skills.models import Skill
from projects.serializers import ProjectSerializer

client = Client()


class GetAllProjectsTest(TestCase):
    """ Test module for getting all projects """

    def setUp(self) -> None:
        self.test = Project.objects.create(
            name='test'
        )

    def test_get_all_projects(self):
        response = client.get(reverse('projects-list'))
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProjectTest(TestCase):
    """ Test module for getting single project """

    def setUp(self) -> None:
        self.test = Project.objects.create(
            name='test'
        )

    def test_get_valid_single_project(self):
        response = client.get(
            reverse('projects-detail', kwargs={'pk': self.test.pk}))
        project = Project.objects.get(pk=self.test.pk)
        serializer = ProjectSerializer(project)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_project(self):
        response = client.get(
            reverse('projects-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewProjectTest(TestCase):
    """ Test module for inserting a new project """

    def setUp(self):
        self.valid_payload = {
            'name': 'JS',
        }
        self.invalid_payload = {
            'name': '',
        }

    def test_create_valid_project(self):
        response = client.post(
            reverse('projects-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_project(self):
        response = client.post(
            reverse('projects-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleProjectTest(TestCase):
    """ Test module for updating an existing project record """

    def setUp(self):
        self.test = Project.objects.create(
            name='test'
        )
        self.valid_payload = {
            'name': 'test1',
        }
        self.invalid_payload = {
            'name': '',
        }

    def test_valid_update_project(self):
        response = client.put(
            reverse('projects-detail', kwargs={'pk': self.test.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_project(self):
        response = client.put(
            reverse('projects-detail', kwargs={'pk': self.test.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleProjectTest(TestCase):
    """ Test module for deleting an existing project record """

    def setUp(self):
        self.test = Project.objects.create(
            name='test'
        )

    def test_valid_delete_project(self):
        response = client.delete(
            reverse('projects-detail', kwargs={'pk': self.test.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_project(self):
        response = client.delete(
            reverse('projects-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)