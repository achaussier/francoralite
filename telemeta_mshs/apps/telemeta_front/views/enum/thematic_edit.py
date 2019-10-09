# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>


from django.views.generic.edit import FormView
from rest_framework import status
import requests
from settings import FRONT_HOST_URL
from telemeta_front.forms.thematic import ThematicForm
from django.shortcuts import render
import telemeta_front.tools as tools


class ThematicEdit(FormView):
    template_name = "../templates/enum/thematic-add.html"
    form_class = ThematicForm
    success_url = '/thematic/'

    def get_context_data(self, **kwargs):
        context = super(ThematicEdit, self).get_context_data(**kwargs)

        id = kwargs.get('id')
        # Obtain values of the record
        response = requests.get(
            FRONT_HOST_URL + '/api/thematic/' + str(id))
        if response.status_code == status.HTTP_200_OK:
            context['thematic'] = response.json
        return context

    def get(self, request, *args, **kwargs):

        id = kwargs.get('id')

        # Obtain values of the record
        thematic = requests.get(
            FRONT_HOST_URL + '/api/thematic/' + str(id))
        form = ThematicForm(initial=thematic.json())

        return render(request,
                      '../templates/enum/thematic-add.html',
                      {'form': form, 'id': id})

    def post(self, request, *args, **kwargs):
        return tools.patch('thematic', ThematicForm, request, *args, **kwargs)
