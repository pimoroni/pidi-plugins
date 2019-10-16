import setuptools


VERSION = '0.0.1'


setuptools.setup(
    name="pidi-display-tk",
    version=VERSION,
    author="Philip Howard",
    author_email="phil@pimoroni.com",
    description="pidi plugin to display output using PIL and Tk.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/pimoroni/pidi-plugins",
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pidi_display_tk"],
    install_requires=[
        "pidi-display-pil",
        "tk",
        "Pillow",
    ],
    entry_points={
        'pidi.plugin.display': [
            'DisplayTK = pidi_display_tk:DisplayTK'
        ]
    },
    python_requires=">=3.6",
    test_suite="tests",
    include_package_data=True
)
