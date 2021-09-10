import setuptools

VERSION = '0.1.2'


setuptools.setup(
    name="pidi-display-st7789",
    version=VERSION,
    author="Philip Howard",
    author_email="phil@pimoroni.com",
    description="pidi plugin for display output using an ST7789 1.3\" 240x240 SPI LCD.",
    long_description=open("README.md").read() + "\n" + open("CHANGELOG.txt").read(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/pimoroni/pidi-plugins",
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pidi_display_st7789"],
    install_requires=[
        "pidi-display-pil>=0.1.0",
        "st7789",
        "Pillow",
    ],
    entry_points={
        'pidi.plugin.display': [
            'DisplayST7789 = pidi_display_st7789:DisplayST7789'
        ]
    },
    python_requires=">=2.7",
    test_suite="tests",
    include_package_data=True
)
