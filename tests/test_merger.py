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
    subfolder: pathlib.Path = tmp_path / "results"
    subfolder.mkdir()
    file_name: pathlib.Path = subfolder / "result.html"

    create_pytest_report(tmp_path, success=2, failed=2)
    create_pytest_report(tmp_path, success=1, failed=1)
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

