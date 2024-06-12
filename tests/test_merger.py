import pathlib
import pytest
import pytest_html_merger.main as phm
from bs4 import BeautifulSoup
from tests.conftest import create_pytest_report
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re



def test_title(custom_tmp_path):
    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / "venv4"

    create_pytest_report(venv_path, input_path, success=1, failed=2)
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
    title = soup.select_one("#head-title").string
    assert title == "merged"


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


def test_report_created(custom_tmp_path):
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



@pytest.mark.parametrize("payTest", [
    ("3.2"),        # test case 1
    ("4")   # test case 2

])
def test_checking_the_number_of_failed_and_success_records(custom_tmp_path,payTest):
    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / f"venv{payTest}"

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

    elements_failed = driver.find_elements(By.CSS_SELECTOR, ".results-table-row.failed")
    elements_success = driver.find_elements(By.CSS_SELECTOR, ".results-table-row.passed")
    assert len(elements_failed) == 3 and len(elements_success) == 3


@pytest.mark.parametrize("payTest", [
    ("3.2.0"),        # test case 1
    ("4.1.1")   # test case 2

])
def test_Version_check_pytest(custom_tmp_path,payTest):
    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / f"venv{payTest}"

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

    p_element = driver.find_element(By.CSS_SELECTOR, 'p')
    texts = p_element.text
    version = texts[-5:]
    assert version == payTest


def test_The_date_the_report_was_created(custom_tmp_path):
    today = datetime.today().date()

    subfolder: pathlib.Path = custom_tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path / "venv4.1.1"

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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    file_path = f'file://{file_name}'
    driver.get(file_path)

    p_element = driver.find_element(By.TAG_NAME, 'p')
    text = p_element.text
    pattern = r'^.+ (\d{2}-.+-\d{4})'
    match = re.search(pattern, text)
    date_str = match.group(1)

    date_obj = datetime.strptime(date_str, '%d-%b-%Y').date()
    assert date_obj == today






