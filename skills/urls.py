from rest_framework.routers import SimpleRouter
from skills import views

router = SimpleRouter()
router.register(r'skills', views.SkillsViewSet, basename='skills')

urlpatterns = router.urls
urlpatterns += []