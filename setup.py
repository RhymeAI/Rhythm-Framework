from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

with open("VERSION.txt", "r") as file:
    version = file.read()

setup(
    name="rhythmFramework",
    version=version,
    description="A Framework for faster development with AI Agents.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.rhyme-network.com",
    author="Rhyme Network",
    author_email="rhyme.ainetwork@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=["langchain >= 0.0.350", "qdrant-client >= 1.7.0", "tweepy >= 4.14.0", "openai >= 1.4.0"],
    python_requires=">=3.12",
)
