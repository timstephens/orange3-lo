from Orange.data import (ContinuousVariable, Domain, FileFormat, Table)
from Orange.data.io_base import DataTableMixin
from typing import List, Iterable

import numpy as np
import datetime


from lo.sdk.api.acquisition.io.open import open as lo_open


class LOReader(FileFormat, DataTableMixin):


    """Read Living Optics processed hyperspectral data files"""
    EXTENSIONS = ('.lo',)
    DESCRIPTION = 'Living Optics processed data file'
    SUPPORT_COMPRESSED = False
    SUPPORT_SPARSE_DATA = True

    # We get the filename from the super when instantiated
    def __init__(self, filename):
        super().__init__(filename)
        print(f"Filename to be loaded is {self.filename}")

    @property
    #This populates a drop-down in the File widget to let you select the frame to view.
    def sheets(self) -> List:
        # from lo.sdk.api.acquisition.io.open import open as lo_open
        sheet_list = []
        with lo_open(self.filename) as f:
            if len(f) > 1: #This is a file containing more than one frame
                for idx, frame in enumerate(f):
                    (metadata, _, _) = frame
                    sheet_list.append(f"{idx}, {metadata.timestamp_s}.{metadata.timestamp_us}")

        return sheet_list


    def read(self):
        # from lo.sdk.api.acquisition.io.open import open as lo_open

        # Accommodate .lo files where there are multiple frames:
        # self.sheet is only set if there's >1 frame (?)
        if self.sheet:
            file_position = self.sheets.index(self.sheet)
            print(f"{self.sheet}, is at {file_position}")
            print(f"/n/n SHEETS /n{self.sheets}")
        else:
            file_position = 0

        with lo_open(self.filename) as f:
            f.seek(file_position)
            (metadata, scene, spectra) = f.read()
        print(f"Metadata = {metadata}")


        #Needs to return a data_table(data, headers). Headers are the wavelength results.
        # Build a Domain to describe the spectra data
        # 
        my_domain = []
        for w in metadata.wavelengths:
            my_domain.append(ContinuousVariable(f"{w}"))
        
        domain = Domain(my_domain, metas=[ContinuousVariable("map_x"), ContinuousVariable("map_y")])
        data = Table.from_numpy(domain, spectra, metas=metadata.sampling_coordinates)
        return data

if __name__ == "__main__":
    #FileFormat.readers['.hea'] = HDRReader_WFDB
    #t = Table("/home/chris/Downloads/ctu-chb-intrapartum-cardiotocography-database-1.0.0/1001.hea")
    print("Wouldn't it be nice to include something to read in a test file if this was run by itself?")
