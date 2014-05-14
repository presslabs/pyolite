from setuptools import setup, find_packages

requires = []

setup(name="pyolite",
      version="0.1",
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
      ]
)
