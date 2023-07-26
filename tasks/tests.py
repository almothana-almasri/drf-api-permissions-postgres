from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from tasks.models import Task

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
            title="Test Task",
            description="This is a test task.",
            created_by=testuser1,
        )

    def setUp(self) -> None:
        self.client.login(username="testuser1", password="pass")

    def test_task_model(self):
        task = Task.objects.get(id=1)
        actual_owner = str(task.created_by)
        actual_title = str(task.title)
        actual_desc = str(task.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_title, "Test Task")
        self.assertEqual(actual_desc, "This is a test task.")

    def test_get_task_list(self):
        url = reverse("task-list")  # Change "task_list" to your actual view name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = response.data
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Test Task")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("task-list")  # Change "task_list" to your actual view name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_delete_task(self):
        self.client.logout()
        self.client.login(username="testuser2", password="pass2")
        url = reverse("task-detail", args=[1])  # Change "task_detail" to your actual view name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
