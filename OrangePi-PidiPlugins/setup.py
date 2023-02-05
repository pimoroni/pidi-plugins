from setuptools import setup, find_packages

VERSION = "1.0.0"

setup(
    name="OrangePi.PidiPlugins",
    version=VERSION,
    author='Andriy Malyshenko',
    author_email='andriy@sonocotta.com',
    description="Pidi plugins for display output using SPI LCDs on the OrangePi.",
    long_description=open("README.md").read() + "\n" + open("CHANGELOG.txt").read(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/sonocotta/pidi-plugins-python",
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    install_requires=[
        "fonts",
        "font_roboto",
        "Mopidy.OrangePi.Pidi",
        "OrangePi.ST7789",
        "Pillow",
    ],
    entry_points={
        'pidi.plugin.display': [
            'File = OrangePi_PidiPlugins:DisplayFile',
            'DisplayST7789 = OrangePi_PidiPlugins.DisplayST7789:DisplayST7789'
        ]
    },
    python_requires=">=2.7",
    test_suite="tests",
    include_package_data=True
)
