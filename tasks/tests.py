from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Task

class TaskTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser2 = get_user_model().objects.create_user(
            username="testuser2", password="pass2"
        )

        test_task = Task.objects.create(
            title="rake",
            created_by=testuser1,
            description="Better for collecting leaves than a shovel.",
        )

    def setUp(self) -> None:
        self.client.login(username="testuser1", password="pass")  

    def test_task_model(self):
        task = Task.objects.get(id=1)
        actual_created_by = str(task.created_by)
        actual_title = str(task.title)
        actual_desc = str(task.description)
        self.assertEqual(actual_created_by, "testuser1")
        self.assertEqual(actual_title, "rake")
        self.assertEqual(
            actual_desc, "Better for collecting leaves than a shovel."
        )

    def test_get_task_list(self):
        url = reverse("task_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = response.data
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "rake")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("task_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_delete_task(self):
        self.client.logout()
        self.client.login(username="testuser2", password="pass2")
        url = reverse("task_retrieve_update_delete", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
