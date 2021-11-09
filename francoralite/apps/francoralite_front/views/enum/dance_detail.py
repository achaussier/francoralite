# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>


from francoralite.apps.francoralite_front.francoralite_template_view import FrancoraliteTemplateView
from francoralite.apps.francoralite_front.forms.dance import DanceForm
import francoralite.apps.francoralite_front.tools as tools


class DanceDetail(FrancoraliteTemplateView):
    template_name = "../templates/enum/dance-detail.html"

    def get_context_data(self, **kwargs):
        try:
            context = super(DanceDetail, self).get_context_data(**kwargs)
            context['dance'] = tools.request_api(
                '/api/dance/' + context['id'])
            context['form'] = DanceForm()

        except Exception as err:
            context['dance'] = {}
            context['error'] = err
            context['form'] = DanceForm()
        return context
