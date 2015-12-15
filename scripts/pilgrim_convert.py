#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pilgrim import utils

usage = "Usage: %s [FILE]..." % (sys.argv[0])

def main():
    if len(sys.argv) < 2:
        print usage
        exit(1)

    for f in sys.argv[1:]:
        if not os.path.exists(f):
            print "%r: No such file or directory" % (f)

        codec = utils.getDecoder(f)
        if codec:
            print "Converting...", f,
            name, ext = os.path.splitext(f)
            codec(f).save(name + ".png")
            print "=> %s.png" % (name)
        else:
            print "Unknown file format for %s..." % (f)
            print usage

if __name__ == "__main__":
    main()
