import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discordsdk",
    version="0.2.4",
    author="LennyPhoenix & NathaanTFM",
    author_email="lennyphoenixc@gmail.com",
    description="Python wrapper around Discord's Game SDK library.",
    license="LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LennyPhoenix/py-discord-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
