from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, ISchemaModifier
from Products.Archetypes.Widget import BooleanWidget, StringWidget
from bika.veterinary import bikaMessageFactory as _
from bika.lims import fields
from bika.lims.interfaces import IMethod


class MethodSchemaExtender(object):
    adapts(IMethod)
    implements(IOrderableSchemaExtender)

    fields = [
        # Method ID should be unique, specified on MethodSchemaModifier
        fields.ExtStringField('MethodID',
            searchable=1,
            required=0,
            widget=StringWidget(
                visible={'view': 'visible', 'edit': 'visible'},
                label=_('Method ID'),
                description=_('Define an identifier code for the method. It must be unique.'),
            ),
        ),
        fields.ExtBooleanField('Accredited',
            schemata="default",
            default=True,
            widget=BooleanWidget(
                label=_("Accredited"),
                description=_("Check if the method has been accredited"))
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        schematas['default'] = ['id',
                                'title',
                                'MethodID',
                                'description',
                                'Instructions',
                                'MethodDocument',
                                '_Instruments',
                                '_AvailableInstruments',
                                'ManualEntryOfResults',
                                'ManualEntryOfResultsViewField',
                                'Calculation',
                                'Accredited'
                                ]
        return schematas

class MethodSchemaModifier(object):
    adapts(IMethod)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['MethodID'].validators = ('uniquefieldvalidator',)
        # Update the validation layer after change the validator in runtime
        schema['MethodID']._validationLayer()

        return schema
