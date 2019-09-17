from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.datetime_safe import datetime, date

from timezone_field import TimeZoneField


class Member(models.Model):

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    skills = models.ManyToManyField(  # This is all skills member has, ManyToMany relationship
        'skills.Skill',
        blank=True,
    )

    project = models.ForeignKey(  # The project of the member, OneToMany relationship
        'projects.Project',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )

    manager_id = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )

    workhours = models.ForeignKey(
        'WorkHours',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )

    on_holidays_till = models.DateField(
        blank=True, null=True
    )

    @property
    def is_available(self):
        if not self.on_holidays_till or self.on_holidays_till < date.today():
            return True
        return False

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class WorkHours(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    timezone = TimeZoneField()  # works with pytz

    def __str__(self):
        return f'Start: {self.start}, End: {self.end}, Timezone: {self.timezone}'
