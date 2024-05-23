#!/usr/bin/python3
"""Deploy to remote server
"""
import os
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["54.164.142.209", "54.160.125.83"]


def do_deploy(archive_path):
    """fiber script to distribute releases to remote server

    Args:
        archive_path (str): The path of the archive.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True."""
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    filename = file.split(".")[0]
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/".format(filename)).failed:
        return False
    if run("sudo mkdir -p /data/web_static/releases/{}/".format(filename)).failed:
        return False
    if run("sudo tar -xzf /tmp/{} -C /data/web_static/\
            releases/{}/".format(file, filename)).failed:
        return False
    if run("sudo rm -rf /tmp/{}".format(file)).failed:
        return False
    if run("sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(filename, filename)).failed:
        return False
    if run("sudo rm -rf /data/web_static/releases/\
            {}/web_static".format(filename)).failed:
        return False
    if run("sudo rm -rf /data/web_static/current").failed:
        return False
    if run("sudo ln -s /data/web_static/releases/{}/\
        /data/web_static/current").failed:
        return False
    return True
