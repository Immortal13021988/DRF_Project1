from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):
    """Тесты для уроков (Lesson)"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="Первый", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Введение", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест одного урока"""

        url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тест создания урока"""

        url = reverse(
            "lms:lesson_create",
        )
        data = {"title": "Ознакомление"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест изменения урока"""

        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {"title": "Погружение"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Погружение")

    def test_lesson_delete(self):
        """Тест удаление урока"""

        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест списка уроков"""

        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": None,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)


class CourseTestCase(APITestCase):
    """Тесты для курсов (Course)"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="Первый", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Введение", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тест одного курса"""

        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        """Тест создания курса"""

        url = reverse("lms:course-list")
        data = {"title": "Ознакомление"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест изменения курса"""

        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "Погружение"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Погружение")

    def test_lesson_delete(self):
        """Тест удаления курса"""

        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """Тест списка курсов"""

        url = reverse("lms:course-list")
        response = self.client.get(url)

        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "preview": None,
                    "description": None,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    """Тесты для подписок (Subscription)"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="Первый", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Введение", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribed(self):
        url = reverse("lms:subscribe")

        data = {"course_id": self.course.pk}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(
                course_sub=self.course.pk, user_sub=self.user.pk
            ).exists()
        )
