# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Cooperative Artefacts <artefacts.lle@gmail.com>

"""
Ext_MediaCollection tests
"""

import factory
import pytest
import sys

from django.forms.models import model_to_dict
from django.core.management import call_command
from django.core.urlresolvers import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


from .factories.extMediaCollection import ExtMediaCollectionFactory
from .factories.MediaCollection import MediacollectionFactory
from ..models.ext_media_collection import ExtMediaCollection
from telemeta.models.collection import MediaCollection


# Expected structure for Mediacollection objects
# FIXIT ----
# EXTMEDIACOLLECTION_STRUCTURE = [
#     ('id', int),
#     ('media_collection', dict),
#     ('location', []),
#     ('location_details', str),
#     ('cultural_area', str),
#     ('language_iso', []),
#     ('language', str),
#     ('collectors', []),
#     ('informers', []),
#     ('publishers', [])
# ]

EXTMEDIACOLLECTION_STRUCTURE = [
    ('id', int),
    ('media_collection', dict),
    ('location_details', str),
    ('cultural_area', str),
    ('language', str),
]

# Expected keys for MODEL objects
EXTMEDIACOLLECTION_FIELDS = sorted(
    [item[0] for item in EXTMEDIACOLLECTION_STRUCTURE])


@pytest.mark.django_db
class TestExtMediacollectionList(APITestCase):
    """
    This class manage all ExtMediacollection tests
    """

    def setUp(self):
        """
        Run needed commands to have a fully working project
        """

        call_command('telemeta-setup-enumerations')

        # ExtMediaCollectionFactory.create_batch(6)
        MediacollectionFactory.create_batch(6)

    def test_can_get_extMediaCollection_list(self):
        """
        Ensure ExtMediacollection objects exists
        """
        url = reverse('MediaCollection-list')

        # ORM side
        ExtMediaCollections = ExtMediaCollection.objects.all()
        self.assertEqual(len(ExtMediaCollections), 6)

        # API side
        response = self.client.get(url)

        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    @parameterized.expand(EXTMEDIACOLLECTION_STRUCTURE)
    def test_has_valid_extMediaCollection_values(
            self, attribute, attribute_type):
        """
        Ensure ExtMediacollection objects have valid values
        """

        url = reverse('ExtMediaCollection-list')
        response = self.client.get(url)

        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for extMediaCollection in response.data:
            # Check only expected attributes returned
            self.assertEqual(
                sorted(extMediaCollection.keys()), EXTMEDIACOLLECTION_FIELDS)

            # Ensure type of each attribute
            if attribute_type == str:
                if sys.version_info.major == 2:
                    self.assertIsInstance(
                        extMediaCollection[attribute], basestring)
                else:
                    self.assertIsInstance(extMediaCollection[attribute], str)
            else:
                self.assertIsInstance(
                    extMediaCollection[attribute], attribute_type)
            self.assertIsNot(extMediaCollection[attribute], '')

    def test_get_an_extMediaCollection(self):
        """
        Ensure we can get an Mediacollection objects
        using an existing id
        """

        item = ExtMediaCollection.objects.first()
        url = reverse('ExtMediaCollection-detail',
                      kwargs={'pk': item.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)

    # def test_create_an_extMediaCollection(self):
    #     """
    #     Ensure we can create an ExtMediacollection object
    #     """
    #
    #     # Converting the factory to a dict
    #     data = factory.build(
    #         dict,
    #         FACTORY_CLASS=ExtMediaCollectionFactory)
    #     data['media_collection'] = data['media_collection'].__dict__
    #     self.assertEqual(data['media_collection']['comment'], {})
    #     # # related factory
    #     # data_c = factory.build(
    #     #     dict,
    #     #     FACTORY_CLASS=MediacollectionFactory)
    #     # # related objects
    #     # data_c['recording_context'] = str(data_c['recording_context'])
    #     # data_c['metadata_author'] = str(data_c['metadata_author'])
    #     # data_c['publisher'] = str(data_c['publisher'])
    #     # data_c['publisher_collection'] = str(data_c['publisher_collection'])
    #     # data_c['legal_rights'] = str(data_c['legal_rights'])
    #     # data_c['acquisition_mode'] = str(data_c['acquisition_mode'])
    #     # data_c['copy_type'] = str(data_c['copy_type'])
    #     # data_c['publishing_status'] = str(data_c['publishing_status'])
    #     # data_c['status'] = str(data_c['status'])
    #     # data_c['metadata_writer'] = str(data_c['metadata_writer'])
    #     # data_c['media_type'] = str(data_c['media_type'])
    #     # data_c['original_format'] = str(data_c['original_format'])
    #     # data_c['physical_format'] = str(data_c['physical_format'])
    #     # data_c['ad_conversion'] = str(data_c['ad_conversion'])
    #     #
    #     # data['media_collection'] = data_c
    #
    #     url = reverse('ExtMediaCollection-list')
    #     response = self.client.post(url, data, format='json')
    #
    #     # Check only expected attributes returned
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIsInstance(response.data, dict)
    #     self.assertEqual(
    #         sorted(response.data.keys()),
    #         EXTMEDIACOLLECTION_FIELDS)
    #
    #     url = reverse(
    #         'ExtMediaCollection-detail',
    #         kwargs={'pk': response.data['id']}
    #     )
    #     response_get = self.client.get(url)
    #
    #     self.assertEqual(response_get.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response_get.data, dict)
    #
    #     item = ExtMediaCollection.objects.first()
    #     self.assertEqual(item.id, 1)

    def test_update_an_extMediaCollection(self):
        """
        Ensure we can update an Mediacollection object
        """

        item = ExtMediaCollection.objects.first()
        self.assertNotEqual(item.cultural_area, 'foobar_test_put')

        # Get existing object from API
        url_get = reverse(
            'ExtMediaCollection-detail',
            kwargs={'pk': item.id})
        data = self.client.get(url_get).data

        data['cultural_area'] = 'foobar_test_put'
        data['location_details'] = 'A'
        data['language'] = 'A'

        url = reverse(
            'ExtMediaCollection-detail',
            kwargs={'pk': item.id})
        response = self.client.put(url, data, format='json')

        # Ensure new name returned
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(
            sorted(response.data.keys()),
            EXTMEDIACOLLECTION_FIELDS)
        self.assertEqual(response.data['cultural_area'], 'foobar_test_put')

    def test_patch_an_extMediaCollection(self):
        """
        Ensure we can patch an ExtMediacollection object
        """

        item = ExtMediaCollection.objects.first()
        self.assertNotEqual(item.cultural_area, 'foobar_test_patch')

        data = {'cultural_area': 'foobar_test_patch'}
        url = reverse(
            'ExtMediaCollection-detail',
            kwargs={'pk': item.id})
        response = self.client.patch(url, data, format='json')

        # Ensure new name returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(
            sorted(response.data.keys()),
            EXTMEDIACOLLECTION_FIELDS)
        self.assertEqual(
            response.data['cultural_area'], 'foobar_test_patch')

    def test_delete_an_extMediaCollection(self):
        """
        Ensure we can delete an ExtMediacollection object
        """

        item = ExtMediaCollection.objects.first()

        # Delete this object
        url = reverse(
            'ExtMediaCollection-detail',
            kwargs={'pk': item.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure ExtMediacollection removed
        url_get = reverse(
            'ExtMediaCollection-detail',
            kwargs={'pk': item.id})
        response_get = self.client.get(url_get)
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)