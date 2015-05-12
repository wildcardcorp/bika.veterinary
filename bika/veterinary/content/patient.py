from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, ISchemaModifier
from Products.Archetypes.Widget import StringWidget
from bika.veterinary import bikaMessageFactory as _
from bika.lims import fields
from bika.health.interfaces import IPatient


class PatientSchemaExtender(object):
    adapts(IPatient)
    implements(ISchemaExtender)

    fields = [
        fields.ExtStringField('CoatColour',
                searchable=1,
                required=0,
                widget=StringWidget(
                    visible={'view': 'visible', 'edit': 'visible'},
                    label=_('Coat Colour'),
                ),
        ),
        fields.ExtStringField('Breeder',
                searchable=1,
                required=0,
                widget=StringWidget(
                    description="Name of breeder",
                    visible={'view': 'visible', 'edit': 'visible'},
                    label=_('Breeder'),
                ),
        ),

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class PatientSchemaModifier(object):
    adapts(IPatient)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['Middlename'].widget.visible = False
        schema['Salutation'].widget.visible = False
        schema['Middleinitial'].widget.visible = False
        schema['PrimaryReferrer'].widget.label = _("Client")
        # TODO on next health release, Ethnicity_Obj -> Ethnicity
        schema['Ethnicity_Obj'].widget.label = _('Breed')
        schema['Citizenship'].widget.visible = False
        schema['CivilStatus'].widget.visible = False
        schema['MenstrualStatus'].widget.visible = False
        schema['CivilStatus'].widget.visible = False
        schema['AllowResultsDistribution'].widget.visible = False
        schema['PatientAsGuarantor'].widget.visible = False
        schema['EmailAddress'].widget.visible = False
        schema['HomePhone'].widget.visible = False
        schema['MobilePhone'].widget.visible = False
        schema['BirthPlace'].schemata = 'default'
        schema['PhysicalAddress'].widget.visible = False
        schema['PostalAddress'].widget.visible = False
        schema['DefaultResultsDistribution'].widget.visible = False
        schema['PublicationPreferences'].widget.visible = False
        schema['PublicationAttachmentsPermitted'].widget.visible = False

        return schema

