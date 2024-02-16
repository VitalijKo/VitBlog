from django.contrib.auth.models import User
from django.db import models
from pytils.translit import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True, verbose_name='Подписан')
    username = models.CharField('Имя пользователя', max_length=64, blank=True, null=True)
    image = models.ImageField('Фото', null=True, blank=True, upload_to='', default='default.jpg')
    name = models.CharField('Имя', max_length=64, blank=True, null=True)
    email = models.EmailField('Email', max_length=64, blank=True, null=True)
    city = models.CharField('Город', max_length=32, blank=True, null=True)
    profession = models.CharField('Профессия', max_length=128, blank=True, null=True)
    summary = models.CharField('О себе', max_length=128, blank=True, null=True)
    about = models.TextField('Описание', blank=True, null=True)
    vk = models.CharField('VK', max_length=128, default='https://vk.com')
    github = models.CharField('Github', max_length=128, default='https://github.com')
    youtube = models.CharField('YouTube', max_length=128, default='https://youtube.com')
    website = models.CharField('Сайт', max_length=128, default='https://mysite.com')
    created = models.DateTimeField('Создан', auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['created']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Interest(models.Model):
    profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Профиль')
    slug = models.SlugField('URL')
    name = models.CharField('Имя', max_length=128, blank=True, null=True)
    description = models.TextField('Описание', null=True, blank=True)
    created = models.DateTimeField('Создан', auto_now_add=True)

    def save(self, *args, **kwargs):
        value = self.name

        self.slug = slugify(value)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created']
        verbose_name = 'Интерес'
        verbose_name_plural = 'Интересы'
        unique_together = ('name', 'slug', 'profile')

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Отправитель')
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages', verbose_name='Получатель')
    name = models.CharField('Имя', max_length=128, null=True, blank=True)
    email = models.EmailField('Email', max_length=128, null=True, blank=True)
    subject = models.CharField('Тема', max_length=128, null=True, blank=True)
    body = models.TextField('Содержимое')
    seen = models.BooleanField('Просмотрено', default=False, null=True)
    created = models.DateTimeField('Создано', auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['seen', '-created']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
