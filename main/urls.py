from rest_framework_nested import routers
from pprint import pprint
from .views import CategoryViewSet, LocationViewSet, ReviewsViewSet, SubCategoryViewSet

router = routers.DefaultRouter()

# Parent routers
router.register('categories', CategoryViewSet, basename='çollections')
router.register('location', LocationViewSet, basename='location')
# router.register('gofers', LocationViewSet, basename='gofer')
# router.register('vendors', LocationViewSet, basename='gofer')
# router.register('vendors', LocationViewSet, basename='gofer')


# Child routers
category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('subcategory', SubCategoryViewSet, basename='category_subcategory')




urlpatterns = router.urls + category_router.urls

