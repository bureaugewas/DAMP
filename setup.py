from setuptools import find_packages, setup

setup(
    name='DAMP',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
