from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Task


# Create your tests here.


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="TestPassword123!"
        )

    def test_task_creation(self):
        task = Task.objects.create(
            owner=self.user,
            title="Learn Django Testing",
            description="Write my first Django test.",
            status="pending",
            priority="high",
        )

        self.assertEqual(task.title, "Learn Django Testing")
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.priority, "high")

    def test_task_belongs_to_correct_user(self):
        another_user = User.objects.create_user(
            username="anotheruser", password="AnotherPassword123!"
        )
        task = Task.objects.create(
            owner=self.user, title="Private Task", status="pending", priority="medium"
        )
        self.assertEqual(task.owner, self.user)
        self.assertNotEqual(task.owner, another_user)

    def test_task_default_status(self):
        task = Task.objects.create(owner=self.user, title="Default Status Test")
        self.assertEqual(task.status, "pending")

    def test_task_default_priority(self):
        task = Task.objects.create(owner=self.user, title="Default Priority Test")
        self.assertEqual(task.priority, "medium")

    def test_task_list_requires_login(self):
        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_view_task_list(self):
        self.client.login(username="testuser", password="TestPassword123!")

        response = self.client.get(reverse("task_list"))

        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_create_task(self):
        self.client.login(username="testuser", password="TestPassword123!")

        response = self.client.post(
            reverse("create_task"),
            {
                "title": "Test Task",
                "description": "Testing task creation.",
                "status": "pending",
                "priority": "high",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Task.objects.filter(title="Test Task", owner=self.user).exists()
        )

    def test_user_cannot_access_another_users_task(self):
        another_user = User.objects.create_user(
            username="anotheruser", password="AnotherPassword123!"
        )

        task = Task.objects.create(
            owner=another_user,
            title="Private Task",
            status="pending",
            priority="medium",
        )

        self.client.login(username="testuser", password="TestPassword123!")

        response = self.client.get(reverse("task_detail", kwargs={"pk": task.pk}))

        self.assertEqual(response.status_code, 404)
