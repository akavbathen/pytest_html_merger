# pytest_html_merger

This utility will merge all of your `pytest` HTML reports into a single HTML report.

## usage

### installation
`pip install pytest-html-merger`

### running
pytest_html_merger [-h] [--version] [-i INPUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  -i INPUT, --input INPUT
  -o OUTPUT, --output OUTPUT

### example
`pytest_html_merger -i /path/to/your/html/reports -o /path/to/output/report/merged.html`

Enjoy merging reports!
