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
            if not row.get('Firstname', None) or not row.get('VeterinaryCenter', None):
                continue
            pc = getToolByName(self.context, 'portal_catalog')
            veterinarycenter = pc(portal_type='Client', Title=row.get('VeterinaryCenter', ''))
            if len(veterinarycenter) == 0:
                raise IndexError("Veterinary Center invalid: '%s'" % row.get('VeterinaryCenter', 'VeterinaryCenter'))

            veterinarycenter = veterinarycenter[0].getObject()
            _id = folder.invokeFactory('Patient', id=tmpID())
            obj = folder[_id]
            obj.unmarkCreationFlag()
            renameAfterCreation(obj)
            Fullname = (row.get('Firstname', '') + " " + row.get('Surname', '')).strip()
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


class Methods(WorksheetImporter):

    def Import(self):
        folder = self.context.methods
        for row in self.get_rows(3):
            if row.get('title', None):
                obj = _createObjectByType("Method", folder, tmpID())

                obj.edit(
                    title=row['title'],
                    description=row.get('description', ''),
                    Instructions=row.get('Instructions', ''),
                    MethodID=row.get('MethodID', ''),
                    Accredited=row.get('Accredited', True),
                    )
                # Obtain all created methods
                catalog = getToolByName(self.context, 'portal_catalog')
                methods_brains = catalog.searchResults({'portal_type': 'Method'})
                # If a the new method has the same MethodID as a created method, remove MethodID value.
                for methods in methods_brains:
                    if methods.getObject().get('MethodID', '') != '' and methods.getObject.get('MethodID', '') == obj['MethodID']:
                        obj.edit(MethodID='')

                if row.get('MethodDocument', None):
                    path = resource_filename(
                        self.dataset_project,
                        "setupdata/%s/%s" % (self.dataset_name,
                                             row['MethodDocument'])
                    )
                    file_data = open(path, "rb").read()
                    obj.setMethodDocument(file_data)

                obj.unmarkCreationFlag()
                renameAfterCreation(obj)
