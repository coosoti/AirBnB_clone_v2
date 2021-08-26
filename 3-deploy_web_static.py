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
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    date_str = date_str.replace('/', '')
    if not os.path.exists('versions'):
        local("mkdir versions")
    file_name = "versions/web_static_{}.tgz".format(date_str)
    result = local("tar -cvzf {} web_static".format(file_name))
    if result.succeeded:
        file_name
    else:
        return None


def do_deploy(archive_path):
    """this function distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(filename, path, no_ext))
        run('rm /tmp/{}'.format(filename))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """this function creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
