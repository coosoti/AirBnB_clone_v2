#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.api import put, run, env
from os.path import exists, isfile
env.hosts = ['35.243.198.3', '35.231.244.226']


def do_deploy(archive_path):
    """this distributes anbarchive to the web servers"""

    if not isfile(archive_path):
        return False
    filename = basename(archive_path)
    try:
        no_ext = filename.split(".")[0]
        put(archive_path, "/tmp/")
        extract_path = "/data/web_static/releases/{}".format(no_ext)
        run("mkdir -p {}".format(extract_path))
        run("tar xzf /tmp/{} -C {}".format(filename, extract_path))
        run("rm /tmp/{}".format(filename))
        run("mv {0}/web_static/* {0}/".format(extract_path))
        run("rm -rf {0}/web_static/".format(extract_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(extract_path))
        return True
    except:
        return False
