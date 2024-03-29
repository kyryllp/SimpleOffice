from django.utils import six
from rest_framework import serializers

from members.models import WorkHours, Member

from skills.serializers import SkillSerializer
from projects.serializers import ProjectSerializer


class WorkHoursSerializer(serializers.ModelSerializer):
    timezone = serializers.SerializerMethodField()

    class Meta:
        model = WorkHours
        fields = (
            'id',
            'start',
            'end',
            'timezone',
        )

    def get_timezone(self, obj):
        """
        Method is created fro drf to be able to serialize timezone variable
        """
        return six.text_type(obj.timezone)


class MemberSerializer(serializers.ModelSerializer):
    # read_only = True is set to be able to create models via POST requests
    # because django doesn't support nested creation
    skills = SkillSerializer(many=True, read_only=True)
    project = ProjectSerializer(read_only=True)
    workhours = WorkHoursSerializer(read_only=True)

    class Meta:
        model = Member
        fields = (
            'id',
            'first_name',
            'last_name',
            'skills',
            'project',
            'manager_id',
            'workhours',
            'on_holidays_till',
        )