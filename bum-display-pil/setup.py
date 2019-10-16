"""bum - setup.py"""
import setuptools

import bum_display_pil

VERSION = bum_display_pil.__version__


setuptools.setup(
    name="bum-display-pil",
    version=VERSION,
    author="Philip Howard",
    author_email="phil@pimoroni.com",
    description="Display output using PIL.",
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
    packages=["bum_display_pil"],
    install_requires=[
        "fonts",
        "font_roboto",
        "Pillow",
    ],
    entry_points={
        'bum_plugin_display': [
            'File = bum_display_pil:DisplayFile'
        ]
    },
    python_requires=">=3.6",
    test_suite="tests",
    include_package_data=True
)
