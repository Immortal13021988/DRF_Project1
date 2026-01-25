from rest_framework import serializers


from .models import Course, Lesson, Subscription
from .validators import ValidateInvitedUrl


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор по курсам"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор по курсам"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [ValidateInvitedUrl(field='video_url')]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор по курсам с добавлением поля всех уроков и с количеством уроков"""

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "description", "preview", "lessons", "lesson_count"]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['user_sub', 'course_sub', 'is_sub']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        course = obj.course_subscription

        return Subscription.objects.filter(user_sub=user, course_sub=course).exists()
