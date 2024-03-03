from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from .models import Product, Lesson
from .serializers import ProductSerializer, LessonSerializer, GroupSerializer, GroupCreateSerializer
from django.utils import timezone

from edu.models import Group


def distribute_users_to_groups(product, user):
    groups = Group.objects.filter(product=product)
    group_students_count = [group.students.count() for group in groups]

    if product.start_date <= timezone.now():
        non_zero_groups = groups.exclude(students=None)
        min_group = min(non_zero_groups, key=lambda group: group.students.count())

        if min_group.students.count() < min_group.max_students:
            min_group.students.add(user)
            return None

    total_students = sum(group_students_count)
    if total_students >= sum(group.max_students for group in groups):
        return None

    non_zero_groups = groups.exclude(students=None)
    avg_students_per_group = total_students / non_zero_groups.count()
    if total_students == 0 or avg_students_per_group == non_zero_groups.first().max_students:
        for group in groups:
            if group.students.count() == 0:
                group.students.add(user)

                non_empty_groups = [group for group in groups if group.students.count() > 0]

                while max(group_students_count) - min(group_students_count) > 1:
                    max_group = max(non_empty_groups, key=lambda group: group.students.count())
                    min_group = min(non_empty_groups, key=lambda group: group.students.count())

                    user_to_move = max_group.students.last()
                    min_group.students.add(user_to_move)
                    max_group.students.remove(user_to_move)

                    group_students_count = [group.students.count() for group in non_empty_groups]
                return None

    min_group = min(groups, key=lambda group: group.students.count())
    min_group.students.add(user)
    return None


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        student_id = request.data.get('student_id')
        if student_id:
            student = get_object_or_404(User, pk=student_id)
            instance.students.add(student)
            distribute_users_to_groups(instance, student.id)

        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        if self.request.user in product.students.all():
            return Lesson.objects.filter(product=product)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        serializer = GroupCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        student_id = request.data.get('student_id')
        if student_id:
            student = get_object_or_404(User, pk=student_id)
            instance.students.add(student)

        return Response(serializer.data)