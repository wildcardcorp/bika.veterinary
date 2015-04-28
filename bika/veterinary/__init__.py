# Defining a Message Factory for when this product is internationalized.
from zope.i18nmessageid import MessageFactory
bikaMessageFactory = MessageFactory('bika.veterinary')

# we import the configuration module, in order to have access to the variables it contains
from bika.veterinary import config

import logging
logger = logging.getLogger('Bika Veterinary')

# importing some useful stuff from the Archetypes API
from Products.Archetypes.atapi import process_types, listTypes
from Products.CMFCore import utils

# We also need to define tpermissions for the content types
from bika.veterinary.permissions import *

# We import everything that is defined in the content sub-package
# from content.breeder import Breeder


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    # It generates the content types, the constructors and the Factory-based
    # Type Informations required to make your types work with the CMF
    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    # content init and registers your types in the CMF
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: Add %s" % (config.PROJECTNAME, atype.portal_type)
        perm = config.ADD_CONTENT_PERMISSIONS.get(atype.portal_type, config.ADD_CONTENT_PERMISSION)
        utils.ContentInit(kind,
                          content_types      = (atype,),
                          permission         = perm,
                          extra_constructors = (constructor,),
                          fti                = ftis,
                          ).initialize(context)

