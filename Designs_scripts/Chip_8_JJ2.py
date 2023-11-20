from GDSpy_Modules.gdspy_fucntions import *
from datetime import datetime
dt = datetime.now()
import qiskit_metal
import os
# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------

#Determine the fileformat
Save_file = True
dxf = True
invert = True

filename = "Chip_8_JJ2"


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

frame(cell,
      layer_frame = layers['Frame'], 
      position_frame = (0,0),
      design_size = design_x,
      chip_size = chip_x,
      thickness_frame = 10.0)

markers(cell,     
      position_marker = (1000,1000),
      length = chip_x,
      width = chip_y,
      layer_markers = layers['Markers'],
      Numer_markers = N)

name_chip(cell, 
      layer_name = layers['Name_chip'], 
      position_name = (0,0),
      fond_size = 20)



jj_manhattan(cell, #this function will make both the capacitor pads and the arms
        layer_manhattan = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 460.0,
        capacitor_width = 460.0,
        arm_width = 3.0, # size of te arm
        arm_length = 14.8,
        arm_height = 4.5,
        jj_length1 = 5.2,
        jj_length2 = 4.5, 
        jj_width = 0.30,)



# jj_manhattan(cell, #this function will make both the capacitor pads and the arms
#         layer_manhattan = 5,
#         position = (2000,2000), #position of the jj
#         capacitor_height = 460.0,
#         capacitor_width = 460.0,
#         arm_width = 3.0, # size of te arm
#         arm_length = 14.8,
#         arm_height = 4.5,
#         pad_arm_length = 120,
#         jj_length1 = 5.2,
#         jj_length2 = 4.5, 
#         jj_width = 0.30,)



# multi_path = gdspy.Path(2, (-3, -2))
# multi_path.segment(4, "+x")
# multi_path.turn(2, "l").turn(2, "r")
# multi_path.segment(4)
      
# # # Create a copy with joined polygons and no fracturing
# # joined = gdspy.boolean(multi_path, None, "or", max_points=0)
# # joined.translate(0, -5)

# # Fillet applied to each polygon in the path
# multi_path.fillet(0.5)

# # Fillet applied to the joined copy
# joined.fillet(0.5)

# cell.add(multi_path)
# cell.add(joined)

# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS      
# # ------------------------------------------------------------------------

# View the layout using a GUI.
# gdspy.LayoutViewer(cells=cell)    

if Save_file:
      gds_file_name = os.path.join(path, '{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt, filename))
      gdspy.write_gds(gds_file_name, unit=1.0e-6, precision=1.0e-9)



