import setuptools


VERSION = "0.0.2"


setuptools.setup(
    name="pidi-display-pil",
    version=VERSION,
    author="Philip Howard",
    author_email="phil@pimoroni.com",
    description="pidi plugin for display output using PIL.",
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
    packages=["pidi_display_pil"],
    install_requires=[
        "fonts",
        "font_roboto",
        "Pillow",
    ],
    entry_points={
        'pidi.plugin.display': [
            'File = pidi_display_pil:DisplayFile'
        ]
    },
    python_requires=">=2.7",
    test_suite="tests",
    include_package_data=True
)
