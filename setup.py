import setuptools

from src import version

description = "Pytest HTML reports merging utility"

with open("requirements.txt") as fid:
    install_requires = fid.readlines()

setuptools.setup(
    name="pytest_html_merger",
    version=version.version,
    author="Akav Bat Hen",
    author_email="akav.bathen@gmail.com",
    description=description,
    long_description=description,
    python_requires=">=3.6.0",
    url="https://github.com/akavbathen/pytest_html_merger.git",
    install_requires=install_requires,
    package_dir={"pytest_html_merger": "src"},
    packages=["pytest_html_merger"],
    entry_points={"console_scripts": ["pytest_html_merger = src.main:main"]},
    include_package_data=True,
)
