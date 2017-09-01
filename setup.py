# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rpi_aiy_blinkt_assist',
    version='0.1.0',
    description='Raspberry Project for Pimoroni''s Blinkt LED with Google AIY Color effects',
    long_description=readme,
    author='Pierre-yves Baloche',
    author_email='funkypiwy@gmail.com',
    url='https://github.com/pierreyvesbaloche/rpi_aiy_blinkt_assist',
    license=license,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=find_packages(exclude=('tests', 'docs'))
)
