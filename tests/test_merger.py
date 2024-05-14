import pathlib
import pytest
import pytest_html_merger.main as phm
from bs4 import BeautifulSoup
from tests.conftest import create_pytest_report
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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

def test_the_number_of_failures_indicated_in_the_report(custom_tmp_path, element=None):
    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / "venv4"

    create_pytest_report(venv_path, input_path, success=2, failed=2)
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
    with open(file_name, "r") as f:
        html_content: str = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    element = soup.find('span', class_='failed')
    text = element.get_text()

    parts = text.split(' ')
    res = (parts[0].strip())
    assert res == '3'



def test_checking_the_number_of_failed_records(custom_tmp_path):
    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / "venv4"

    create_pytest_report(venv_path, input_path, success=2, failed=2)
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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    file_path = f'file://{file_name}'
    driver.get(file_path)

    elements = driver.find_elements(By.CSS_SELECTOR, ".results-table-row.failed")
    assert len(elements) == 3
