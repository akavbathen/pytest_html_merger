import yaml

with open("pytest_html_merger/ver.yml", "r") as f:
    data = yaml.safe_load(f)

with open("pytest_html_merger/version.py", "w+") as f:
    f.write('name = "{0}"\n'.format(data["name"]))
    f.write('version = "{0}"\n'.format(data["version"]))
    f.write('_version = "{0}"\n'.format(data["_version"]))
