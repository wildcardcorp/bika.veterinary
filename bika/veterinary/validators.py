from Products.validation.interfaces.IValidator import IValidator
from Products.validation import validation
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import to_utf8
import string

def _toIntList(numstr, acceptX=0):
    """
    Convert ans string to a list removing all invalid characters.
    Receive: a string as a number
    """
    res = []
    # Converting and removing invalid characters
    for i in numstr:
        if i in string.digits and i not in string.letters:
            res.append(int(i))

    # Converting control number into ISBN
    if acceptX and (numstr[-1] in 'Xx'):
        res.append(10)
    return res

def _sumLists(a, b):
    """
    Algorithm to check validity of NBI and NIF.
    Receives string with a umber to validate.
    """
    val = 0
    for i in map(lambda a, b: a * b, a, b):
        val += i
    return val


class NIBvalidator:
    """
    Validates if the introduced NIB is correct.
    """

    implements(IValidator)
    name = "NIBvalidator"

    def __call__(self, value, *args, **kwargs):
        """
        Check the NIB number
        value:: string with NIB.
        """
        instance = kwargs['instance']
        translate = getToolByName(instance, 'translation_service').translate
        LEN_NIB = 21
        table = ( 73, 17, 89, 38, 62, 45, 53, 15, 50,
                5, 49, 34, 81, 76, 27, 90, 9, 30, 3 )

        # convert to entire numbers list
        nib = _toIntList(value)

        # checking the length of the number
        if len(nib) != LEN_NIB:
            msg = _('Incorrect NIB number: %s' % value)
            return to_utf8(translate(msg))
        # last numbers algorithm validator
        return nib[-2] * 10 + nib[-1] == 98 - _sumLists(table, nib[:-2]) % 97

validation.register(NIBvalidator())


class IBANvalidator:
    """
    Validates if the introduced NIB is correct.
    """

    implements(IValidator)
    name = "IBANvalidator"

    def __call__(self, value, *args, **kwargs):
        instance = kwargs['instance']
        translate = getToolByName(instance, 'translation_service').translate

        # remove spaces from formatted
        IBAN = ''.join(c for c in value if c.isalnum())

        IBAN = IBAN[4:] + IBAN[:4]
        country = IBAN[-4:-2]

        if country not in country_dic:
            msg = _('Unknown IBAN country %s' % country)
            return to_utf8(translate(msg))

        length_c, name_c = country_dic[country]

        if len(IBAN) != length_c:
            diff = len(IBAN) - length_c
            msg = _('Wrong IBAN length by %s: %s' % (('short by %i' % -diff) if diff < 0 else
            ('too long by %i' % diff), value))
            return to_utf8(translate(msg))
        # Validating procedure
        elif int("".join(str(letter_dic[x]) for x in IBAN)) % 97 != 1:
            msg = _('Incorrect IBAN number: %s' % value)
            return to_utf8(translate(msg))

        else:
            # Accepted:
            return True

validation.register(IBANvalidator())

# Utility to check the integrity of an IBAN bank account No.
# based on https://www.daniweb.com/software-development/python/code/382069/iban-number-check-refreshed
# Dictionaries - Refer to ISO 7064 mod 97-10
letter_dic={"A":10, "B":11, "C":12, "D":13, "E":14, "F":15, "G":16, "H":17, "I":18, "J":19, "K":20, "L":21, "M":22,
            "N":23, "O":24, "P":25, "Q":26, "R":27, "S":28, "T":29, "U":30, "V":31, "W":32, "X":33, "Y":34, "Z":35,
            "0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}

# ISO 3166-1 alpha-2 country code
country_dic = {
    "AL": [28,"Albania"],
    "AD": [24,"Andorra"],
    "AT": [20,"Austria"],
    "BE": [16,"Belgium"],
    "BA": [20,"Bosnia"],
    "BG": [22,"Bulgaria"],
    "HR": [21,"Croatia"],
    "CY": [28,"Cyprus"],
    "CZ": [24,"Czech Republic"],
    "DK": [18,"Denmark"],
    "EE": [20,"Estonia"],
    "FO": [18,"Faroe Islands"],
    "FI": [18,"Finland"],
    "FR": [27,"France"],
    "DE": [22,"Germany"],
    "GI": [23,"Gibraltar"],
    "GR": [27,"Greece"],
    "GL": [18,"Greenland"],
    "HU": [28,"Hungary"],
    "IS": [26,"Iceland"],
    "IE": [22,"Ireland"],
    "IL": [23,"Israel"],
    "IT": [27,"Italy"],
    "LV": [21,"Latvia"],
    "LI": [21,"Liechtenstein"],
    "LT": [20,"Lithuania"],
    "LU": [20,"Luxembourg"],
    "MK": [19,"Macedonia"],
    "MT": [31,"Malta"],
    "MU": [30,"Mauritius"],
    "MC": [27,"Monaco"],
    "ME": [22,"Montenegro"],
    "NL": [18,"Netherlands"],
    "NO": [15,"Northern Ireland"],
    "PO": [28,"Poland"],
    "PT": [25,"Portugal"],
    "RO": [24,"Romania"],
    "SM": [27,"San Marino"],
    "SA": [24,"Saudi Arabia"],
    "RS": [22,"Serbia"],
    "SK": [24,"Slovakia"],
    "SI": [19,"Slovenia"],
    "ES": [24,"Spain"],
    "SE": [24,"Sweden"],
    "CH": [21,"Switzerland"],
    "TR": [26,"Turkey"],
    "TN": [24,"Tunisia"],
    "GB": [22,"United Kingdom"]}
