from bika.lims.content import bikaschema

bikaschema.BikaSchema['MethodID'].validators = ('uniquefieldvalidator',)
# Update the validation layer after change the validator in runtime
bikaschema.BikaSchema['MethodID']._validationLayer()