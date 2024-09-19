from distutils.core import setup

import setuptools

setup(
    name="GoogleColabSetup",
    version="0.1.0",
    author="Sander Van Aken",
    packages=setuptools.find_packages(),
    license="LICENSE.txt",
    description="Setup for using notebook in Google Colab",
    long_description=open("README.md").read(),
    python_requires=">=3.10",
)
