from GDSpy_Modules.gdspy_fucntions import *
from datetime import datetime
dt = datetime.now()

# # ------------------------------------------------------------------------
# #                       INPUT OPTIONS      
# # ------------------------------------------------------------------------

#Determine the fileformat
Save_file = True
dxf = True
invert = True


filename = "Chip_7_JJ1_Danbo"


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

# jj_manhattan_federico(cell, #this function will make both the capacitor pads and the arms
#       layer_manhattan = layers['JJ'],
#       position = (2000,2000), #position of the jj
#       capacitor_height = 460,
#       capacitor_width = 460,
#       arm_width = 3, # size of te arm
#       arm_length = 14.8,
#       arm_height = 4.5,
#       jj_length1 = 5.2,
#       jj_length2 = 4.5, 
#       jj_width = 0.30

k = np.linspace(0.03,0.5,48)
print(k)

v = k*1000
print(v)

for i in range(14):
      # size = gdspy.Text(f"{format_decimal_places(k[i], u)} um = {int(v[i])} nm", 2.25, (2000, 2100 + 50*i), layer = layers['JJ'] )
      # cell.add(size)
      for ii in range(7):
            jj_manhattan_federico(cell, #this function will make both the capacitor pads and the arms
                  layer_manhattan = layers['JJ'],
                  position = (1500 + 1000 * ii , 1500 + 500 * i), #position of the jj
                  capacitor_height = 460,
                  capacitor_width = 460,
                  arm_width = 3, # size of te arm
                  arm_length = 14.8,
                  arm_height = 4.5,
                  jj_length1 = 5.2,
                  jj_length2 = 4.3, 
                  jj_width = k[i*2+7])



# now we want to invert the design


# if invert == True
#     # Create rectangle covering the whole chip
#     point1_in = (0, 0)
#     point2_in = (chip_x, chip_y)
#     rectangle = gdspy.Rectangle(point1_in, point2_in, layer=5, datatype=0)
#     # Create inversion
#     inv = gdspy.boolean(rectangle, layer = 5, "not")



# # ------------------------------------------------------------------------
# #                       VIEW CHIP FUNCTIONS      
# # ------------------------------------------------------------------------

# View the layout using a GUI.
gdspy.LayoutViewer(cells=cell)

if Save_file:
      gds_file_name = os.path.join(path, '{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt, filename))
      gdspy.write_gds(gds_file_name, unit=1.0e-6, precision=1.0e-9)


