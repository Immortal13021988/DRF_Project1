from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModer, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import PageNumbersPagination
from .serializers import (CourseDetailSerializer, CourseSerializer,
                          LessonSerializer)


class CourseViewSet(ModelViewSet):
    """Класс для выполнения всех CRUD операций с курсами."""

    queryset = Course.objects.all()
    pagination_class = PageNumbersPagination

    def get_serializer_class(self):
        """Выбираем сериализатор"""
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    # def get_serializer(self, *args, **kwargs):
    #     """Переопределяем метод для передачи request в контекст."""  #  Пока не требуется, т.к. хз
    #     kwargs['context'] = kwargs.get('context', {})
    #     kwargs['context']['request'] = self.request
    #     print("get_serializer")
    #     return super().get_serializer(*args, **kwargs)

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
    pagination_class = PageNumbersPagination


class SubscriptionAPIView(APIView):
    """Контроллер по установки подписки пользователя и на удаление подписки у пользователя."""

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        if not course_id:
            return Response(
                {"error": "course_id обязателен"}, status=status.HTTP_400_BAD_REQUEST
            )
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user_sub=user, course_sub=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():

            subs_item.delete()
            message = "Подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user_sub=user, course_sub=course_item)

            message = "Подписка добавлена"
        # Возвращаем ответ в API
        return Response({"message": message})
