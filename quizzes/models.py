from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    name = models.CharField('Имя', max_length=128)
    published = models.DateTimeField('Опубликован', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['published']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    class question_type(models.TextChoices):
        single = 'single'
        multiple = 'multiple'

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Викторина')
    name = models.CharField('Название', max_length=512)
    question_type = models.CharField('Тип', max_length=8, choices=question_type.choices, default=question_type.single)
    explanation = models.CharField('Объяснение', max_length=512)

    def user_can_answer(self, user):
        user_choices = user.choice_set.all()

        done = user_choices.filter(question=self)

        return not done.exists()

    def get_answers(self):
        if self.question_type == 'single':
            return self.answer_set.filter(correct=True).first()

        qs = self.answer_set.filter(correct=True).values()

        return [i.get('name') for i in qs]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    name = models.CharField('Название', max_length=256)
    correct = models.BooleanField('Верно', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Викторина')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    correct = models.IntegerField('Верно', default=0)
    wrong = models.IntegerField('Неверно', default=0)
