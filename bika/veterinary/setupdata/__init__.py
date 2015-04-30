from pkg_resources import resource_filename
from Products.CMFCore.utils import getToolByName
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
            if not row['Firstname'] or not row['VeterinaryCenter']:
                continue
            pc = getToolByName(self.context, 'portal_catalog')
            veterinarycenter = pc(portal_type='Client', Title=row['VeterinaryCenter'])
            if len(veterinarycenter) == 0:
                raise IndexError("Veterinary Center invalid: '%s'" % row['VeterinaryCenter'])

            veterinarycenter = veterinarycenter[0].getObject()
            _id = folder.invokeFactory('Patient', id=tmpID())
            obj = folder[_id]
            obj.unmarkCreationFlag()
            renameAfterCreation(obj)
            Fullname = (row['Firstname'] + " " + row.get('Surname', '')).strip()
            obj.edit(PatientID=row.get('PatientID'),
                     title=Fullname,
                     ClientPatientID=row.get('ClientPatientID', ''),
                     Firstname=row.get('Firstname', ''),
                     Surname=row.get('Surname', ''),
                     PrimaryReferrer=veterinarycenter.UID(),
                     Gender=row.get('Gender', 'dk'),
                     Age=row.get('Age', ''),
                     BirthDate=row.get('BirthDate', ''),
                     BirthDateEstimated =self.to_bool(row.get('BirthDateEstimated', 'False')),
                     BirthPlace=row.get('BirthPlace', ''),
                     Breed=row.get('Breed', ''),
                     CoatColour=row.get('CoatColour', ''),
                     UEALN=row.get('UELN', ''),
                     Breeder=row.get('Breeder', '')
                     )
            self.fill_contactfields(row, obj)
            self.fill_addressfields(row, obj)
            if 'Photo' in row and row['Photo']:
                try:
                    path = resource_filename("bika.lims",
                                             "setupdata/%s/%s" \
                                             % (self.dataset_name, row['Photo']))
                    file_data = open(path, "rb").read()
                    obj.setPhoto(file_data)
                except:
                    logger.error("Unable to load Photo %s"%row['Photo'])

            if 'Feature' in row and row['Feature']:
                try:
                    path = resource_filename("bika.lims",
                                             "setupdata/%s/%s" \
                                             % (self.dataset_name, row['Feature']))
                    file_data = open(path, "rb").read()
                    obj.setFeature(file_data)
                except:
                    logger.error("Unable to load Feature %s"%row['Feature'])

            obj.unmarkCreationFlag()
            transaction.savepoint(optimistic=True)
            if row.get('PatientID'):
                # To maintain the patient spreadsheet's IDs, we cannot do a 'renameaftercreation()'
                obj.aq_inner.aq_parent.manage_renameObject(obj.id, row.get('PatientID'))
            else:
                renameAfterCreation(obj)
