# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>

from django.http import HttpResponseRedirect
from django.views.generic.base import View

import requests
from requests.exceptions import RequestException
from settings import FRONT_HOST_URL


class MediaTypeDelete(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        try:
            requests.delete(
                FRONT_HOST_URL + '/api/mediatype/' + str(id)
                )
            return HttpResponseRedirect('/mediatype/')

        except RequestException:
            return HttpResponseRedirect('/mediatype/')
