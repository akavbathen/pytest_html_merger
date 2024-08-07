import os
import pathlib
import random
import string
import subprocess
from dataclasses import dataclass


import pytest


def create_eror_tests(eror: int, filepath: pathlib.Path):
    content = """
import pytest

"""
    b = """
def test_conditional_error():
    number: int = 

 """

    for i in range(eror):
        content += b.replace("test_number", f"test_number_{i}")

    with open(str(filepath), 'w') as file:
        file.write(content)





def create_skip_test(skip: int, filepath: pathlib.Path):
    content = """
import pytest

    """
    b = """
@pytest.mark.skip(reason="Skipping this test for demonstration purposes")
def test_number():
    assert 10 == 10
     """

    for i in range(skip):
        content += b.replace("test_number", f"test_number_{i}")

    with open(str(filepath), 'w') as file:
        file.write(content)


def create_positive_tests(success: int, filepath: pathlib.Path):
    content = """
import pytest

"""
    b = """
def test_number():
    assert 5 == 5
 """

    for i in range(success):
        content += b.replace("test_number", f"test_number_{i}")

    with open(str(filepath), 'w') as file:
        file.write(content)


def create_negative_tests(failed: int, filepath: pathlib.Path):
    content = """
import pytest

"""
    b = """
def test_number():
    assert 5 == 2
     """

    for i in range(failed):
        content += b.replace("test_number", f"test_number_{i}")

    with open(str(filepath), 'w') as file:
        file.write(content)


def create_folder_name(base_name, num_letters=5):
    # Generate a random string of letters
    random_letters = ''.join(random.choices(string.ascii_letters, k=num_letters))

    # Append the random letters to the base folder name
    folder_name = f"{base_name}_{random_letters}"

    return folder_name


def create_pytest_report(venv_path: pathlib.Path, report_path: pathlib.Path, success: int=0, failed: int=0, skip: int=0, eror: int=0):
    base_folder_name = "tests"
    test_path: pathlib.Path = report_path / base_folder_name
    test_path.mkdir(exist_ok=True)

    new_folder_name = create_folder_name(base_folder_name, 5)
    random_path: pathlib.Path = test_path / new_folder_name
    random_path.mkdir()

    create_eror_tests(eror,random_path / "test_eror.py")
    create_skip_test(skip, random_path / "test_skip.py")
    create_positive_tests(success, random_path / "test_pos.py")
    create_negative_tests(failed, random_path / "test_neg.py")
    res = run_pytest(venv_path, random_path, random_path / "report.html")

    # TODO:: return report path
    return ""


def run_pytest(venv_path, path_to_tests: pathlib.Path, report_path: pathlib.Path):
    try:
        result = subprocess.run(f"{venv_path}/bin/pytest --html={report_path} {path_to_tests}", shell=True)
    except Exception as B:
        pass
    if result.returncode == 0:
        print("Command executed successfully!")
        print("Output:\n", result.stdout)
    else:
        print("Command failed with return code:", result.returncode)
        print("Error output:\n", result.stderr)

    return result.returncode


def create_virtualenv(path):
    # Create the virtual environment
    try:
        # Construct the command to create a virtual environment
        command = ['python', '-m', 'venv', path]

        # Run the command
        subprocess.run(command, check=True)
        print(f"Virtual environment created successfully at {path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtual environment: {e}")
        return False


def install_packages(venv_path, packages):
    # Path to the pip executable inside the virtual environment
    pip_executable = os.path.join(venv_path, 'bin', 'pip')

    # Construct the pip install command with the packages list
    command = [pip_executable, 'install'] + packages

    # Execute the pip command
    try:
        subprocess.run(command, check=True)
        print(f"Packages {packages} installed successfully in virtual environment at {venv_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")



@pytest.fixture(scope="session")
def venv():
    loc = pathlib.Path("venv_tests")
    if loc.exists():
        return loc

    loc.mkdir()
    pytest_vers = ["3.2.0", "4.1.1"]
    for pytest_ver in pytest_vers:
        packages_to_install = ['pytest', "setuptools"]
        packages_to_install.append(f"pytest-html=={pytest_ver}")

        venv_path: pathlib.Path = loc / f"venv{pytest_ver}"

        # Create the virtual environment
        if create_virtualenv(venv_path):
            # Install packages in the virtual environment
            install_packages(venv_path, packages_to_install)

    # You can set up the temporary directory here, e.g., creating a subdirectory or files

    # Return the path to the subdirectory, or just tmp_path if you don't need a subdirectory
    return loc


@dataclass
class TestPath:
    """Class for keeping track of an item in inventory."""
    venv_path: pathlib.Path
    venv_path_4: pathlib.Path
    venv_path_3: pathlib.Path
    tmp_path: pathlib.Path
    input_path: pathlib.Path
    result_file_name: pathlib.Path


@pytest.fixture(scope="function")
def custom_tmp_path(venv: pathlib.Path, tmp_path: pathlib.Path):
    venv4 = venv / "venv4.1.1"
    venv3 = venv/ "venv3.2.0"
    input_p = tmp_path / "input_reports"

    subfolder: pathlib.Path = tmp_path / "results"
    subfolder.mkdir(parents=True)

    file_name: pathlib.Path = subfolder / "result.html"
    ret: TestPath = TestPath(venv, venv4, venv3, tmp_path,input_p,file_name)

    input_p.mkdir(exist_ok=True)

    return ret


