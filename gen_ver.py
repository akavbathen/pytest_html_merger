import yaml

with open("src/ver.yml", "r") as f:
    data = yaml.safe_load(f)

with open("src/version.py", "w+") as f:
    f.write('name = "{0}"\n'.format(data["name"]))
    f.write('version = "{0}"\n'.format(data["version"]))
    f.write('_version = "{0}"\n'.format(data["_version"]))
