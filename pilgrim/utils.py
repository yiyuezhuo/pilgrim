# -*- coding: utf-8 -*-
"""
Utility functions for pilgrim
"""
import mimetypes

from . import codecs

def __defaultopen(file):
    import os, subprocess, sys

    if os.name == "posix":
        if sys.platform == "darwin":
            cmd = "open"

        cmd = "xdg-open"

    elif os.name == "nt":
        cmd = "start"

    else:
        raise NotImplementedError("Unsupported os: %r", os.name)

    return subprocess.call((cmd, file))

def show(files):
    import tempfile

    for img in files:
        tmp, filename = tempfile.mkstemp(suffix=".png")
        if img.mode == "CMYK":
            img = img.convert("RGBA")
        img.save(filename)
        __defaultopen(filename)

def getDecoder(filename):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/dn424129(v=vs.85).aspx
    mimetypes.add_type('image/vnd-ms.dds', '.dds')

    """
    NOTICE: This is not a standard, see also
    https://github.com/jleclanche/mpqt/blob/master/packages/blizzard.xml
    """
    mimetypes.add_type('image/vnd.bliz.blp', '.blp')

    filename = filename.lower()
    mime_type, encoding = mimetypes.guess_type(filename)

    if mime_type == "image/vnd-ms.dds":
        return codecs.DDS

    if mime_type == "image/png":
        return codecs.PNG

    if mime_type == "image/vnd.microsoft.icon":
        return codecs.ICO

    # if filename.endswith(".blp"):
    #     return codecs.BLP
    if mime_type == "image/vnd.bliz.blp":
        return codecs.BLP

    if filename.endswith(".ftc") or filename.endswith(".ftu"):
        return codecs.FTEX