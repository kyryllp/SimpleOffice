from rest_framework.routers import SimpleRouter
from projects import views

router = SimpleRouter()
router.register(r'projects', views.ProjectsViewSet, basename='projects')

urlpatterns = router.urls
urlpatterns += []