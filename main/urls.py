from rest_framework_nested import routers
from user.errand_boy_views import ErrandBoyViewset
from user.vendor_views import VendorViewSet
from user.views import BookingViewSet, GoferViewset, MediaViewset, ScheduleViewSet
from .views import CategoryViewSet, DocumentViewSet, LocationViewSet, AddressViewSet, ReviewsViewSet, SubCategoryViewSet

router = routers.DefaultRouter()

# Parent routers
router.register('categories', CategoryViewSet, basename='çollections')
router.register('location', LocationViewSet, basename='location')
router.register('vendors', VendorViewSet, basename='vendor')
router.register('gofers', GoferViewset, basename='gofer')
router.register('errand-boys', ErrandBoyViewset, basename='errand-boy')
router.register('documents', DocumentViewSet, basename='document')
router.register('addresses', AddressViewSet, basename='address')
router.register('bookings', BookingViewSet, basename='booking')



# Child routers
category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('subcategory', SubCategoryViewSet, basename='category_subcategory')

gofer_router = routers.NestedDefaultRouter(router, 'gofers', lookup='gofer')
gofer_router.register('reviews', ReviewsViewSet, basename='gofer_reviews')

vendor_router = routers.NestedDefaultRouter(router, 'vendors', lookup='vendor')
vendor_router.register('media', MediaViewset, basename='vendor_media')


urlpatterns = router.urls + category_router.urls + gofer_router.urls + vendor_router.urls
