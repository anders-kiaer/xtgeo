# coding: utf-8
"""Roxar API functions for XTGeo Cube"""
from __future__ import division, absolute_import
from __future__ import print_function

import numpy as np

from xtgeo.common import XTGeoDialog

xtg = XTGeoDialog()

logger = xtg.functionlogger(__name__)

xtg_verbose_level = xtg.get_syslevel()


def import_cube_roxapi(self, project, name):
    """Import (transfer) a Cube via ROXAR API container to XTGeo."""
    import roxar

    if project is not None and isinstance(project, str):
        projectname = project
        with roxar.Project.open_import(projectname) as proj:
            _roxapi_import_cube(self, proj, name)
    else:
        _roxapi_import_cube(self, project, name)


def _roxapi_import_cube(self, proj, name):
    # note that name must be in brackets
    if [name] not in proj.seismic.data.keys():
        raise ValueError('Name {} is not within RMS Seismic Cube container'
                         .format(name))
    try:
        rcube = proj.seismic.data[[name]]
        _roxapi_cube_to_xtgeo(self, rcube)
    except KeyError as ke:
        logger.error(ke)


def _roxapi_cube_to_xtgeo(self, rcube):
    """Tranforming cube from ROXAPI to XTGeo object."""
    logger.info('Cube from roxapi to xtgeo...')
    self._xori, self._yori = rcube.origin
    self._zori = rcube.first_z
    self._ncol, self._nrow, self._nlay = rcube.dimensions
    self._xinc, self._yinc = rcube.increment
    self._zinc = rcube.sample_rate
    self._rotation = rcube.rotation
    self._yflip = 0
    if rcube.handedness == 'left':
        self._yflip = 1

    if rcube.is_empty:
        xtg.warn('Cube has no data; assume 0')
    else:
        self._values = np.asanyarray(rcube.get_values(), order='F')


def export_cube_roxapi(self, project, name, folder=None, domain='time',
                       compression=('wavelet', 5)):
    """Export (store) a Seismic cube to RMS via ROXAR API spec."""
    import roxar

    if project is not None and isinstance(project, str):
        projectname = project
        with roxar.Project.open_import(projectname) as proj:
            _roxapi_export_cube(self, roxar, proj, name,
                                domain=domain, compression=compression)
    else:
        _roxapi_export_cube(self, roxar, project, name,
                            domain=domain, compression=compression)


def _roxapi_export_cube(self, roxar, proj, name, folder=None, domain='time',
                        compression=('wavelet', 5)):
    if folder is None:
        rcube = proj.seismic.data.create_cube(name)
    else:
        rcube = proj.seismic.data.create_cube(name, folder)

    # populate
    origin = (self.xori, self.yori)
    first_z = self.zori
    increment = (self.xinc, self.yinc)
    sample_rate = self.zinc
    rotation = self.rotation
    vertical_domain = roxar.VerticalDomain.time
    if domain == 'depth':
        vertical_domain = roxar.VerticalDomain.depth

    values = np.asanyarray(self.values, order='C')

    handedness = roxar.Direction.right
    if self.yflip == 1:
        handedness = roxar.Direction.left

    rcube.set_cube(values, origin, increment, first_z, sample_rate, rotation,
                   vertical_domain=vertical_domain,
                   handedness=handedness)
