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


def test_h1_title(custom_tmp_path):
    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / "venv4"

    create_pytest_report(venv_path, input_path, success=10, failed=2)
    create_pytest_report(venv_path, input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(input_path),
            "-o",
            str(file_name),
            "-t",
            "merged"

        ]
    )

    with open(file_name, "r") as f:
        html_content: str = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.select_one("#title").string
    assert title == "merged"


def test_succeeded_and_failed(custom_tmp_path):
    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / "venv4"

    create_pytest_report(venv_path, input_path, success=10, failed=2)
    create_pytest_report(venv_path, input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(input_path),
            "-o",
            str(file_name),
            "-t",
            "html_report"

        ]
    )

    assert file_name.exists()

