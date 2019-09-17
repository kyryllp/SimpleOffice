from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from timezone_field import TimeZoneField


class Member(models.Model):

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    skills = models.ManyToManyField(  # This is all skills, ManyToMany relationship
        'skills.Skill',  # TODO: Create skills model
        blank=True,
    )

    project = models.ForeignKey(  # The project of the member, OneToMany relationship
        'projects.Project',  # TODO: Create Project model
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='pr_members'
    )

    manager_id = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='children'
    )

    workhours = models.ForeignKey(
        'WorkHours',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='wh_members'
    )

    on_holidays_till = models.DateField(
        blank=True, null=True
    )

    @property
    def on_holidays(self) -> bool:
        return False if self.on_holidays_till is None else True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class WorkHours(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    timezone = TimeZoneField()  # works with pytz

    def __str__(self):
        return f'Start: {self.start}, End: {self.end}, Timezone: {self.timezone}'
