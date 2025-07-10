from setuptools import setup, find_packages

setup(
    name="jira_arangodb_connector",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests>=2.28.0",
        "python-arango>=7.3.0"
    ],
    author="Rithwik T",
    author_email="rithwik.t2003@gmail.com",
    description="A Python library to migrate Jira issues to ArangoDB",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rithwikt2003/jira_arangodb_connector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)