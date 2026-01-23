from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Course, Lesson
from .validators import ValidateInvitedUrl


class CourseSerializer(ModelSerializer):
    """Сериализатор по курсам"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Сериализатор по курсам"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [ValidateInvitedUrl(field='video_url')]


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор по курсам с добавлением поля всех уроков и с количеством уроков"""

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = SerializerMethodField()

    @staticmethod
    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "description", "preview", "lessons", "lesson_count"]
