# -*- coding: utf-8 -*-
"""
Windows ICO file format.
Based on BMP format.
"""

from struct import unpack
from . import BMP


class ICO(BMP):

    def _open(self):
        # check magic
        if not self.fp.read(4) == "\0\0\1\0":
            raise SyntaxError("not an ICO file")

        images, = unpack("H", self.fp.read(2))

        # pick the largest icon in the file
        lOffset, lWidth, lHeight = 0, 0, 0
        for i in range(images):
            width, height, colors, _ = unpack("BBBB", self.fp.read(4))
            planes, bpp, size, offset = unpack("HHII", self.fp.read(12))

            #width, height = width or 256, height or 256

            if width > lWidth and height > lHeight:
                lOffset = offset
                lWidth = width
                lHeight = height

        # load as bitmap
        self._bitmap(lOffset)

        # patch up the bitmap height
        self.size = lWidth, lHeight
        tile = self.tile[0]
        self.tile[0] = (tile[0], (0, 0) + self.size, tile[2], tile[3])
