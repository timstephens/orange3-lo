#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QStyle, QSizePolicy, QFileDialog
from Orange.data import Table
from Orange.data import Domain
from Orange.data import StringVariable, ContinuousVariable
#from Orange.data import  DiscreteVariable
from Orange.widgets import gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Msg, Output
import numpy as np
from os import path
from typing import List

from lo.sdk.api.acquisition.io.open import open as lo_open

class OWLOFileReader(OWWidget):
    name = "LO File Loader"
    description = "Opens a Living Optics .lo file to allow reading of the spectral data and preview image"
    icon = "icons/mywidget.svg"
    priority = 55
    keywords = "livingoptics"
    
    class Outputs:
        spectral_data = Output("Spectra", Table)
        preview_data = Output("Preview", Table)
        
    class Error(OWWidget.Error):
        load_exception = Msg('Exception loading Living Optics processed file: {}')
        
    settingsHandler = settings.DomainContextHandler()
    lofile = settings.ContextSetting(None)
    recentFiles = settings.ContextSetting([])
    
    want_control_area = False
    
    def __init__(self):
        super().__init__()
        self.file_index = 0
        self.results = None
        self.sheet = 0 #Default to 0 unless there are >1 frames in the file
        self.populate_mainArea()        
        self.populate_comboboxes()
        self.reload()
    
    #This populates a drop-down in the File widget to let you select the frame to view.
    @property
    def sheets(self) -> List:
        sheet_list = []
        with lo_open(self.filename) as f:
            if len(f) > 1: #This is a file containing more than one frame
                for idx, frame in enumerate(f):
                    (metadata, _, _) = frame
                    sheet_list.append(f"{idx}, {metadata.timestamp_s}.{metadata.timestamp_us}")

        return sheet_list

    def load_lo_file(self):
        # Accommodate .lo files where there are multiple frames:
        # self.sheet is only set if there's >1 frame (?)
        if self.sheet:
            file_position = self.sheets.index(self.sheet)
            print(f"{self.sheet}, is at {file_position}")
            print(f"/n/n SHEETS /n{self.sheets}")
        else:
            file_position = 0

        with lo_open(self.lofile) as f:
            f.seek(file_position)
            (metadata, scene, spectra) = f.read()
            self.results = (metadata, scene, spectra)
        print(f"Metadata = {metadata}")


        # #Needs to return a data_table(data, headers). Headers are the wavelength results.
        # # Build a Domain to describe the spectra data
        # # 
        # my_domain = []
        # for w in metadata.wavelengths:
        #     my_domain.append(ContinuousVariable(f"{w}"))

        # domain = Domain(my_domain, metas=[ContinuousVariable("map_x"), ContinuousVariable("map_y")])
        # data = Table.from_numpy(domain, spectra, metas=metadata.sampling_coordinates)
        # return data

    def populate_mainArea(self):
        hb = gui.widgetBox(self.mainArea, orientation=Qt.Horizontal)
        self.filecombo = gui.comboBox(
            hb, self, "file_index", callback=self.select_lo_file, 
            minimumWidth=200)
        gui.button(hb, self, '...', callback=self.browse_lo_file,
            disabled=0, icon=self.style().standardIcon(QStyle.SP_DirOpenIcon),
            sizePolicy=(QSizePolicy.Maximum, QSizePolicy.Fixed)
        )

    def create_tables_from_results(self):
        if not self.results: return
        #Needs to return a data_table(data, headers). Headers are the wavelength results.
        # Build a Domain to describe the spectra data
        (metadata, scene, spectra) = self.results
        my_domain = []
        for w in metadata.wavelengths:
            my_domain.append(ContinuousVariable(f"{w}"))
        domain = Domain(my_domain, metas=[ContinuousVariable("map_x"), ContinuousVariable("map_y")])
        tableA = Table.from_numpy(domain, spectra, metas=metadata.sampling_coordinates)

        #Build a domain for the image table
        image_domain = []
        print(f"Scene shape is {scene.shape}")
        for y in range(scene.shape[1]):
            image_domain.append(ContinuousVariable(f"{y}"))
        domain = Domain(image_domain)
        tableB = Table.from_numpy(domain, np.squeeze(scene))
        return tableA, tableB

    def reload(self):
        if not self.lofile: return
        self.load_lo_file()
        if self.results: 
            tableA, tableB = self.create_tables_from_results()
            self.Outputs.spectral_data.send(tableA)
            self.Outputs.preview_data.send(tableB)
        
    def browse_lo_file(self, browse_demos=False):
        """user pressed the '...' button to manually select a file to load"""
        startfile = self.recentFiles[0] if self.recentFiles else '.'

        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open a Living Optics File', startfile,
            ';;'.join((".lo files (*.lo)",".lo files (*.lo)", "*.* (*)")))
        if not filename:
            return False

        if filename in self.recentFiles:
            self.recentFiles.remove(filename)
        self.recentFiles.insert(0, filename)

        self.populate_comboboxes()
        self.file_index = 0
        self.select_lo_file()
        return True
    
    def select_lo_file(self):
        """user selected a td file from the combo box"""
        if self.file_index > len(self.recentFiles) - 1:
            if not self.browse_lo_file(True):
                return  # Cancelled
        elif self.file_index:
            self.recentFiles.insert(0, self.recentFiles.pop(self.file_index))
            self.file_index = 0
            self.populate_comboboxes()
        if self.recentFiles:
            self.lofile = self.recentFiles[0]
            self.reload()

    def populate_comboboxes(self):
        self.filecombo.clear()
        for file in self.recentFiles or ("(None)",):
            self.filecombo.addItem(path.basename(file))
        self.filecombo.addItem("Browse Living Optics Files...")
        self.filecombo.updateGeometry()
        
        
if __name__ == "__main__":
    WidgetPreview(OWLOFileReader).run()
        