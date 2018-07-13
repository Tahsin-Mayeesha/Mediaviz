import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='mediaviz',
      version='0.1',
      description='Visualize Networks With Force Atlas 2 Layout',
      long_description = long_description,
          long_description_content_type="text/markdown",
      url='https://github.com/Tahsin-Mayeesha/Mediaviz',
      author='Tahsin Mayeesha',
      author_email='tasmiah.tahsin@hotmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    install_requires=[ "fa2l",
        "networkx<2.0.0",
        "numpy", "matplotlib"
    ],

    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
    ],
     
      zip_safe=False)