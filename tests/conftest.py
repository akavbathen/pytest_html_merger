import os
import pathlib
import random
import string
import subprocess

import pytest


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


def create_pytest_report(venv_path: pathlib.Path, report_path: pathlib.Path, success: int, failed: int):
    base_folder_name = "tests"
    test_path: pathlib.Path = report_path / base_folder_name
    test_path.mkdir(exist_ok=True)

    new_folder_name = create_folder_name(base_folder_name, 5)
    random_path: pathlib.Path = test_path / new_folder_name
    random_path.mkdir()

    create_positive_tests(success, random_path / "test_pos.py")
    create_negative_tests(failed, random_path / "test_neg.py")
    res = run_pytest(venv_path, random_path, random_path / "report.html")

    # TODO:: return report path
    return ""


def run_pytest(venv_path, path_to_tests: pathlib.Path, report_path: pathlib.Path):
    result = subprocess.run(f"{venv_path}/bin/pytest --html={report_path} {path_to_tests}", shell=True)

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


@pytest.fixture
def custom_tmp_path(tmp_path):
    # List of packages to install
    packages_to_install = ['pytest', 'pytest-html']

    pytest_vers = ["3", "4"]
    for pytest_ver in pytest_vers:
        venv_path = tmp_path / f"venv{pytest_ver}"

        # Create the virtual environment
        if create_virtualenv(venv_path):
            # Install packages in the virtual environment
            install_packages(venv_path, packages_to_install)

    # You can set up the temporary directory here, e.g., creating a subdirectory or files

    # Return the path to the subdirectory, or just tmp_path if you don't need a subdirectory
    return tmp_path