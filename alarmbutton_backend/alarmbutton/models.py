import random
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# UKR
CARETAKER = 'Доглядач'
# USER = 'Користувач'
CLIENT = 'Підопічний'
EVENT = 'Подія'
STATUS = 'Статус'


class Users(AbstractUser):

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Caretaker(models.Model):
    address = models.CharField(max_length=150, verbose_name='Адреса', blank=True, default='', )
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефону')
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    fathers_name = models.CharField(verbose_name='По батькові', max_length=150)
    number_buttons_received = models.IntegerField(verbose_name='Кількість кнопок получено', default=0)
    number_buttons_responded = models.IntegerField(verbose_name='Кількість кнопок оброблено', default=0)
    active = models.BooleanField(default=True, verbose_name='Активний')
    comment = models.CharField(max_length=300, verbose_name='Коментар', null=True, default=None, blank=True)

    class Meta:
        verbose_name = CARETAKER
        verbose_name_plural = 'Доглядачі'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Customer(models.Model):
    address = models.CharField(max_length=150, verbose_name='Адреса', blank=True, default='', )
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефону')
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    fathers_name = models.CharField(verbose_name='По батькові', max_length=150)
    birth_year = models.IntegerField(verbose_name='Рік народження',)
    caretaker = models.ForeignKey('Caretaker', on_delete=models.PROTECT, verbose_name='Доглядач')
    number_buttons_event = models.IntegerField(verbose_name='Кількість натискань кнопки', default=0)
    registration_code = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='Реєстраційний код')
    active = models.BooleanField(default=True, verbose_name='Активний')
    comment = models.CharField(max_length=300, verbose_name='Коментар', null=True, default=None, blank=True)

    class Meta:
        verbose_name = CLIENT
        verbose_name_plural = 'Підопічні'
        ordering = ['registration_code']

    def generate_unique_reg_code(self):
        while True:
            code = str(random.randint(12345000, 99999999))
            if not Customer.objects.filter(registration_code=code).first():
                break

        self.registration_code = code

    def save(self, **kwargs):
        if not self.id:
            self.generate_unique_reg_code()
        super().save(**kwargs)

    def __str__(self):
        year = ' ' + str(self.birth_year) if self.birth_year else ''
        return f'{self.last_name} {self.first_name}{year}'


class StatusChoices(models.Model):
    status = models.CharField(max_length=100, verbose_name='Статус')

    class Meta:
        verbose_name = STATUS
        verbose_name_plural = 'Статуси'

    def __str__(self):
        return self.status


class ButtonsEvents(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name='Підопічний')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створений')
    responded_at = models.DateTimeField(default=None, null=True, verbose_name='Отримана відповідь')
    resolved_at = models.DateTimeField(default=None, null=True, verbose_name='Вирішено')
    caretaker = models.ForeignKey('Caretaker', on_delete=models.PROTECT, null=True, verbose_name='Доглядач', default=None)
    status = models.ForeignKey('StatusChoices', on_delete=models.PROTECT, default=1, verbose_name='Статус')
    comment = models.CharField(max_length=300, verbose_name='Коментар', null=True, default=None, blank=True)
    # caretaker_changed_flag = models.BooleanField(verbose_name='Доглядача змінено', default=False)

    class Meta:
        verbose_name = EVENT
        verbose_name_plural = 'Події'
        ordering = ['created_at']

    def save(self, **kwargs):
        if self.id:
            if not self.responded_at and self.status.id == 2:
                self.responded_at = datetime.now().replace(microsecond=0)
            if not self.resolved_at and self.status.id == 3:
                self.resolved_at = datetime.now().replace(microsecond=0)
                caretaker = Caretaker.objects.get(id=self.caretaker.id)
                caretaker.number_buttons_responded = caretaker.number_buttons_responded + 1
                caretaker.save()
        super().save(**kwargs)
