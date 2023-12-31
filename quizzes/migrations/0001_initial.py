# Generated by Django 4.1.7 on 2023-08-20 11:00

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
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('correct', models.BooleanField(default=False, verbose_name='Верно')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Имя')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Опубликован')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
                'ordering': ['published'],
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.IntegerField(default=0, verbose_name='Верно')),
                ('wrong', models.IntegerField(default=0, verbose_name='Неверно')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz', verbose_name='Викторина')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Название')),
                ('question_type', models.CharField(choices=[('single', 'Single'), ('multiple', 'Multiple')], default='single', max_length=8, verbose_name='Тип')),
                ('explanation', models.CharField(max_length=512, verbose_name='Объяснение')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quiz', verbose_name='Викторина')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.answer', verbose_name='Ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question', verbose_name='Вопрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question', verbose_name='Вопрос'),
        ),
    ]
