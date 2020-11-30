#!/usr/bin/python

import io
import os
import shutil
import subprocess
import sys
import tarfile
from contextlib import closing
from os import makedirs
from time import gmtime, strftime
from pprint import pprint

import requests
from jinja2 import Environment, FileSystemLoader


arches = list(os.environ.get("arches").split(",")) if os.environ.get("arches", False) else ["amd64", "arm64", "armhf"]
scriptsDir = "/scripts"
baseDir = f"{scriptsDir}/out"
outDir = "./builds"

makedirs(baseDir)
if not os.path.exists(outDir):
    makedirs(outDir)

data = {}
project = os.environ.get("INPUT_REPO", os.environ.get("GITHUB_REPOSITORY"))

data["date"] = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
data["description"] = os.environ.get("INPUT_DESCRIPTION", None)
data["maintainer"] = os.environ.get("INPUT_MAINTAINER", project.split("/")[0])
data["name"] = os.environ.get("INPUT_NAME", project.split("/")[1]).lower()
data["project"] = project
data["tag"] = os.environ.get("INPUT_VERSION", None)
data["token"] = os.environ.get("GITHUB_TOKEN")

print(f"::add-mask::{data['token']}")

url = f"https://api.github.com/repos/{data['project']}"

headers = {
    "Accept": "application/vnd.github.v3+json",
}

if data['token']:
    headers["Authorization"] = "token " + data["token"]

if not data["tag"]:
    print(f"::debug::{url}/releases/latest")
    r = requests.get(url=url + "/releases/latest", headers=headers).json()
    data["tag"] = r["tag_name"]

if not data["description"]:
    print(f"::debug::{url}")
    r = requests.get(url=url, headers=headers).json()
    data["description"] = r["description"]

data["description"] = data["description"].replace("\n", "\n ")


def gen_metadata(data):
    r = requests.get(url=url + f"/releases/tags/{data['tag']}", headers=headers).json()

    changelog = f"Automaticity generated, visit https://github.com/{data['project']}/releases/tag/{data['tag']}\n"
    changelog += r.get("body").replace('\r', '')
    changelog = changelog.replace('\n', '\n  ')
    data["changelog"] = changelog
    data["state"] = "unstable"
    if not r["prerelease"]:
        data["state"] = "stable"
    print(f"::set-output name=state::{data['state']}")
    return data


def gen_template(data, dir_):
    templateLoader = FileSystemLoader(searchpath=scriptsDir + "/templater/jinja/")
    templateEnv = Environment(loader=templateLoader)

    j2_changelog = templateEnv.get_template("changelog.j2")
    j2_control = templateEnv.get_template("control.j2")

    shutil.copytree(scriptsDir + "/templater/debian", dir_ + "/debian")
    j2_changelog.stream(**data).dump(dir_ + "/debian/changelog")
    j2_control.stream(**data).dump(dir_ + "/debian/control")


def gen_pkg(data):
    pkg_name = f"{data['name']}_{data['tag'][1:]}"
    print(f"Creating folder for {pkg_name} - {data['arch']}")
    ver_dir = baseDir + f"/{data['arch']}/{pkg_name}"
    makedirs(ver_dir + f"/{data['name']}")
    gen_template(data, ver_dir)
    file_mapper = {
        "amd64": "linux-x64.tar.gz",
        "armhf": "linux-arm.tar.gz",
        "arm64": "linux-arm64.tar.gz",
    }
    url = f"https://github.com/{data['project']}/releases/download/{data['tag']}/{file_mapper[data['arch']]}"
    r = requests.get(url, headers=headers)
    with closing(r), tarfile.open(fileobj=io.BytesIO(r.content), format="r:gz") as archive:
        archive.extractall(ver_dir + f"/{data['name']}")
        archive.close()

    print(f"Packaging {pkg_name} - {data['arch']}")
    process = subprocess.Popen(["dpkg-buildpackage", "-b", "-us", "-uc", "-a",
                                data['arch']], cwd=ver_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    log = ""
    errlog = ""
    while True:
        msg = process.stdout.readline()
        err = process.stderr.readline()
        log += msg
        errlog += err
        print(f"[ {data['arch']} ] {msg.strip()}")
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            with open(f"{outDir}/{data['arch']}_build.log", "w") as f:
                for msg in log:
                    f.write(msg)
            with open(f"{outDir}/{data['arch']}_err.log", "w") as f:
                for msg in errlog:
                    f.write(msg)
            if return_code != 0:
                exit(1)
            break
    print(f"Successfully built {pkg_name} - {data['arch']}")

    shutil.copyfile(
        ver_dir + f"_{data['arch']}.deb", f"{outDir}/{pkg_name}_{data['arch']}.deb")


if __name__ == "__main__":

    data = gen_metadata(data)
    for arch in arches:
        os.environ["DEB_BUILD_ARCH"] = arch
        data["arch"] = arch
        gen_pkg(data)
