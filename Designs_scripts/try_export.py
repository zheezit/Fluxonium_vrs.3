import numpy as np
import gdspy
import gdshelpers
import sys
import os
import datetime
import ezdxf    

from Modules.gdspy_fucntions import *
from datetime import datetime
dt = datetime.now()

# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------

cell1 = gdspy.Cell('Chip_1')
    
layers = {'Frame':0,
            'Markers':1, 
            'Bonding_path':2,
            'another': 3
            }

# Determine the chip dimensions in um
design_x = 8000.0
design_y = 8000.0

# Determine the diced chip dimensions in um
chip_x = 10000.0
chip_y = 10000.0

#Determine the number of markers
N = 9
#Determine the spacing between the markers: 
spacing_markers = 200


# # ------------------------------------------------------------------------
# #                       CALL FUNCTIONS      
# # ------------------------------------------------------------------------
         

cell = cell1
name = cell.name

frame(cell,
      layer_frame = layers['Frame'], 
      position_frame = (0,0),
      design_size = 8000.0,
      chip_size = 10000.0,
      thickness_frame = 10.0)

markers(cell,
        position_marker = (1000,1000),
        length = 10000.0,
        width = 10000.0,
        layer_markers = 1,
        Numer_markers = N)

name_chip(cell, layer_name = 0, position_name = (0,0))

feedline(cell, layer_feedline = 2, position_feedline = (0,0))

    
# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS      
# # ------------------------------------------------------------------------
   
# View the layout using a GUI.
gdspy.LayoutViewer(cells=cell1)