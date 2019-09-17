from django_filters import rest_framework as filters
from rest_framework import viewsets

from members.filters import MembersFilter
from members.models import WorkHours, Member
from members.serializers import WorkHoursSerializer, MemberSerializer


class WorkHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkHours.objects.all()
    serializer_class = WorkHoursSerializer


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = MembersFilter
