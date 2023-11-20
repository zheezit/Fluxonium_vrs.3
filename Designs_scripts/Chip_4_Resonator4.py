from GDSpy_Modules.gdspy_fucntions import *
from datetime import datetime
dt = datetime.now()

# # ------------------------------------------------------------------------
# #                       Design scripts      
# # ------------------------------------------------------------------------



# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------

#Determine the fileformat
Save_file = False
dxf = True

filename = "Chip_4_Resonator4"


cell1 = gdspy.Cell(f'{filename}')
    
layers = {'Frame':0,
            'Markers':1, 
            'Name_chip':2,
            'Feedline':3,
            'Resonators': 4,
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

#Resonator 1
resonator_lambda2(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 840,    #Change from here
               location_y = True,
               seperation_length = 18,
               coupler_length = 440,
               middle_length = 500,
               nr_turns = 12, 
               total_length = 8918,
               )

#Resonator 2
resonator_lambda2(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 2261,    #Change from here
               location_y = True,
               seperation_length = 16,
               coupler_length = 440,
               middle_length = 458,
               nr_turns = 14, 
               total_length = 9631,
               )

#Resonator 3
resonator_lambda2(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 3679,    #Change from here
               location_y = True,
               seperation_length = 4,
               coupler_length = 475,
               middle_length = 492,
               nr_turns = 16, 
               total_length = 11466,
               )

#Resonator 4
resonator_lambda2(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 5105,    #Change from here
               location_y = True,
               seperation_length = 17,
               coupler_length = 510,
               middle_length = 510,
               nr_turns = 14, 
               total_length = 10470,
               )

#Resonator 5
resonator_lambda4_d(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 1161,    #Change from here
               location_y = False,
               seperation_length = 19,
               coupler_length = 354,
               middle_length = 330,
               nr_turns = 8, 
               total_length = 4624,
               )

#Resonator 6
resonator_lambda4_d(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 2546,    #Change from here
               location_y = False,
               seperation_length = 16,
               coupler_length = 384,
               middle_length = 360,
               nr_turns = 8, 
               total_length = 5016.3,
               )

#Resonator 7
resonator_lambda4_d(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 3930,    #Change from here
               location_y = False,
               seperation_length = 20.5,
               coupler_length = 419,
               middle_length = 398,
               nr_turns = 6, 
               total_length = 4304,
               )

#Resonator 8
resonator_lambda4_d(cell, 
               layer_resonator = layers['Resonators'], 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 5371,    #Change from here
               location_y = False,
               seperation_length = 14.5,
               coupler_length = 334,
               middle_length = 310,
               nr_turns = 10, 
               total_length = 5471,
               )

# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS      
# # ------------------------------------------------------------------------
   
# View the layout using a GUI.
gdspy.LayoutViewer(cells=cell)

if Save_file:
      gds_file_name = os.path.join(path, '{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt, filename))
      gdspy.write_gds(gds_file_name, unit=1.0e-6, precision=1.0e-9)

