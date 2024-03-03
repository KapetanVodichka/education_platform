from django.db import models

from config import settings


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    start_date = models.DateTimeField(verbose_name='Дата и время старта')
    cost = models.IntegerField(verbose_name='Стоимость')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор', blank=True,
                               null=True, related_name='product_author')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Студент', related_name='product_students')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    video_link = models.URLField(verbose_name='Ссылка на видео')

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Group(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название группы')
    min_students = models.IntegerField(verbose_name='Минимальное количество участников')
    max_students = models.IntegerField(verbose_name='Максимальное количество участников')

    students = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Ученик')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
