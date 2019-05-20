from setuptools import setup, find_packages

setup(name='eventpy',
      version='0.2',
      description='Classes and functions to read and analyse HEP event files.',
      url='http://github.com/LucaMantani/eventpy',
      author='Luca Mantani',
      author_email='luca.mantani@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)