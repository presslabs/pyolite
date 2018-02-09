from setuptools import setup, find_packages


requires = ['sh==1.09', 'Unipath==1.1', 'argparse==1.2.1',
            'coverage==3.7.1', 'mock==1.0.1', 'nose==1.3.3',
            'six==1.6.1', 'spec==0.11.1']

setup(name="pyolite",
      version='1.6.1',
      platforms='any',
      packages=find_packages(),
      include_package_data=True,
      install_requires=requires,
      author="Vlad Temian",
      author_email="vlad@presslabs.com",
      url="https://github.com/Presslabs/pyolite",
      description="Python wrapper for gitolite",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Topic :: System :: Networking',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5'
      ])
