# Generated by Django 3.2.7 on 2021-09-26 17:28

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.CharField(blank=True, default='', max_length=150, verbose_name='Адреса')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефону')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('birth_year', models.IntegerField(blank=True, default=None, null=True, verbose_name='Рік народження')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Caretaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_buttons_received', models.IntegerField(default=0, verbose_name='Кількість кнопок получено')),
                ('number_buttons_responded', models.IntegerField(default=0, verbose_name='Кількість кнопок оброблено')),
                ('active', models.BooleanField(default=True, verbose_name='Активний')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Доглядач',
                'verbose_name_plural': 'Доглядачі',
            },
        ),
        migrations.CreateModel(
            name='StatusChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статуси',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_buttons_event', models.IntegerField(default=0, verbose_name='Кількість натискань кнопки')),
                ('registration_code', models.CharField(db_index=True, max_length=150, unique=True, verbose_name='Реєстраційний код')),
                ('active', models.BooleanField(default=True, verbose_name='Активний')),
                ('caretaker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='alarmbutton.caretaker', verbose_name='Доглядач')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Підопічний')),
            ],
            options={
                'verbose_name': 'Підопічний',
                'verbose_name_plural': 'Підопічні',
                'ordering': ['registration_code'],
            },
        ),
        migrations.CreateModel(
            name='ButtonsEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створений')),
                ('responded_at', models.DateTimeField(default=None, null=True, verbose_name='Отримана відповідь')),
                ('resolved_at', models.DateTimeField(default=None, null=True, verbose_name='Вирішено')),
                ('comment', models.CharField(blank=True, default=None, max_length=300, null=True, verbose_name='Коментар')),
                ('caretaker', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='alarmbutton.caretaker', verbose_name='Доглядач')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='alarmbutton.customer', verbose_name='Підопічний')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='alarmbutton.statuschoices', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Подія',
                'verbose_name_plural': 'Події',
                'ordering': ['created_at'],
            },
        ),
    ]
