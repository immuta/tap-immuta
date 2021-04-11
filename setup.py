#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="tap-immuta",
    version="0.2.0",
    description="Singer.io tap for extracting data from the Immuta web app.",
    author="Stephen Bailey",
    url="http://github.com/immuta/tap-immuta",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_immuta"],
    entry_points="""
        [console_scripts]
        tap-immuta=tap_immuta.tap:cli
    """,
    packages=setuptools.find_packages(),
    package_data={"schemas": ["tap_immuta/schemas/*.json"]},
    install_requires=["singer-sdk"],
    include_package_data=True,
)
