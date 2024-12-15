from Orange.data import Table
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget, Input, Output, Msg

from lo.sdk.api.acquisition.data.coordinates import NearestUpSample
import numpy as np

class UpsampleLO(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "Upsample"
    description = "Upsample a Living Optics spectral frame"
    icon = "icons/upsample.svg"
    priority = 100  # where in the widget order it will appear
    keywords = ["widget", "data"]
    want_main_area = False
    resizing_enabled = False
    
    originals = []

    class Inputs:
        # specify the name of the input and the type
        in_data = Input("Data", Table)

    class Outputs:
        # if there are two or more outputs, default=True marks the default output
        out_data = Output("Data", Table, default=True)
        originals = Output("Sparse Data", Table)
    
    upsample_dimension = Setting("640")
  
    # same class can be initiated for Error and Information messages
    class Warning(OWWidget.Warning):
        warning = Msg("My warning!")

    def __init__(self):
        super().__init__()
        self.data = None
        
        self.label_box = gui.comboBox(
            self.controlArea, 
            self, 
            "upsample_dimension",
            label="Select Target Output Size", 
            items=("1920", "960", "640", "480"),
            sendSelectedValue=True,
            callback=self.changeSetting
        )
    

    @Inputs.in_data
    def set_data(self, in_data):
        if in_data is not None: #This is where the data processing happens?

            self.originals = in_data # Pass through the unmolested data
            self.in_data = in_data

            print(f"Refreshing data: Shape of data is now: {np.shape(self.in_data)}")
            # extract the sampling_coordinates from the metadata on self.data
            sampling_coordinates = in_data.metas #since that's the coordinates in the LO data, unless we go and mess that up somewhere else. 
            upsample_dimension = int(self.upsample_dimension)
            sampling_scale = upsample_dimension/1920 #Maximum size is 1920, hard coded.
            print(f"Upsample to {upsample_dimension}, using scale {sampling_scale}")

            upsampler = NearestUpSample(
                sampling_coordinates, 
                output_shape=(upsample_dimension, upsample_dimension), 
                origin=(64, 256), 
                scale = sampling_scale
            )
            upsampled_cube = upsampler(in_data.X)
            print(f"upsampled_cube shape is {upsampled_cube.shape}")

            #convert the upsampled cube into a table.             
            domain = in_data.domain 
            
            # Need to reshape the x,y,λ data into (loc, λ) where loc is the sampled coords
            # Do the sample coordinates first. Need to use 'ij' indexing style since
            # meshgrid makes an NxM matrix from np.meshgrid(M,N) because python. 
            # If you allow the default (xy indexing), any mismatch in array dimensions (i.e. if it's non-square) 
            # causes the output to be all skewed.
            x,y = np.meshgrid(np.arange(upsampled_cube.shape[0]),np.arange(upsampled_cube.shape[1]), indexing='ij')
            x = x.reshape(-1)
            y = y.reshape(-1)
            #Need to get x,y into the right format, which is stuck together and then transposed
            coordinates = np.array([x,y]).T 
            print(f"coordinate array shape {coordinates.shape}")
            #Then do the cube
            reshaped_cube = upsampled_cube.reshape(-1,upsampled_cube.shape[2])
            self.out_data = Table.from_numpy(domain, reshaped_cube, metas=coordinates)  
            
            print(f"Shape of data is now: {np.shape(self.out_data)}")
            
        else:
            self.out_data = None

        self.Outputs.out_data.send(self.out_data)
        self.Outputs.originals.send(self.originals)
    def changeSetting(self):
        self.set_data(self.in_data)

    def commit(self):
        #out_data = self.set_data(self.originals) #Update the contents, using the data that were originally passed in to make sure we don't keep making it smaller. 
        
        #TODO Need to use fresh original data each time this is done. Currently we're recycling the data object, so it gets downsampled each time by the look of things.
        
        self.Outputs.data.send(out_data)
        self.Outputs.originals.send(self.originals)
    
    def send_report(self):
        # self.report_plot() includes visualizations in the report
        self.report_caption(self.label)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(UpsampleLO).run()
