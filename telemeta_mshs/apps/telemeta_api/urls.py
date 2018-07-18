from rest_framework_nested import routers
from .views import (
    authority,
    coupe,
    institution,
    MediaCollection,
    ExtMediaCollection,
    collectioncollectors,
    collection_informer,
    collection_publisher,
    collection_location,
    collection_language,
    location,
    language,
    )

router = routers.SimpleRouter()
router.register(r'institution',
                institution.InstitutionViewSet, base_name='institution')
router.register(r'coupe', coupe.CoupeViewSet, base_name='coupe')
router.register(r'authority',
                authority.AuthorityViewSet, base_name='authority')
router.register(r'collection',
                MediaCollection.MediacollectionViewSet,
                base_name='MediaCollection')
router.register(r'extcollection',
                ExtMediaCollection.ExtMediacollectionViewSet,
                base_name='ExtMediaCollection')
router.register(r'location',
                location.LocationViewSet,
                base_name='location')
router.register(r'language',
                language.LanguageViewSet,
                base_name='language')


# Nested routers
router.register(
    r'extcollections', ExtMediaCollection.ExtMediacollectionViewSet)
ExtMediaCollection_router = routers.NestedSimpleRouter(
    router, r'extcollections', lookup='extcollection')
ExtMediaCollection_router.register(
    r'collectors', collectioncollectors.CollectionCollectorsViewSet)
ExtMediaCollection_router.register(
    r'informer', collection_informer.CollectionInformerViewSet)
ExtMediaCollection_router.register(
    r'publisher', collection_publisher.CollectionPublisherViewSet)
ExtMediaCollection_router.register(
    r'location', collection_location.CollectionLocationViewSet)
ExtMediaCollection_router.register(
    r'language', collection_language.CollectionLanguageViewSet)
