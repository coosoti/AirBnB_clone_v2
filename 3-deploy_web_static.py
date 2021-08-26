#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy
"""

from fabric.api import put, run, env
from os.path import exists
import os
from datetime import datetime
from fabric.api import local
env.hosts = ['35.243.198.3', '35.231.244.226']


def do_pack():
    """ Creates a .tgz archive from the contents of the web_static folder """
    if not os.path.isdir("./versions"):
        os.makedirs("./versions")
    dtime = datetime.now().strftime("%Y%m%d%H%M%S")
    local("tar -czzf versions/web_static_{}.tgz web_static/*".format(dtime))
    return ("{}/versions/web_static_{}.tgz".format(os.path.dirname(
        os.path.abspath(__file__)), dtime))


def do_deploy(archive_path):
    """this function distributes an archive to the web servers"""
    if archive_path is None or not os.path.isfile(archive_path):
        print("NOT PATH")
        return False

    filename = os.path.basename(archive_path)
    rm_ext = filename.split(".")[0]

    put(local_path=archive_path, remote_path="/tmp/")
    run("mkdir -p /data/web_static/releases/{}".format(rm_ext))
    run("tar -xzf /tmp/{} \
    -C /data/web_static/releases/{}".format(filename, rm_ext))
    run("rm /tmp/{}".format(filename))
    run("rm -rf /data/web_static/current")
    run("ln -fs /data/web_static/releases/{}/ \
    /data/web_static/current".format(rm_ext))
    run("mv /data/web_static/current/web_static/* /data/web_static/current/")
    run("rm -rf /data/web_static/curren/web_static")

    return True


def deploy():
    """this function creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
