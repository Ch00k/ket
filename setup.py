from setuptools import find_packages, setup


setup(
    name='ket',
    version='0.0.3',
    description='Bitbucket workflows in your terminal',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrii Yurchuk',
    author_email='ay@mntw.re',
    license='MIT',
    url='https://github.com/Ch00k/ket',
    install_requires=[
        'click==7.0',
        'gitpython==2.1.11',
        'requests==2.21.0',
        'tabulate==0.8.3'],
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        ket=ket.cli:ket''',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Version Control :: Git'])
