from django.shortcuts import render
from rest_framework import viewsets

from skills.models import Skill
from skills.serializers import SkillSerializer


class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer