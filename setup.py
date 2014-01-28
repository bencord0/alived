from setuptools import setup, find_packages

setup(
    name='alived',
    version='0.0.1',
    packages=find_packages(exclude=('tests', 'docs'))
)
