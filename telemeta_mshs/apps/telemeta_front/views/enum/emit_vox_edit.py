# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>


from django.views.generic.edit import FormView
from rest_framework import status
import requests
from settings import FRONT_HOST_URL
from telemeta_front.forms.emit_vox import EmitVoxForm
from django.shortcuts import render
import telemeta_front.tools as tools


class EmitVoxEdit(FormView):
    template_name = "../templates/enum/emit_vox-add.html"
    form_class = EmitVoxForm
    success_url = '/emit_vox/'

    def get_context_data(self, **kwargs):
        context = super(EmitVoxEdit, self).get_context_data(**kwargs)

        id = kwargs.get('id')
        # Obtain values of the record
        response = requests.get(
            FRONT_HOST_URL + '/api/emit_vox/' + str(id))
        if response.status_code == status.HTTP_200_OK:
            context['emit_vox'] = response.json
        return context

    def get(self, request, *args, **kwargs):

        id = kwargs.get('id')

        # Obtain values of the record
        emit_vox = requests.get(
            FRONT_HOST_URL + '/api/emit_vox/' + str(id))
        form = EmitVoxForm(initial=emit_vox.json())

        return render(request,
                      '../templates/enum/emit_vox-add.html',
                      {'form': form, 'id': id})

    def post(self, request, *args, **kwargs):
        return tools.patch('emit_vox', EmitVoxForm, request, *args, **kwargs)
