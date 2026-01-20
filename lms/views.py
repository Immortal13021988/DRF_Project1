from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer, IsOwner

from .models import Course, Lesson
from .serializers import (CourseDetailSerializer, CourseSerializer,
                          LessonSerializer)


class CourseViewSet(ModelViewSet):
    """Класс для выполнения всех CRUD операций с курсами."""

    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """Автоматически устанавливает текущего пользователя как владельца создаваемого объекта."""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """Определяем permissions в зависимости от действия."""
        if self.action == "create":
            # Создавать курсы могут только аутентифицированные пользователи НЕ модераторы
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            # Смотреть и редактировать могут владельцы ИЛИ модераторы
            self.permission_classes = (
                IsAuthenticated,
                IsOwner | IsModer,
            )
        elif self.action == "destroy":
            # Удалять могут только владельцы И НЕ модераторы
            self.permission_classes = (
                IsAuthenticated,
                IsOwner | ~IsModer,
            )
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Класс создания нового урока."""

    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModer,
    )

    def perform_create(self, serializer):
        """Автоматически устанавливает текущего пользователя как владельца создаваемого объекта."""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveApiView(RetrieveAPIView):
    """Класс просмотра (деталей) урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    """Класс изменения урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    """Класс удаления урока."""

    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class LessonListApiView(ListAPIView):
    """Класс списка всех уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
