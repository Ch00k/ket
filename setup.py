from setuptools import find_packages, setup


setup(
    name='ket',
    version='0.0.1',
    install_requires=[
        'click==7.0',
        'gitpython==2.1.11',
        'requests==2.21.0',
        'tabulate==0.8.3'],
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        ket=ket.cli:ket''')
