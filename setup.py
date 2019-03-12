from setuptools import Extension, find_packages, setup

setup(
    name="AlphaAssign",
    version="0.0.1",
    author="Andrew Whalen",
    author_email="awhalen@roslin.ed.ac.uk",
    description="A pedigree assignement algorithm.",
    long_description="AlphaAssign is a parentage assignement algorithm that was designed to handle SNP and GBS data.",
    long_description_content_type="text/markdown",
    url="",
    
    packages=['tinyassign','tinyassign.Assign','tinyassign.tinyhouse'],
    package_dir={'': 'src'},

    classifiers=[
        "Programming Language :: Python :: 3",
    ],

    entry_points = {
    'console_scripts': [
        'AlphaAssign=tinyassign.tinyAssign:main',
        'AlphaMGSAssign=tinyassign.tinyMgsAssign:main',
        ],
    },
    install_requires=[
        'numpy',
        'numba',
        'scipy'
    ]
)
