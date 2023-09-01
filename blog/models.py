from django.contrib.auth.models import User
from django.db import models
from users.models import Profile
from pytils.translit import slugify


class Category(models.Model):
    name = models.CharField('Название', max_length=32)
    slug = models.SlugField('URL')

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Название', max_length=32)
    slug = models.SlugField('URL')

    def save(self, *args, **kwargs):
        value = self.name

        self.slug = slugify(value)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тег')
    bookmarks = models.ManyToManyField(User, related_name='bookmarks', blank=True, verbose_name='Закладки')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True, verbose_name='Понравилось')
    slug = models.SlugField('URL')
    title = models.CharField('Заголовок', max_length=128)
    text = models.TextField('Содержимое', max_length=2048)
    published = models.DateTimeField('Опубликован', auto_now_add=True)

    def get_unique_slug(self):
        slug = slugify(self.title)

        unique_slug = slug

        num = 1

        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}{num}'

            num += 1

        return unique_slug

    def number_of_likes(self):
        return self.likes.count() or ''

    def number_of_bookmarks(self):
        return self.bookmarks.count() or ''

    def number_of_comments(self):
        return self.comments.filter(approved=True).count() or ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner}: {self.title}'

    class Meta:
        ordering = ['-published']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField('Содержимое')
    published = models.DateTimeField('Опубликован', auto_now_add=True)
    approved = models.BooleanField('Одобрено', default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-published']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
