"""bum - setup.py"""
import setuptools

import bum_display_tk

VERSION = bum_display_tk.__version__


setuptools.setup(
    name="bum-display-tk",
    version=VERSION,
    author="Philip Howard",
    author_email="phil@pimoroni.com",
    description="Display output using PIL and Tk.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/pimoroni/bum-plugins",
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["bum_display_tk"],
    install_requires=[
        "tk",
        "Pillow",
    ],
    entry_points={
        'bum_plugin_display': [
            'DisplayTK = bum_display_tk:DisplayTK'
        ]
    },
    python_requires=">=3.6",
    test_suite="tests",
    include_package_data=True
)
