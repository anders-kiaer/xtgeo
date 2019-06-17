# coding: utf-8
from __future__ import division, absolute_import
from __future__ import print_function

import os
from collections import OrderedDict
from os.path import join

import pytest

import xtgeo
import test_common.test_xtg as tsetup

xtg = xtgeo.common.XTGeoDialog()
logger = xtg.basiclogger(__name__)

if not xtg.testsetup():
    raise SystemExit

TMPDIR = xtg.tmpdir
TESTPATH = xtg.testpath

REEKROOT = "../xtgeo-testdata/3dgrids/reek/REEK"
WELL1 = "../xtgeo-testdata/wells/reek/1/OP_1.w"

# =============================================================================
# Do tests
# =============================================================================


def test_randomline_fence():
    """Import ROFF grid with props and make fences"""

    grd = xtgeo.Grid(REEKROOT, fformat="eclipserun", initprops=["PORO"])
    wll = xtgeo.Well(WELL1, zonelogname="Zonelog")

    print(grd.describe(details=True))

    # get the polygon for the well, limit it to 1200
    fspec = wll.get_fence_polyline(
        sampling=10, nextend=2, asnumpy=False, tvdmin=1200
    )
    print(fspec.dataframe)

    tsetup.assert_almostequal(fspec.dataframe[fspec.dhname][4], 12.6335, 0.001)
    logger.info(fspec.dataframe)

    fspec = wll.get_fence_polyline(
        sampling=10, nextend=2, asnumpy=True, tvdmin=1200
    )

    # get the "image", which is a 2D numpy that can be plotted with e.g. imgshow
    hmin, hmax, vmin, vmax, por = grd.get_randomline(
        fspec, "PORO", zmin=1200, zmax=1700, zincrement=1.0
    )

    import numpy as np
    print(np.nanmean(por))

    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(por, cmap='seismic', interpolation='sinc',
               extent=(hmin, hmax, vmax, vmin))
    plt.axis('tight')
    plt.colorbar()
    plt.show()
