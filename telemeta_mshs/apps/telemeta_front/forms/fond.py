# -*- coding: utf-8 -*-
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luc LEGER / Coopérative ARTEFACTS <artefacts.lle@gmail.com>

from django import forms
from django.utils.translation import ugettext_lazy as _
from .core import Core


class FondForm(forms.Form):
    title = forms.CharField(label=_(u'Titre'), max_length=255, required=True)
    code = forms.CharField(label=_(u'Cote du fonds'),
                           widget=forms.TextInput(
                               attrs={
                                    'data-mask': 'aaaa_aaa',
                                    'style': 'text-transform:uppercase;'
                                }
                           ),
                           max_length=16, required=True)
    descriptions = forms.CharField(label=_(u'Description'),
                                   widget=forms.Textarea, required=False)
    conservation_site = forms.CharField(
        label=_(u'Lieu de conservation original'),
        max_length=255, required=True)
    comment = forms.CharField(label=_(u'Commentaires'),
                              widget=forms.Textarea,
                              required=False)

    def __init__(self, *args, **kwargs):
        super(FondForm, self).__init__(*args, **kwargs)

        PUBLIC_ACCESS_CHOICES = (
            ('none', _(u'Aucun')),
            ('metadata', _(u'Meta-données')),
            ('partial', _(u'Partiel')),
            ('full', _(u'Complet'))
            )

        self.fields['public_access'] = forms.ChoiceField(
            label=_(u'Type d\'accès'),
            choices=PUBLIC_ACCESS_CHOICES,
            initial="metadata",
            required=True)

        self.fields['institution'] = forms.ChoiceField(
            label=_(u'Institution partenaire'),
            choices=Core.get_choices(
                entity="institution", label_field="name"),
            required=True)

        self.fields['acquisition_mode'] = forms.ChoiceField(
            label=_(u'Mode d\'acquisition'),
            choices=Core.get_choices(
                entity="acquisitionmode", label_field="value"),
            required=False)
