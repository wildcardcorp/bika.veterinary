# you have to ensure  your validators are registered before the object gets
# accessed the first time:
from bika.veterinary.validators import NIBvalidator, IBANvalidator
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.Widget import BooleanWidget, StringWidget
from bika.veterinary import bikaMessageFactory as _
from bika.lims import fields
from bika.lims.interfaces import ISupplier


class SupplierSchemaExtender(object):
    adapts(ISupplier)
    implements(ISchemaExtender)

    fields = [
        fields.ExtStringField('Website',
            searchable=1,
            required=0,
            widget=StringWidget(
                visible={'view': 'visible', 'edit': 'visible'},
                label=_('Website.'),
            ),
        ),
        fields.ExtStringField('NIB',
            searchable=1,
            schemata = 'Bank details',
            required=0,
            widget=StringWidget(
                visible={'view': 'visible', 'edit': 'visible'},
                label=_('NIB'),
            ),
            validators=('NIBvalidator'),
        ),
        fields.ExtStringField('IBN',
            searchable=1,
            schemata ='Bank details',
            required=0,
            widget=StringWidget(
                visible={'view': 'visible', 'edit': 'visible'},
                label=_('IBN'),
            ),
            validators=('IBANvalidator'),
        ),
        fields.ExtStringField('SWIFTcode',
            searchable=1,
            required=0,
            schemata ='Bank details',
            widget=StringWidget(
                visible={'view': 'visible', 'edit': 'visible'},
                label=_('SWIFT code.'),
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
