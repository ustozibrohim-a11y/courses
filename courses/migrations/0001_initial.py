# Generated manually for Online Kurs Platformasi

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Kurs nomi')),
                ('description', models.TextField(blank=True, verbose_name="Kurs haqida")),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")),
                ('is_active', models.BooleanField(default=True, verbose_name='Kurs holati')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'Teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='taught_courses', to=settings.AUTH_USER_MODEL, verbose_name="O'qituvchi")),
            ],
            options={
                'verbose_name': 'Kurs',
                'verbose_name_plural': 'Kurslar',
                'ordering': ['-added_at'],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True, verbose_name='Yozilgan sana')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faollik')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.course', verbose_name='Kurs')),
                ('student', models.ForeignKey(limit_choices_to={'role': 'Student'}, on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL, verbose_name='Talaba')),
            ],
            options={
                'verbose_name': 'Yozilish',
                'verbose_name_plural': 'Yozilishlar',
                'ordering': ['-enrolled_at'],
                'unique_together': {('student', 'course')},
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Dars nomi')),
                ('content', models.TextField(blank=True, verbose_name='Dars mazmuni')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course', verbose_name='Kurs')),
            ],
            options={
                'verbose_name': 'Dars',
                'verbose_name_plural': 'Darslar',
                'ordering': ['course', 'order', 'added_at'],
            },
        ),
    ]
