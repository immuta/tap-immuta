#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="tap-immuta",
    version="0.1.0",
    description="Singer.io tap for extracting data from Immuta Accounts API",
    author="Stephen Bailey",
    url="http://singer.io/",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_immuta"],
    entry_points="""
        [console_scripts]
        tap-immuta=tap_immuta:main
    """,
    packages=setuptools.find_packages(),
    package_data = {
        "schemas": ["tap_immuta/schemas/*.json"]
    },
    include_package_data=True,
)
