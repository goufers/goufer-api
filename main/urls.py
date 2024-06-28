from rest_framework_nested import routers
from user.errand_boy_views import ErrandBoyViewset
from user.vendor_views import VendorViewSet
from pprint import pprint

from user.views import GoferViewset
from .views import CategoryViewSet, ErrandBoyDocumentViewSet, GoferDocumentViewSet, LocationViewSet, MessagePosterViewSet, ReviewsViewSet, SubCategoryViewSet, VendorDocumentViewSet

router = routers.DefaultRouter()

# Parent routers
router.register('categories', CategoryViewSet, basename='çollections')
router.register('location', LocationViewSet, basename='location')
router.register('vendors', VendorViewSet, basename='vendor')
router.register('gofers', GoferViewset, basename='gofer')
router.register('errand-boys', ErrandBoyViewset, basename='errand-boy')
router.register('message-posters', MessagePosterViewSet, basename='message-poster')



# Child routers
category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('subcategory', SubCategoryViewSet, basename='category_subcategory')

vendor_router = routers.NestedDefaultRouter(router, 'vendors', lookup='vendor')
vendor_router.register('document', VendorDocumentViewSet, basename='vendor_document')

errand_boy_router = routers.NestedDefaultRouter(router, 'errand-boys', lookup='errandboy')
vendor_router.register('document', ErrandBoyDocumentViewSet, basename='errandboy_document')

gofer_router = routers.NestedDefaultRouter(router, 'gofers', lookup='gofer')
gofer_router.register('document', GoferDocumentViewSet, basename='gofer_document')


urlpatterns = router.urls + category_router.urls + vendor_router.urls + errand_boy_router.urls + gofer_router.urls
