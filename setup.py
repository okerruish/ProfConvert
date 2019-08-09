from setuptools import setup

setup(name='profconvert',
      version='0.1',
      description='A quick profile converter to use a formatted Google Sheet and turn it in to .json for CyberAIO',
      url='https://github.com/okerruish/profconvert',
      author='Ollie',
      author_email='olliekerruish@albertparkcollege.vic.edu.au',
      license='MIT',
      packages=['profconvert'],
      install_requires=[
          'csv', 'json', 'sys', 'subprocess', 'pandas', 'os'
      ],
      zip_safe=False)