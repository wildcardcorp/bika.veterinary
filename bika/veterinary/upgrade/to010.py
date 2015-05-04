from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName


def upgrade(tool):
    """ Upgrade steps to 1.0
    """
    portal = aq_parent(aq_inner(tool))

    # Re-run conf files where changes have been made.
    setup = portal.portal_setup
    setup.runImportStepFromProfile('profile-bika.veterinary:default', 'jsregistry')

    return True
