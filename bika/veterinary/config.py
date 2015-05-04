from bika.health import bikaMessageFactory as _
# Displaylist is a data container we use when displaying pulldowns/radiobuttons/checkmarks with different choices
from Products.Archetypes.public import DisplayList

# Setting project name
PROJECTNAME = "bika.veterinary"

# Specifying the gender options using the DisplayList utility class that Archetypes has provided
# for exactly that purpose
GENDERS = DisplayList((
    ('male', _('Male')),
    ('female', _('Female')),
    ('dk', _("Don't Know")),
    ))
