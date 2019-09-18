from django.db.models import Q
from django.utils.datetime_safe import datetime
from django_filters import rest_framework as filters

from members.models import Member


class MembersFilter(filters.FilterSet):
    skills = filters.BaseInFilter(field_name='skills__name')
    holidays = filters.BooleanFilter(method='filter_is_on_holidays')
    is_working = filters.BooleanFilter(method='filter_is_working')

    class Meta:
        model = Member
        fields = (
            'skills',
            'project',
            'holidays',
            'is_working',
        )

    def filter_is_on_holidays(self, queryset, name, value):
        if value:
            return queryset.filter(Q(on_holidays_till__isnull=False) | Q(on_holidays_till__gt=datetime.now()))
        return queryset.filter(Q(on_holidays_till__isnull=True) | Q(on_holidays_till__lt=datetime.now()))


    def filter_is_working(self, queryset, name, value):
        if value:
            return queryset.filter(Q(workhours__start__lt=datetime.now()) & Q(workhours__end__gt=datetime.now()))

        return queryset.filter(Q(workhours__start__gt=datetime.now()) | Q(workhours__end__lt=datetime.now()))
