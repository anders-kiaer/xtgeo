# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from __future__ import print_function

from os.path import join

import xtgeo

xtg = xtgeo.common.XTGeoDialog()
logger = xtg.basiclogger(__name__)

if not xtg.testsetup():
    raise SystemExit

TMPDIR = xtg.tmpdir
TESTPATH = xtg.testpath

WFILE = join(TESTPATH, "wells/battle/1/WELLX.rmswell")
SFILE = join(TESTPATH, "surfaces/etc/battle_1330.gri")


def test_get_well_x_surf():
    """Getting XYZ, MD for well where crossing a surface"""

    wll = xtgeo.Well(WFILE, mdlogname="Q_MDEPTH")
    surf = xtgeo.RegularSurface(SFILE)
    top = wll.get_surface_picks(surf)

    print(top.dataframe)
