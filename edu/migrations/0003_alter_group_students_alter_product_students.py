# Generated by Django 5.0.2 on 2024-03-03 05:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Ученик'),
        ),
        migrations.AlterField(
            model_name='product',
            name='students',
            field=models.ManyToManyField(related_name='product_students', to=settings.AUTH_USER_MODEL, verbose_name='Студент'),
        ),
    ]
