from GDSpy_Modules.gdspy_fucntions import *
from datetime import datetime
dt = datetime.now()
import qiskit_metal
import os
import cdes
# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------

#Determine the fileformat
Save_file = True
dxf = True
invert = True

path = r"C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium\Designs"
filename = "Wafer_2023_10_22"


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
positions = np.array([])
for k in range(10):
    for l in range(10):
         for m in range(10):
              for n in range(10):
                position = (0,0)
                positions.add(position) 

# for i in range(10):
#      frame(cell,
#             layer_frame = layers['Frame'], 
#             position_frame = positions[i],
#             design_size = design_x,
#             chip_size = chip_x,
#             thickness_frame = 3.0)


print(positions)

# wafer(cell,
#           radius = 25400,#given in micrometer
#           layer = 0,)

# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS      
# # ------------------------------------------------------------------------

# # View the layout using a GUI.
# gdspy.LayoutViewer(cells=cell)

# if Save_file:
#       gds_file_name = os.path.join(path, '{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt, filename))
#       gdspy.write_gds(gds_file_name, unit=1.0e-6, precision=1.0e-9)



