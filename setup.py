import setuptools

with open('README.md', 'r') as description_file:
    long_description = description_file.read()

setuptools.setup(name='LocationsMap', version='0.0.1', author='Ivanenko Denis', author_email='ivanenko@ucu.edu.ua',
                 description='Map to display the places where movies were shot', long_description=long_description,
                 long_description_content_type='text/markdown', url='https://github.com/LilJohny/Map.git',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ], )
