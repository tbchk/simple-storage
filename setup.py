from setuptools import setup


setup(name='simplestorage',
      version='0.1',
      description='Storage client for local and gcloud',
      url='https://github.com/tbchk/simple-storage',
      author='Juan F. Hernandez',
      author_email='jhernandez426@gmail.com',
      license='MIT',
      packages=['simplestorage'],
      install_requires=[
          'google-cloud-storage',
          'pydantic'
      ],
      zip_safe=False)