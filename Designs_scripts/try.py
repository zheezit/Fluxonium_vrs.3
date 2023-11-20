from GDSpy_Modules.gdspy_fucntions import *
from datetime import datetime
dt = datetime.now()

# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------

#Determine the fileformat
Save_file = False
dxf = True

path = r"C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium\Designs"
filename = "Chip_5_jj1"


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


for in range()
pads(cell, #this function will make both the capacitor pads and the arms
         layer_pads = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 460,
        capacitor_width = 460,
        arm_width = 3, # size of te arm
        arm_length = 14.8,
        arm_height = 4.5,)



# Optionally, view the layout using the GDSII viewer
# gdspy.LayoutViewer(layout_filename)
# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS      
# # ------------------------------------------------------------------------
   
# View the layout using a GUI.
gdspy.LayoutViewer(cells=cell)


if Save_file:
      gds_file_name = os.path.join(path, '{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt, filename))
      gdspy.write_gds(gds_file_name, unit=1.0e-6, precision=1.0e-9)

