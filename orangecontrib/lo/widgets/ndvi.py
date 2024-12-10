from Orange.data import Table, Domain, ContinuousVariable
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget, Input, Output, Msg

from lo.sdk.api.analysis.overlays import NDVI as calculate_NDVI
import numpy as np

class NDVI(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "Calculate NDVI"
    description = "Calculate NDVI (or band ratios) from a list of spectra"
    icon = "icons/ndvi.svg"
    priority = 100  # where in the widget order it will appear
    keywords = ["widget", "data"]
    want_main_area = False
    resizing_enabled = False
    

    class Inputs:
        # specify the name of the input and the type
        data = Input("Data", Table)

    class Outputs:
        # if there are two or more outputs, default=True marks the default output
        data = Output("Data", Table, default=True)
    
    #Enable the user to set the bands so it's not just NDVI that's possible.
    band1_start = Setting("")
    band1_end = Setting("")
    band2_start = Setting("")
    band2_end = Setting("")
  
    # same class can be initiated for Error and Information messages
    class Warning(OWWidget.Warning):
        warning = Msg("My warning!")

    def __init__(self):
        super().__init__()
        self.data = None
        self.band1_start = gui.lineEdit(
            self.controlArea, 
            self, 
            "band1_start", 
            label="Band 1 start wavelength", 
            callback=self.commit
        )

        self.band1_end = gui.lineEdit(
            self.controlArea, 
            self, 
            "band1_end", 
            label="Band 1 end wavelength", 
            callback=self.commit
        )

        self.band2_start = gui.lineEdit(
            self.controlArea, 
            self, 
            "band2_start", 
            label="Band 2 start wavelength", 
            callback=self.commit
        )

        self.band2_end = gui.lineEdit(
            self.controlArea, 
            self, 
            "band2_end", 
            label="Band 2 end wavelength", 
            callback=self.commit
        )

        self.reset_limits_button = gui.button(
            self.controlArea, 
            self, 
            label="Reset Band Limits", 
            callback=self.reset_limits
        )

        self.reset_limits() #Run this to set the values to their defaults when the widget is instantiated.

        # self.label_box = gui.comboBox(
        #     self.controlArea, 
        #     self, 
        #     "upsample_dimension",
        #     label="Select Target Output Size", 
        #     items=("1920", "960", "640", "480"),
        #     sendSelectedValue=True,
        #     callback=self.commit
        # )
    

    @Inputs.data
    def set_data(self, data):
        if data is not None: 

            # extract the sampling_coordinates from the metadata on self.data
            sampling_coordinates = data.metas #since that's the coordinates in the LO data, unless we go and mess that up somewhere else. 
            band1_start = int(self.band1_start)
            band1_end = int(self.band1_end)
            band2_start = int(self.band2_start)
            band2_end = int(self.band2_end)

            wavelengths = np.array([float(var.name) for var in data.domain.variables])
            ndvi_list_a= calculate_NDVI(
                data.X, 
                wavelengths, 
                (band1_start, band1_end), 
                (band2_start, band2_end)
            )
            ndvi_list = np.array([ndvi_list_a, ndvi_list_a]) #Hack to make the data 2D
            # Convert the domain from one containing spectra to one containing a single number per point.
            # First build a new domain           
            my_domain = [ContinuousVariable("Band Ratio"), ContinuousVariable("Band Ratio 2")]
            domain = Domain(my_domain, metas=[ContinuousVariable("map_x"), ContinuousVariable("map_y")])

            #Then transfer data into it
            print(f"Shape of ndvi data is {ndvi_list.shape}")

            self.data = Table.from_numpy(domain, ndvi_list.T, metas=sampling_coordinates)  
        else:
            self.data = None

        self.Outputs.data.send(self.data)
    def reset_limits(self):
        #Reset the band start and stop values to their default (NDVI values)
        self.band1_start = 650
        self.band1_end = 850
        self.band2_start = 785
        self.band2_end = 900
        self.commit() 

    def commit(self):
        self.set_data(self.data) #Update the contents.
        self.Outputs.data.send(self.data)

    
    def send_report(self):
        # self.report_plot() includes visualizations in the report
        self.report_caption(self.label)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(NDVI).run()
