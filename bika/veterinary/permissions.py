"""All permissions are defined here.
They are also defined in permissions.zcml.
The two files must be kept in sync.

bika.veterinary.__init__ imports * from this file, so
bika.veterinary.PermName or bika.veterinary.permissions.PermName are
both valid.
"""
from bika.lims.permissions import *
from bika.health.permissions import *

# Add Permissions for specific types, if required
ADD_CONTENT_PERMISSIONS = {
}
