from bika.lims.exportimport.dataimport import SetupDataSetList as SDL
from bika.lims.interfaces import ISetupDataSetList
from zope.interface import implements



class SetupDataSetList(SDL):

    implements(ISetupDataSetList)

    def __call__(self):
        return SDL.__call__(self, projectname="bika.veterinary")
