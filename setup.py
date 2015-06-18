from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='bika.veterinary',
      version=version,
      description="Bika Veterinary Open Source LIS",
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
      keywords=['lims', 'veterinary', 'bika', 'opensource'],
      author='Naralabs',
      author_email='info@naralabs.com',
      url='http://github.com/naralabs/bika.veterinary',
      license='AGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bika'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'bika.health == 3.1.7',
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
