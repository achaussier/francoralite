# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>

from django.views.generic.base import TemplateView
from rest_framework import status
import requests

from settings import FRONT_HOST_URL
from telemeta_front.forms.location import LocationForm


class LocationDetail(TemplateView):
    template_name = "../templates/location-detail.html"

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)

        # Obtain values of the record
        response = requests.get(
            FRONT_HOST_URL + '/api/location/' + context['id'])
        if response.status_code == status.HTTP_200_OK:
            context['location'] = response.json
            context['form'] = LocationForm
        return context