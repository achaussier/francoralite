# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>

from django.db import models
from rest_framework import generics

from ..models.coupe import Coupe
from ..models.collection import Collection
from ..models.collection_location import CollectionLocation
from ..models.instrument import Instrument
from ..models.item import Item
from ..serializers.advanced_search import AdvancedSearchSerializer


class AdvancedSearchList(generics.ListAPIView):
    serializer_class = AdvancedSearchSerializer

    def get_queryset(self):

        # Initialize data from ORM (-> querysets)
        query_sets = [
            Collection.objects.all(),
            Item.objects.all(),
        ]

        # Filtering ----------------------------------------------------
        fields = (
            {
                'name': 'instrument',
                'sub_model': Instrument,
                'paths': (
                    'performancecollection__collection',
                    'performancecollection__itemperformance__item',
                ),
            }, {
                'name': 'location',
                'paths': (
                    'collectionlocation__location',
                    'collection__collectionlocation__location',
                ),
            }, {
                'name': 'dance',
                'paths': (
                    'collection__itemdance__dance',
                    'itemdance__dance',
                ),
            }, {
                'name': 'collector',
                'paths': (
                    'collectioncollectors__collector',
                    'itemcollector__collector',
                ),
            }, {
                'name': 'informer',
                'paths': (
                    'collectioninformer__informer',
                    'iteminformer__informer',
                ),
            }, {
                'name': 'coupe',
                'sub_model': Coupe,
                'paths': ('items__collection', 'items'),
            }, {
                'name': 'usefulness',
                'paths': (
                    'collection__itemusefulness__usefulness',
                    'itemusefulness__usefulness'
                ),
            }, {
                'name': 'thematic',
                'paths': (
                    'collection__itemthematic__thematic',
                    'itemthematic__thematic'
                ),
            }, {
                'name': 'domain_music',
                'paths': (
                    'collection__itemdomainmusic__domain_music',
                    'itemdomainmusic__domain_music'
                ),
            }, {
                'name': 'domain_song',
                'paths': (
                    'collection__itemdomainsong__domain_song',
                    'itemdomainsong__domain_song'
                ),
            }, {
                'name': 'domain_tale',
                'paths': (
                    'collection__itemdomaintale__domain_tale',
                    'itemdomaintale__domain_tale'
                ),
            }, {
                'name': 'domain_vocal',
                'paths': (
                    'collection__itemdomainvocal__domain_vocal',
                    'itemdomainvocal__domain_vocal'
                ),
            }, {
                'name': 'refrain',
                'paths': (None, 'refrain'),
                'lookups': 'icontains',
            }, {
                'name': 'incipit',
                'paths': (None, 'incipit'),
                'lookups': 'icontains',
            }, {
                'name': 'timbre',
                'paths': (None, 'timbre'),
                'lookups': 'icontains',
            }, {
                'name': 'timbre_ref',
                'paths': (None, 'timbre_ref'),
                'lookups': 'icontains',
            },
        )

        or_operators = self.request.query_params.getlist('or_operators', [])

        for field in fields:
            values = self.request.query_params.getlist(field['name'], [])

            if not values:
                continue

            paths = field['paths']
            sub_model = field.get('sub_model')
            lookups = field.get('lookups')

            if field['name'] in or_operators:
                # Filter : value OR value OR ...
                for index, path in enumerate(paths):
                    if path is None:
                        query_sets[index] = query_sets[index].none()
                    elif lookups:
                        if sub_model:
                            raise NotImplementedError
                        # Use many joins
                        path = '%s__%s' % (path, lookups)
                        sub_filter = models.Q()
                        for value in values:
                            sub_filter |= models.Q(**{path: value})
                        query_sets[index] = query_sets[index].filter(sub_filter)
                    elif sub_model is not None:
                        # Use a sub-query
                        query_sets[index] = query_sets[index].filter(
                            id__in=sub_model.objects.filter(
                                id__in=values).values_list(path))
                    else:
                        # Use joins
                        query_sets[index] = query_sets[index].filter(
                            **{'%s__in' % path: values})
            else:
                # Filter : value AND value AND ...
                for value in values:
                    for index, path in enumerate(paths):
                        if path is None:
                            query_sets[index] = query_sets[index].none()
                        elif sub_model is not None:
                            # Use a sub-query
                            if lookups:
                                raise NotImplementedError
                            query_sets[index] = query_sets[index].filter(
                                id__in=sub_model.objects.filter(
                                    id=value).values_list(path))
                        else:
                            # Use joins
                            if lookups:
                                path = '%s__%s' % (path, lookups)
                            query_sets[index] = query_sets[index].filter(
                                **{path: value})

        # Special dates filtering
        date_filter = models.Q()
        date_start = self.request.query_params.get('date_start', None)
        date_end = self.request.query_params.get('date_end', None)
        if date_start:
            date_filter &= models.Q(recorded_from_year__gte=date_start)
        if date_end:
            date_filter &= models.Q(recorded_to_year__lte=date_end)
        if date_filter:
            query_sets[0] = query_sets[0].filter(date_filter)
            query_sets[1] = query_sets[1].filter(
                collection__in=Collection.objects.filter(date_filter))
        # ---------------------------------------------------- end filtering
      
        # Collecting the locations
        collection_locations = CollectionLocation.objects.filter(collection__in=query_sets[0])
        query_sets.append(collection_locations)
        
        # Composing results
        all_results = [item for qs in query_sets for item in qs.distinct()]

        return all_results
