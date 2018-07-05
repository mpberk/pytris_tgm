import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytris_tgm",
    version="0.0.1",
    author="Matt Berk",
    author_email="matthew.p.berk@gmail.com",
    description="A python implementation of Tetris using the TGM ruleset",
    long_description=long_description
    long_description_content_type="text/markdown",
    url="https://github.com/mpberk/pytris_tgm",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
