import pathlib

import pytest

import pytest_html_merger.main as phm

from bs4 import BeautifulSoup

from tests.conftest import create_pytest_report


def test_title():
    html_file_path: str = "./merged.html"

    with open(html_file_path, "r") as f:
        html_content: str = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    title = soup.title.string
    assert title == "merged.html"


def test_h1_title():
    html_file_path: str = "./merged.html"

    with open(html_file_path, "r") as f:
        html_content: str = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    title = soup.select_one("#title").string
    assert title == "merged.html"


def test_succeeded_and_failed(tmp_path):
    tmp_path = pathlib.Path("/private/var/folders/sz/zyxdxk1j67v40grz43dgnpx00000gp/T/pytest-of-bathen/pytest-2/test_succeeded_and_failed0")
    subfolder: pathlib.Path = tmp_path / "results"
    subfolder.mkdir(exist_ok=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)

    create_pytest_report(input_path, success=10, failed=2)
    create_pytest_report(input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(tmp_path),
            "-o",
            str(file_name),
            "-t",
            "html_report"

        ]
    )

    assert file_name.exists()

