"""bum - setup.py"""
import setuptools

import bum_display_st7789

VERSION = bum_display_st7789.__version__


setuptools.setup(
    name="bum-display-st7789",
    version=VERSION,
    author="Philip Howard",
    author_email="phil@pimoroni.com",
    description="Display output using an ST7789 1.3\" 240x240 SPI LCD.",
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
    packages=["bum_display_st7789"],
    install_requires=[
        "st7789",
        "Pillow",
    ],
    entry_points={
        'bum_plugin_display': [
            'DisplayST7789 = bum_display_st7789:DisplayST7789'
        ]
    },
    python_requires=">=3.6",
    test_suite="tests",
    include_package_data=True
)
