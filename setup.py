import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stl_to_h5m",
    version="develop",
    author="The stl_to_h5m Development Team",
    author_email="mail@jshimwell.com",
    description="Converts STL files to a DAGMC h5m file using PyMoab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusion-energy/stl_to_h5m",
    packages=setuptools.find_packages(),
    package_data={
        "stl_to_h5m": [
            "requirements.txt",
            "README.md",
            "LICENSE",
            "tests/*.stl",
        ]
    },
    classifiers=[
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        # 'pymoab' currently only available via conda-forge
    ],
)
