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
        fields.ExtStringField('Breed',
                searchable=1,
                required=1,
                widget=StringWidget(
                    visible={'view': 'visible', 'edit': 'visible'},
                    label=_('Breed'),
                ),
        ),
        fields.ExtStringField('CoatColour',
                searchable=1,
                required=0,
                widget=StringWidget(
                    visible={'view': 'visible', 'edit': 'visible'},
                    label=_('Coat Colour'),
                ),
        ),
        fields.ExtStringField('Transponder',
                searchable=1,
                required=0,
                widget=StringWidget(
                    description="Implanted transponder ID",
                    visible={'view': 'visible', 'edit': 'visible'},
                    label=_('Transponder'),
                ),
        ),
        fields.ExtStringField('UELN',
                searchable=1,
                required=0,
                widget=StringWidget(
                    description="Universal Equine Life Number",
                    visible={'view': 'visible', 'edit': 'visible'},
                    label=_('UELN'),
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
        schema['PatientID'].widget.label = _("Specimen ID")
        schema['Middlename'].widget.visible = False
        schema['Salutation'].widget.visible = False
        schema['Middleinitial'].widget.visible = False
        schema['ClientPatientID'].widget.label = _("Client Specimen ID")
        schema['PrimaryReferrer'].widget.label = _("Veterinary Center")
        schema['PatientIdentifiers'].widget.description = _("Specimen additional identifiers")
        schema['TreatmentHistory'].widget.description = _("A list of specimen treatments and drugs administered.")

        schema['Allergies'].widget.description = _("Known Specimen allergies to keep information that can aid drug"
                                                   " reaction interpretation")
        schema['ImmunizationHistory'].widget.description = _("A list of immunizations administered to the specimen.")
        schema['TravelHistory'].widget.description = _("A list of places visited by the specimen.")
        schema['ChronicConditions'].widget.description = _("Specimen's past medical history.")
        schema['Ethnicity'].widget.visible = False
        schema['Citizenship'].widget.visible = False
        schema['MothersName'].widget.visible = False
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

