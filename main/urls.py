from rest_framework_nested import routers
from .views import CategoryViewSet, DocumentViewSet, LocationViewSet, ReviewsViewSet, SubCategoryViewSet

router = routers.DefaultRouter()

# Parent routers
router.register('categories', CategoryViewSet, basename='çollections')
router.register('documents', DocumentViewSet, basename='documents')
router.register('location', LocationViewSet, basename='location')


# Child routers
category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('subcategory', SubCategoryViewSet, basename='category_subcategory')


urlpatterns = router.urls + category_router.urls