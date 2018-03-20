# -*- coding: utf-8 -*-
"""XTGeo xyz.polygons module, which contains the Polygons class."""

# For polygons, the order of the points sequence is important. In
# addition, a Polygons dataframe _must_ have a columns called 'ID'
# which identifies each polygon piece.

from __future__ import print_function, absolute_import
import pandas as pd

from xtgeo.xyz._xyz import XYZ
from xtgeo.xyz._xyz_io import _convert_idbased_xyz


class Polygons(XYZ):
    """Class for a polygons (connected points) in the XTGeo framework."""

    def __init__(self, *args, **kwargs):

        super(Polygons, self).__init__(*args, **kwargs)

        self._ispolygons = True

    @property
    def nrow(self):
        """ Returns the Pandas dataframe object number of rows"""
        if self._df is None:
            return 0
        else:
            return len(self._df.index)

    @property
    def dataframe(self):
        """ Returns or set the Pandas dataframe object"""
        return self._df

    @dataframe.setter
    def dataframe(self, df):
        self._df = df.copy()

    def from_file(self, pfile, fformat='xyz'):
        """Doc later"""
        super(Polygons, self).from_file(pfile, fformat=fformat)

        # for polygons, a seperate column with ID is required; however this may
        # lack if the input is on XYZ format

        if 'ID' not in self._df.columns:
            self._df['ID'] = self._df.isnull().all(axis=1).cumsum().dropna()
            self._df.dropna(axis=0, inplace=True)
            self._df.reset_index(inplace=True, drop=True)

    def to_file(self, pfile, fformat='xyz', attributes=None, filter=None,
                wcolumn=None, hcolumn=None, mdcolumn=None):
        """Doc later"""
        super(Polygons, self).to_file(pfile, fformat=fformat,
                                      attributes=attributes, filter=filter,
                                      wcolumn=wcolumn, hcolumn=hcolumn,
                                      mdcolumn=mdcolumn)

    def from_wells(self, wells, zone, resample=1):

        """Get line segments from a list of wells and a zone number

        Args:
            wells (list): List of XTGeo well objects
            zone (int): Which zone to apply
            resample (int): If given, resample every N'th sample to make
                polylines smaller in terms of bit and bytes.
                1 = No resampling.

        Returns:
            None if well list is empty; otherwise the number of wells that
            have one or more line segments to return

        Raises:
            Todo
        """

        if len(wells) == 0:
            return None

        dflist = []
        maxid = 0
        for well in wells:
            wp = well.get_zone_interval(zone, resample=resample)
            if wp is not None:
                # as well segments may have overlapping ID:
                wp['ID'] += maxid
                maxid = wp['ID'].max() + 1
                dflist.append(wp)

        if len(dflist) > 0:
            self._df = pd.concat(dflist, ignore_index=True)
            self._df.reset_index(inplace=True, drop=True)
        else:
            return None

        return len(dflist)

    def get_xyz_dataframe(self):
        """Convert from ID based to XYZ, where a new polygon is marked
        with a 999.0 value as flag"""

        self.logger.info(self.dataframe)

        return _convert_idbased_xyz(self.dataframe)
