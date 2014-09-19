from setuptools import setup, find_packages

setup(
    name='cadizm-scramble',
    version='0.1.0',
    author='Michael Cadiz',
    author_email='michael.cadiz@gmail.com',
    packages=find_packages(),
    scripts=[
    ],
    url='http://0xfa.de/scramble',
    license='LICENSE.txt',
    description='Scramble (aka Boggle) Solver',
    long_description=open('README.txt').read(),
    install_requires=[
    ],
    include_package_data=True,
    data_files=[
#        ('/usr/local/scramble/data', ['words.txt', 'words_gte_6-1.txt', 'words_gte_6-2.txt']),
    ],
    zip_safe=False,
)
