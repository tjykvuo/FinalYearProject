# Generated by Django 2.2.7 on 2020-03-05 17:40

import app.models
import app.validator
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('can_view_content', 'Can view content')],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('figure', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d', verbose_name='figure')),
                ('entans', models.CharField(default=True, help_text='Enter question', max_length=1000, verbose_name='entans')),
                ('questdescript', models.TextField(blank=True, help_text='Description of question after being answered', max_length=2000, verbose_name='Question Description')),
            ],
            options={
                'verbose_name': 'Question',
                'ordering': ['quiztype'],
            },
        ),
        migrations.CreateModel(
            name='QuizType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiztype', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Quiz Type')),
            ],
            options={
                'verbose_name': 'Quiz Type',
                'verbose_name_plural': 'Quiz Types',
            },
        ),
        migrations.CreateModel(
            name='MultipleChoice',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.Question')),
                ('answer_order', models.CharField(blank=True, choices=[('entans', 'entAns'), ('none', 'None')], help_text='the order in which questions are displayed', max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'Multiple Choice Question',
            },
            bases=('app.question',),
        ),
        migrations.CreateModel(
            name='UploadCSVFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to=app.models.csv_upload_instance, validators=[app.validator.csv_file_validator_function])),
                ('completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizCBM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=1024, verbose_name='Result')),
                ('right_answer', models.CharField(max_length=10, verbose_name='Right Answer')),
                ('wrong_answer', models.CharField(max_length=10, verbose_name='Wrong Answer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Quiz Progression',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('descriptor', models.TextField(blank=True, help_text='Useful information about the quiz', verbose_name='Quiz Description')),
                ('url', models.SlugField(help_text='a useful url', max_length=60, verbose_name='a compatible url that is user friendly')),
                ('variable_order', models.BooleanField(default=False, help_text='Questions are displayed in random to prevent cheating', verbose_name='Variable Order')),
                ('attempt_record', models.BooleanField(default=False, help_text='if active; the result from an attempt will be recorded', verbose_name='Quiz Attempt Record')),
                ('max_questions', models.PositiveIntegerField(blank=True, help_text='Number of questions to be answered', null=True, verbose_name='Maximum questions')),
                ('answers_at_end', models.BooleanField(default=False, help_text='Answers displayed at end of quiz', verbose_name='Answers shown at end')),
                ('one_quiz_effort', models.BooleanField(default=False, help_text='If active, users can only have one attempt at quizso that users will not be able to cheat')),
                ('quiz_pass_mark', models.SmallIntegerField(blank=True, default=0, help_text='Mark required to pass the quiz', validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Mark')),
                ('quiz_pass_notif', models.TextField(blank=True, help_text='Display if user passes quiz', verbose_name='Pass Notification')),
                ('quiz_fail_notif', models.TextField(blank=True, help_text='Display if user fails to pass quiz.', verbose_name='Fail Notification')),
                ('quiz_outline', models.TextField(blank=True, default=False, help_text='If active; only authorised users will be able to take the quizas it will not be displayed in the Quiz List. Only users withquiz edit permissions may gain access.', verbose_name='Rough Outline')),
                ('quiztype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.QuizType', verbose_name='Quiz Type')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(blank=True, to='app.Quiz', verbose_name='Quiz'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiztype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.QuizType', verbose_name='QuizType'),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_order', models.CharField(max_length=1024, verbose_name='Question Order')),
                ('question_list', models.CharField(max_length=1024, verbose_name='Question List')),
                ('wrong_questions', models.CharField(blank=True, max_length=1024, verbose_name='Wrong Questions')),
                ('present_score', models.IntegerField(verbose_name='Present Score')),
                ('completed_attempt', models.BooleanField(default=False, verbose_name='Completed Attempt')),
                ('participant_answers', models.TextField(blank=True, default='{}', verbose_name='Answers From Test Participants')),
                ('attempt_start', models.DateTimeField(auto_now_add=True, verbose_name='Start of Attempt')),
                ('attempt_end', models.DateTimeField(auto_now_add=True, verbose_name='End of Attempt')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Quiz', verbose_name='Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'permissions': (('view_attempts', 'can see completed quizzes'),),
            },
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entans', models.CharField(help_text='enter answer', max_length=1000, verbose_name='entAns')),
                ('correct', models.BooleanField(default=False, help_text='is this a correct answer to the proposed question?')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MultipleChoice')),
            ],
        ),
    ]
