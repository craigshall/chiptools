# Import needed function from setuptools
from setuptools import setup

# Create proper setup to be used by pip
setup(name='chiptools',
      version='0.0.1',
      description='Utilities for removing rows and columns from pandas DataFrames.',
      author='Craig Hall',
      email='craigsh@gmail.com',
      packages=['chiptools'],
      install_requires=['numpy', 'pandas>=0.24.0'])
