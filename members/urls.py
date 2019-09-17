from django.urls import path
from rest_framework.routers import SimpleRouter
from members import views

router = SimpleRouter()
router.register(r'workhours', views.WorkHoursViewSet, basename='workhours')
router.register(r'members', views.MembersViewSet, basename='members')

urlpatterns = router.urls
urlpatterns += [
    # path('members/get_by_availability/', views.MembersByAvailability.as_view(), ),
]