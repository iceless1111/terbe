from setuptools import setup, find_packages

setup(
    name="terbe",
    version="1.0.0",
    author="Iceless",
    author_email="jhhsu1111@gmail.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_ontent_type="text/markdown",
    url="https://github.com/iceless1111/terbe",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)