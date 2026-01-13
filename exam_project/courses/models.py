from django.db import models
from django.contrib.auth.models import User

class TimedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(TimedModel):
    title = models.CharField(
        max_length=255,
        verbose_name='Курс',
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    start_date = models.DateField(
        null=False,
        blank=False,
        verbose_name='Дата начала',
    )
    end_date = models.DateField(
        null=False,
        blank=False,
        verbose_name='Дата окончания',
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Автор',
        related_name='created_courses'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(TimedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Курс',
        related_name='lessons'
    )
    title = models.CharField(
        max_length=255,
        null = False,
        blank = False,
        verbose_name = 'Название',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name='Текст',
    )

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title


class Review(TimedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Курс',
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Пользователь',
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        null = False,
        blank = False,
        verbose_name = 'Оценка',
    )
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name='Комментарий',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.course} - {self.rating}'
