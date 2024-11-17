from setuptools import setup, find_packages

setup(
    name='pykleene',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'graphviz==0.20.3'
    ]
)