
import os
from setuptools import setup, find_packages



def parse_requirements():
    requirements_file = './requirements.txt'
    with open(requirements_file) as f:
        return f.readlines()

setup(
    name="dress-review",
    version="0.1.0",
    description="Building a dress-review with weaviate vector db.",
    author="Lemi",
    author_email="lemidebele@gmail.com",
    url="https://github.com/ldebele/Weaviate",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=parse_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Licence :: MIT Licence",
        "Operating Sytem :: OS Independent",
    ],
    python_requires='>=3.8'
)

