from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    name = models.CharField('Вопрос', max_length=512)
    published = models.DateTimeField('Опубликован', auto_now_add=True)

    def user_voted(self, user):
        user_votes = user.vote_set.all()
        done = user_votes.filter(question=self)

        return not done.exists()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['published']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    name = models.CharField('Название', max_length=256)
    votes = models.IntegerField('Голоса', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Варианты'
        verbose_name_plural = 'Варианты'

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name='Выбор')

    def __str__(self):
        return f'{self.question.name[:15]} - {self.choice.name[:15]} - {self.user.username}'

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'
