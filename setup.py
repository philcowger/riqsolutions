from setuptools import setup, find_packages

setup(name='riqsolutions',
      version='0.7.0',
      description='Tools & packages to operationalize RiskIQ datasets',
      author='RiskIQ',
      author_email='support@riskiq.net',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      install_requires=[
          'requests','lxml','xmltodict'
      ],
      zip_safe=False)
