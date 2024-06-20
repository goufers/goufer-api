from rest_framework_nested import routers
from .views import CategoryViewSet, DocumentViewSet, LocationViewSet, ReviewsViewSet, SubCategoryViewSet, GoferViewSet, ErrandViewSet

router = routers.DefaultRouter()

# Parent routers
router.register('categories', CategoryViewSet, basename='çollections')
router.register('documents', DocumentViewSet, basename='documents')
router.register('location', LocationViewSet, basename='location')
router.register('gofers', GoferViewSet, basename='gofer')


# Child routers
category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('subcategory', SubCategoryViewSet, basename='category_subcategory')


gofer_router = routers.NestedDefaultRouter(router, 'gofers', lookup='gofer')
gofer_router.register('reviews', ReviewsViewSet, basename='gofer_review')

gofer_router = routers.NestedDefaultRouter(router, 'gofers', lookup='gofers')
gofer_router.register('errands', ErrandViewSet, basename='gofers_errand')

urlpatterns = router.urls + category_router.urls + gofer_router.urls 

