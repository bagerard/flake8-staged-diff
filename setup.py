from setuptools import setup

INSTALL_REQUIRES = [
    "flake8",
]

VERSION = "0.0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="flake8-staged-diff",
    version=VERSION,
    maintainer="Bastien Gerard",
    maintainer_email="bast.gerard@gmail.com",
    url="https://github.com/bagerard/flake8-staged-diff",
    keywords="flake8 diff linter pre-commit",
    license="MIT License",
    description="Python library to run flake8 only on modified/staged code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["flake8_staged_diff"],
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            # "gitlabci-jsonschema-linter = gitlabci_lint.linter:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
    include_package_data=True,
)
