""" Bika setup handlers. """

from Products.CMFCore.utils import getToolByName
from bika.veterinary import logger


class Empty:
    pass


class BikaVeterinaryGenerator:
    """ Setup Bika site structure """
    def setupCatalogs(self, portal):

        def addIndex(cat, *args):
            try:
                cat.addIndex(*args)
            except:
                logger.warning("Could not create index %s in catalog %s" %
                               (args, cat))

        def addColumn(cat, col):
            try:
                cat.addColumn(col)
            except:
                logger.warning("Could not create metadata %s in catalog %s" %
                               (col, cat))

        # bika_catalog
        bc = getToolByName(portal, 'bika_catalog', None)
        if bc == None:
            logger.warning('Could not find the bika_catalog tool.')
            return

        bsc = getToolByName(portal, 'bika_catalog', None)
        if bsc is None:
            logger.warning('Could not find the bika_catalog tool.')
            return
        # Add indexes and metadata colums here

        bsc = getToolByName(portal, 'bika_setup_catalog', None)
        if bsc is None:
            logger.warning('Could not find the bika_setup_catalog tool.')
            return
        # Add indexes and metadata colums here

        bsc = getToolByName(portal, 'bika_analysis_catalog', None)
        if bsc is None:
            logger.warning('Could not find the bika_analysis_catalog tool.')
            return
        # Add indexes and metadata colums here


def removeHealthEthnicities(portal):
    """
    Removing health ethnicities since they are focused on people instead of animals
    """
    # Getting all ethnicities
    bika_setup = portal._getOb('bika_setup')
    folder = bika_setup.bika_ethnicities
    ids = folder.keys()
    if len(ids) > 0:
        # manage_delObject will mutate the list
        ids = list(ids)
        folder.manage_delObjects(ids)
    logger.info("Health standard ethnicities removed")


def setupVeterinaryVarious(context):
    """ Setup Bika site structure """

    if context.readDataFile('bika.veterinary.txt') is None:
        return

    portal = context.getSite()

    gen = BikaVeterinaryGenerator()
    gen.setupCatalogs(portal)
    removeHealthEthnicities(portal)
