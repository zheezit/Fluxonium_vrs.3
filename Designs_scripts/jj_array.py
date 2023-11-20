from GDSpy_Modules.gdspy_fucntions import *
from datetime import datetime
dt = datetime.now()
import gdspy
import qiskit_metal
import os
# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------
# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------

#Determine the fileformat
Save_file = False
dxf = True
invert = True

path = r"C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium\Designs"
filename = "Viewer_jj_array"


cell1 = gdspy.Cell(f'{filename}')

layers = {'Frame':0,
            'Markers':1, 
            'Name_chip':2,
            'Feedline':3,
            'Resonators': 4,
            'JJ': 5,
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


jj_manhattan(cell, #this function will make both the capacitor pads and the arms
        layer_manhattan = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 460.0,
        capacitor_width = 460.0,
        arm_width = 3.0, # size of te arm
        arm_length = 14.8,
        arm_height = 4.5,
        pad_arm_length = 120,
        jj_length1 = 5.2,
        jj_length2 = 4.5, 
        jj_width = 0.30,
        jj_array_arm = 18,
        nr_junctions = 300,
        jj_array_width = 0.420,
        jj_array_distance_x = 2.5,
        )
# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS       
# # ------------------------------------------------------------------------

# View the layout using a GUI.
gdspy.LayoutViewer(cells=cell)    


