from setuptools import setup, find_packages

version = '0.1'

setup(name='bika.veterinary',
      version=version,
      description="Bika Veterinary LIS",
      long_description=open("README.md").read() + "\n\n" +
                       open("docs/CHANGELOG.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Veterinary Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        ],
      keywords='',
      author='Naralabs',
      author_email='infonaralabs.com',
      url='http://naralabs.com',
      license='AGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bika'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'bika.health == 3.1.7',
          'archetypes.schemaextender',
          'z3c.unconfigure == 1.0.1',
      ],
      extras_require={
          'test': [
                  'plone.app.testing',
                  'robotsuite',
                  'robotframework-selenium2library',
                  'plone.app.robotframework',
                  'robotframework-debuglibrary',
              ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
