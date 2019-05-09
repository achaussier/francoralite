# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>


from django.db import models
from django.utils.translation import ugettext_lazy as _

# Add nested/related tables
from .item import Item
from .dance import Dance


class ItemDance(models.Model):
    # Description of the table
    "Relation between Item an Dance"

    # List of the fields
    dance = models.ForeignKey(Dance, verbose_name=_(
        'Fonction'))
    item = models.ForeignKey(Item, verbose_name=_('Item'))

    class Meta:
        app_label = 'telemeta_api'
        db_table = 'api_item_dance'
        verbose_name_plural = _('item_dances')
        ordering = []