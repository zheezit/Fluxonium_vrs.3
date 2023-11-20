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

filename = "Chip_x_Fluxonium"


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


feedline(cell, 
             layer_feedline = layers['Feedline'],
             position_feedline = (0,0),
             thickness_bondingpath1 = 636.6,
             size_feedline1 = 468.3,
             angle_feedline1 = 99.75,
             thickness_feedline1 = 22.7,
             length_feedline1 = 6200, 
             thickness_bondingpath2 = 300,
             size_feedline2 = 300,
             angle_feedline2 = 100,
             thickness_feedline2 = 10.7,
             length_feedline2 = 6200,            
             seperation_length = 168.3)


#Resonator 5
resonator_lambda4_drive(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 1161,    #Change from here
               location_y = True,
               seperation_length = 5,
               coupler_length = 250,
               middle_length = 450,
               nr_turns = 8, 
               total_length = 4624,
               )




k = np.linspace(0.03,0.5,48)

capacitor_dim = 400.0

for i in range(10):
      for ii in range(6):
            jj_manhattan(cell, #this function will make both the capacitor pads and the arms
            layer_manhattan = 5,
            position = (1650 + ii*1120 , 1400 + 450 * i), #position of the jj
            capacitor_height = capacitor_dim,
            capacitor_width = capacitor_dim,  
            arm_width = 3.0, # size of te arm
            jj_arm_length = 14.8,
            arm_height = 4.5,
            pad_arm_length = 120,
            jj_length1 = 5.2,
            jj_length2 = 4.5, 
            jj_width = k[i*4 + 1],
            jj_array_arm = 18,
            nr_junctions = 300,
            jj_array_width = 0.420,
            jj_array_distance_x = 2.5,
            )


for i in range(6):
     for ii in range(6):
      jj_manhattan_array(cell, #this function will make both the capacitor pads and the arms
            layer_manhattan = 5,
            position = (1650 + ii*1120, 5900 + 450 * i), #position of the jj
            capacitor_height = capacitor_dim,
            capacitor_width = capacitor_dim,
            arm_width = 3.0, # size of te arm
            jj_arm_length = 14.8,
            arm_height = 4.5,
            pad_arm_length = 120,
            jj_length1 = 5.2,
            jj_length2 = 4.5, 
            jj_width = 0.30,
            jj_array_arm = 18,
            nr_junctions = 30 + i*6*4,
            jj_long = 12, 
            jj_short = 6,
            jj_array_width = 0.420,
            jj_array_distance_x = 2.5,
            jj_array_distance_y = 3,
            jj_array_arm_width = 1.5, )  
      

# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS      
# # ------------------------------------------------------------------------

# View the layout using a GUI.
gdspy.LayoutViewer(cells=cell)    

if Save_file:
      gds_file_name = os.path.join(path, '{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt, filename))
      gdspy.write_gds(gds_file_name, unit=1.0e-6, precision=1.0e-9)



