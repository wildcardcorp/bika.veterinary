from pkg_resources import resource_filename
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from bika.lims import logger
from bika.lims.exportimport.dataimport import SetupDataSetList as SDL
from bika.lims.exportimport.setupdata import WorksheetImporter
from bika.lims.interfaces import ISetupDataSetList
from bika.lims.idserver import renameAfterCreation
from bika.lims.utils import tmpID
from zope.interface import implements
import transaction


class SetupDataSetList(SDL):

    implements(ISetupDataSetList)

    def __call__(self):
        return SDL.__call__(self, projectname="bika.veterinary")


class Specimen(WorksheetImporter):

    def Import(self):
        folder = self.context.patients
        rows = self.get_rows(3)
        for row in rows:
            if not row.get('Firstname', None) or not row.get('Client', None):
                continue
            pc = getToolByName(self.context, 'portal_catalog')
            client = pc(portal_type='Client', Title=row.get('Client', ''))
            if len(client) == 0:
                raise IndexError("Client invalid: '%s'" % row.get('Client', 'Client'))

            client = client[0].getObject()
            _id = folder.invokeFactory('Patient', id=tmpID())
            obj = folder[_id]
            obj.unmarkCreationFlag()
            renameAfterCreation(obj)
            Fullname = (str(row.get('Firstname', '')) + " " + str(row.get('Surname', ''))).strip()
            identifiers = []
            if row.get('UELN', '') != '':
                identifiers.append({'IdentifierType': 'UEALN', 'Identifier': row.get('UELN', '')})
            if row.get('TransponderID', '') != '':
                identifiers.append({'IdentifierType': 'TransponderID', 'Identifier': row.get('TransponderID', '')})
            if row.get('NationalID', '') != '':
                identifiers.append({'IdentifierType': 'NationalID', 'Identifier': row.get('NationalID', '')})

            obj.edit(PatientID=row.get('PatientID'),
                     title=Fullname,
                     ClientPatientID=row.get('ClientPatientID', ''),
                     Firstname=row.get('Firstname', ''),
                     Surname=row.get('Surname', ''),
                     PrimaryReferrer=client.UID(),
                     Gender=row.get('Gender', 'dk'),
                     Age=row.get('Age', ''),
                     BirthDate=row.get('BirthDate', ''),
                     BirthDateEstimated =self.to_bool(row.get('BirthDateEstimated', 'False')),
                     BirthPlace=row.get('BirthPlace', ''),
                     MothersName=row.get('MothersName', ''),
                     FathersName=row.get('FathersName', ''),
                     Breed=row.get('Breed', ''),
                     CoatColour=row.get('CoatColour', ''),
                     Breeder=row.get('Breeder', ''),
                     PatientIdentifiers=identifiers
                     )
            self.fill_contactfields(row, obj)
            self.fill_addressfields(row, obj)
            if 'Photo' in row and row.get('Photo', None):
                try:
                    path = resource_filename("bika.lims",
                                             "setupdata/%s/%s" \
                                             % (self.dataset_name, row['Photo']))
                    file_data = open(path, "rb").read()
                    obj.setPhoto(file_data)
                except:
                    logger.error("Unable to load Photo %s"%row.get('Photo', 'Photo'))

            if 'Feature' in row and row.get('Feature', None):
                try:
                    path = resource_filename("bika.lims",
                                             "setupdata/%s/%s" \
                                             % (self.dataset_name, row.get('Feature', None)))
                    file_data = open(path, "rb").read()
                    obj.setFeature(file_data)
                except:
                    logger.error("Unable to load Feature %s"%row.get('Feature', 'Photo'))

            obj.unmarkCreationFlag()
            transaction.savepoint(optimistic=True)
            if row.get('PatientID'):
                # To maintain the patient spreadsheet's IDs, we cannot do a 'renameaftercreation()'
                obj.aq_inner.aq_parent.manage_renameObject(obj.id, row.get('PatientID'))
            else:
                renameAfterCreation(obj)
