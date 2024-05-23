#!/usr/bin/python3
""" archive a directory to tgz
"""
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """fabric script to create archive
    """
    dtime = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dtime.year,
                                                         dtime.month,
                                                         dtime.day,
                                                         dtime.hour,
                                                         dtime.minute,
                                                         dtime.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
