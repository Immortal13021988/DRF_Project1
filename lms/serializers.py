from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Сериализатор по курсам"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор по курсам с добавлением поля с количеством уроков"""
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "description", "preview", "lessons", "lesson_count"]
