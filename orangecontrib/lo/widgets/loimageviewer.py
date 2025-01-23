import os
from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QLabel, QVBoxLayout, QFileDialog
from AnyQt.QtGui import QPixmap
from Orange.widgets.widget import OWWidget, Input
from Orange.widgets import gui
from Orange.data import Table
from Orange.data import Table, Domain, ContinuousVariable
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget, Input, Output, Msg

import numpy as np

class LOImageViewer(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "LOImageViewer"
    description = "View LO Hyperspectral data overlaid with the preview image"
    icon = "icons/mywidget.svg"
    priority = 60  # where in the widget order it will appear
    keywords = ["widget", "data"]
    want_main_area = False
    resizing_enabled = False

    class Inputs:
        data = Input("Data", Table)
        image = Input("Data", Table)


    def __init__(self):
        super().__init__()
        self.data = None
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # Layout
        # self.mainArea.layout().addWidget(self.image_label)
        # gui.button(self.controlArea, self, "Select Image", callback=self.select_image)
        image_box = gui.widgetBox(self.mainArea, orientation=Qt.Horizontal)
        self.image_button = gui.button(image_box, self, 'Image Button')
        
    @Inputs.data
    def set_data(self, data: Table):
        """Handle new data input."""
        if data is not None:
            self.data = data
        if image is not None:
            self.image = image

    def select_image(self):
        if self.data is None:
            self.image_label.setText("No Data Available")
            return

        # Extract file paths from the first column
        file_paths = [str(row[0]) for row in self.data]
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", os.path.dirname(file_paths[0]), "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path and os.path.exists(file_path):
            self.display_image(file_path)
        else:
            self.image_label.setText("Invalid File Selected")

    def display_image(self, file_path):
        """Display the selected image."""
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.image_label.setText("Failed to Load Image")
        else:
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), aspectMode=Qt.KeepAspectRatio))

if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    ow = LOImageViewer()
    ow.show()
    app.exec_()
    '''

#     class Inputs:
#         # specify the name of the input and the type
#         spectra = Input("Spectra", Table)
#         scene = Input("Scene", Table)

#     class Outputs:
#         # if there are two or more outputs, default=True marks the default output
#         out_data = Output("Data", Table, default=True)
    
   
#     # same class can be initiated for Error and Information messages
#     class Warning(OWWidget.Warning):
#         warning = Msg("My warning!")

#     def __init__(self):
#         super().__init__()
#         self.spectra = None
#         self.scene = None
#         # self.label_box = gui.comboBox(
#         #     self.controlArea, 
#         #     self, 
#         #     "upsample_dimension",
#         #     label="Select Target Output Size", 
#         #     items=("1920", "960", "640", "480"),
#         #     sendSelectedValue=True,
#         #     callback=self.commit
#         # )
    

#     @Inputs.spectra
#     def set_data(self, in_data):
#         if in_data is not None: 
#             self.in_data = in_data
#             # extract the sampling_coordinates from the metadata on self.data
#             sampling_coordinates = in_data.metas #since that's the coordinates in the LO data, unless we go and mess that up somewhere else. 

#             wavelengths = np.array([float(var.name) for var in in_data.domain.variables])
           
#             # Convert the domain from one containing spectra to one containing a single number per point.
#             # First build a new domain           
#             my_domain = [ContinuousVariable("Band Ratio"), ContinuousVariable("Band Ratio 2")]
#             domain = Domain(my_domain, metas=[ContinuousVariable("map_x"), ContinuousVariable("map_y")])

#             #Then transfer data into it
#             print(f"Shape of ndvi data is {ndvi_list.shape}")
#             #TODO: Confirm whether this needs to be 'self.data' or just plain old 'data'. Might be the source of the errors. 
#             self.out_data = Table.from_numpy(domain, ndvi_list.T, metas=sampling_coordinates)  
#         else:
#             self.out_data = None
#         self.Outputs.out_data.send(self.out_data)
    

#     def commit(self):
#         self.set_data(self.spectra, self.scene) #Update the contents.
#         self.Outputs.out_data.send(self.out_data)

    
#     def send_report(self):
#         # self.report_plot() includes visualizations in the report
#         self.report_caption(self.label)


# if __name__ == "__main__":
#     from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
#     WidgetPreview(LOImageViewer).run()






'''