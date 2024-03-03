from rest_framework import serializers
from .models import Product, Lesson, Group


class ProductSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'start_date', 'cost', 'num_lessons']

    def get_num_lessons(self, obj):
        return obj.lesson_set.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link', 'product']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'min_students', 'max_students', 'product', 'students']


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'min_students', 'max_students', 'product']