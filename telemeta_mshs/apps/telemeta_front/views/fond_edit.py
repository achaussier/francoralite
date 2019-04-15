# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>

from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from rest_framework import status
import requests
from requests.exceptions import RequestException
from settings import FRONT_HOST_URL
from telemeta_front.forms.fond import FondForm
from django.shortcuts import render
import telemeta_front.tools as tools


class FondEdit(FormView):
    template_name = "../templates/fond-add.html"
    form_class = FondForm
    success_url = '/fond/'
    keycloak_scopes = {
            'GET': 'fond:view',
            'POST': 'fond:add',
            'PATCH': 'fond:update',
            'PUT': 'fond:update'}

    def get_context_data(self, **kwargs):
        try:
            context = super(FondEdit, self).get_context_data(**kwargs)
            id = kwargs.get('id')
            # Obtain values of the record
            context['fond'] = tools.request_api(
                '/api/fond/' + str(id))
        except Exception as err:
            context['fond'] = {}
            context['error'] = err.message
        return context

    def get(self, request, *args, **kwargs):

        id = kwargs.get('id')

        # Obtain values of the record
        fond = requests.get(
            FRONT_HOST_URL + '/api/fond/' + str(id))
        data = fond.json()
        data['institution'] = data['institution']['id']
        form = FondForm(initial=data)

        return render(request,
                      '../templates/fond-add.html',
                      {'form': form, 'id': id})

    def post(self, request, *args, **kwargs):

        form = FondForm(request.POST)
        id = kwargs.get('id')

        if form.is_valid():
            try:
                response = requests.patch(
                    FRONT_HOST_URL + '/api/fond/' + str(id) + '/',
                    data=form.cleaned_data
                )
                if(response.status_code != status.HTTP_200_OK):
                    return HttpResponseRedirect('/fond/edit/'
                                                + str(id))
                return HttpResponseRedirect('/fond/')

            except RequestException:
                return HttpResponseRedirect('/fond/edit/'
                                            + str(id))

        return HttpResponseRedirect('/fond/edit/'
                                    + str(id))
