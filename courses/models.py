from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Kurs nomi')
    description = models.TextField(blank=True, verbose_name='Kurs haqida')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_courses',
        limit_choices_to={'role': 'Teacher'},
        verbose_name='O\'qituvchi'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Qo\'shilgan sana')
    is_active = models.BooleanField(default=True, verbose_name='Kurs holati')

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['-added_at']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Kurs'
    )
    title = models.CharField(max_length=255, verbose_name='Dars nomi')
    content = models.TextField(blank=True, verbose_name='Dars mazmuni')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Qo\'shilgan sana')

    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'
        ordering = ['course', 'order', 'added_at']

    def __str__(self):
        return f'{self.course.name} – {self.title}'


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'Student'},
        verbose_name='Talaba'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Kurs'
    )
    phone = models.CharField(max_length=100, null=True, blank=True)
    tg = models.CharField(max_length=100, null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='Yozilgan sana')
    is_active = models.BooleanField(default=True, verbose_name='Faollik')

    class Meta:
        verbose_name = 'Yozilish'
        verbose_name_plural = 'Yozilishlar'
        unique_together = [['student', 'course']]
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.student.username} – {self.course.name}'
