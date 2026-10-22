# -*- coding: utf-8 -*-

import os

from PIL import Image

from amzqr.mylibs.constant import PIXELS_PER_MODULE


def draw_qrcode(abspath, qrmatrix):
    unit_len = PIXELS_PER_MODULE
    size = len(qrmatrix)
    if type(qrmatrix) in (list, tuple) and all(
        type(line) in (list, tuple) and len(line) == size for line in qrmatrix
    ):
        # Render one pixel per module, including the quiet zone, then expand
        # whole modules in Pillow instead of writing each output pixel in Python.
        pic = Image.new("1", (size + 8, size + 8), "white")
        pixels = pic.load()
        for y, line in enumerate(qrmatrix, 4):
            for x, module in enumerate(line, 4):
                if module:
                    pixels[x, y] = 0
        pic = pic.resize(((size + 8) * unit_len,) * 2, Image.NEAREST)
        saving = os.path.join(abspath, "qrcode.png")
        pic.save(saving)
        return saving

    x = y = 4 * unit_len
    pic = Image.new("1", [(len(qrmatrix) + 8) * unit_len] * 2, "white")

    for line in qrmatrix:
        for module in line:
            if module:
                draw_a_black_unit(pic, x, y, unit_len)
            x += unit_len
        x, y = 4 * unit_len, y + unit_len

    saving = os.path.join(abspath, "qrcode.png")
    pic.save(saving)
    return saving


def draw_a_black_unit(p, x, y, ul):
    if (
        type(p) is Image.Image
        and p.mode == "1"
        and type(x) is int
        and type(y) is int
        and type(ul) is int
        and ul > 0
        and 0 <= x <= p.width - ul
        and 0 <= y <= p.height - ul
    ):
        p.paste(0, (x, y, x + ul, y + ul))
        return
    for i in range(ul):
        for j in range(ul):
            p.putpixel((x + i, y + j), 0)
