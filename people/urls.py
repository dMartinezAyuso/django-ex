from .views import PeopleViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('people', PeopleViewSet, base_name='people')
urlpatterns = router.urls