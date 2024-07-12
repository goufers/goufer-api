from rest_framework_nested import routers
from user.errand_boy_views import ErrandBoyViewset
from user.vendor_views import VendorViewSet

from user.views import GoferViewset, MediaViewset
from .views import CategoryViewSet, DocumentViewSet, LocationViewSet, AddressViewSet, MessagePosterViewSet, ReviewsViewSet, SubCategoryViewSet

router = routers.DefaultRouter()

# Parent routers
router.register('categories', CategoryViewSet, basename='çollections')
router.register('location', LocationViewSet, basename='location')
router.register('vendors', VendorViewSet, basename='vendor')
router.register('gofers', GoferViewset, basename='gofer')
router.register('errand-boys', ErrandBoyViewset, basename='errand-boy')
router.register('documents', DocumentViewSet, basename='document')
router.register('message-posters', MessagePosterViewSet, basename='message-poster')
router.register('addresses', AddressViewSet, basename='address')



# Child routers
category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('subcategory', SubCategoryViewSet, basename='category_subcategory')

gofer_router = routers.NestedDefaultRouter(router, 'gofers', lookup='gofer')
category_router.register('reviews', ReviewsViewSet, basename='gofer_reviews')

vendor_router = routers.NestedDefaultRouter(router, 'vendors', lookup='vendor')

vendor_router.register('media', MediaViewset, basename='vendor_media')

urlpatterns = router.urls + category_router.urls + gofer_router.urls + vendor_router.urls
