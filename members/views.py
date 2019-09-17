from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from members.filters import MembersFilter
from members.models import WorkHours, Member
from members.serializers import WorkHoursSerializer, MemberSerializer
from projects.models import Project

from projects.serializers import ProjectIdSerializer


class WorkHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkHours.objects.all()
    serializer_class = WorkHoursSerializer


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = MembersFilter

    @action(detail=True, methods=['POST', ], serializer_class=ProjectIdSerializer)
    def assign_to_project(self, request, pk=None):
        member = get_object_or_404(Member, pk=pk)
        project = get_object_or_404(Project, pk=request.data['id'])

        serializer = MemberSerializer(member)

        if member.is_available:
            member.project = project
            member.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "Member can't be assigned to the project now"})
