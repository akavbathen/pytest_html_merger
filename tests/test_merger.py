import pytest
from bs4 import BeautifulSoup

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


