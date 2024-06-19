from rest_framework_nested import routers
from pprint import pprint
from .views import CategoryViewSet, ContractViewSet, DocumentViewSet, LocationViewSet, ReviewsViewSet, SubCategoryViewSet

router = routers.DefaultRouter()

# Parent routers
router.register('categories', CategoryViewSet, basename='çollections')
router.register('documents', DocumentViewSet, basename='documents')
router.register('location', LocationViewSet, basename='location')
router.register('gofers', LocationViewSet, basename='gofer')


# Child routers
category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('subcategory', SubCategoryViewSet, basename='category_subcategory')

gofer_router = routers.NestedDefaultRouter(router, 'gofers', lookup='gofer')
gofer_router.register('contract', ContractViewSet, basename='gofer_contract')


urlpatterns = router.urls + category_router.urls + gofer_router.urls

