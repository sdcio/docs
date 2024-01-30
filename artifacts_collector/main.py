import logging
import os.path
import shutil
import sys

from jinja2 import Environment, FileSystemLoader
import yaml
import requests


envvar_gh_token = "IPTECHARCH_GITHUB_PAT"
script_dir = os.path.dirname(os.path.abspath(__file__))
artefact_folder = os.path.join(script_dir,"..","artifacts")

def parse():
    environment = Environment(loader=FileSystemLoader(script_dir))
    template = environment.get_template(os.path.join("input.yaml.tmpl"))

    with open(os.path.join(script_dir,'versions.yaml'), 'r') as file:
        data = yaml.safe_load(file)

    content = template.render(data)
    return content

def execute(yaml_def):
    issue_counter = 0

    headers = {
        "Accept": "application/vnd.github.v3.raw"
    }

    t = os.getenv(envvar_gh_token)
    if t is not None:
        headers["Authorization"] = f'token {t}'

    for entry in yaml_def["urls"]:
        r = requests.get(entry["url"], allow_redirects=True, headers=headers)
        if r.status_code != 200:
            logging.error(f'failed downloading {entry["url"]} with status code {r.status_code}')
            issue_counter += 1
            continue

        file = os.path.join(artefact_folder,entry["file"])
        open(file, 'wb').write(r.content)
        logging.info(f'successfully downloaded {entry["url"]} to {file}')

    return issue_counter

def prepare():
    shutil.rmtree(artefact_folder, ignore_errors=True)
    os.mkdir(artefact_folder)
def main():
    prepare()
    data = parse()
    logging.debug(data)
    return execute(yaml.safe_load(data))

if __name__ == '__main__':
    sys.exit(main())

