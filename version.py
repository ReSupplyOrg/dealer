import json

with open('package.json') as package_file:
    version = json.load(package_file)['version']
    print(f"version={version}")