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

      zip_safe=False)