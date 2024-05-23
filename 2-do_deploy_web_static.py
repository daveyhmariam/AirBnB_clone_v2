#!/usr/bin/python3
"""Deploy to remote server
"""
import os
from fabric.api import env, put, run

env.hosts = ["54.164.142.209", "54.160.125.83"]


def do_deploy(archive_path):
    """Fabric script to distribute releases to remote server

    Args:
        archive_path (str): The path of the archive.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        print("Error: Archive file not found at {}".format(archive_path))
        return False

    file = os.path.basename(archive_path)
    filename = os.path.splitext(file)[0]

    try:
        put(archive_path, "/tmp/{}".format(file))
        run("sudo rm -rf /data/web_static/releases/{}/".format(filename))
        run("sudo mkdir -p /data/web_static/releases/{}/".format(filename))
        run("sudo tar -xzf /tmp/{} -C\
            /data/web_static/releases/{}/".format(file, filename))
        run("sudo rm -f /tmp/{}".format(file))
        run("sudo mv /data/web_static/\
            releases/{}/web_static/* /data/web_static\
                /releases/{}/".format(filename, filename))
        run("sudo rm -rf /data/web_static/\
            releases/{}/web_static".format(filename))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/\
            releases/{}/ /data/web_static/current".format(filename))
        return True
    except Exception as e:
        return False
