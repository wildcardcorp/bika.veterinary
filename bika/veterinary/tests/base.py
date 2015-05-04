from bika.lims.tests.base import BikaFunctionalTestCase
from bika.veterinary.testing import VETERINARY_FUNCTIONAL_TESTING



class BikaVeterinaryFunctionalTestCase(BikaFunctionalTestCase):
    """
    All veterinary tests will inheritance from this class. This class is inheritance from bika.lims.tests.base.py
    but you can override a method from the class to suit your needs.

    The class contains methods useful to use inside test as a way to setup, instructions after setup, getting data, ...
    """
    layer = VETERINARY_FUNCTIONAL_TESTING

