"""
Created on Sun June 10th 2023
@author: Amalie Terese Jiao Paulsen
@e-mail: jiaopaulsen@gmail.com
"""

import numpy as np
import gdspy
import gdshelpers
import sys
import os
import datetime
import ezdxf    

# sys.path.append('C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium\python\Designs_gds')

print(' Using gdspy module version ' + gdspy.__version__)

# ------------------------------------------------------------------------
#                       INPUT OPTIONS      
# ------------------------------------------------------------------------


cell1 = gdspy.Cell('Resonator_Chip_1')
    
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


# ------------------------------------------------------------------------
#                       COMPONENTS      
# ------------------------------------------------------------------------

"""
Created on Sun June 10th 2023
@author: Amalie Terese Jiao Paulsen
@e-mail: jiaopaulsen@gmail.com
"""
import numpy as np
import gdspy
import gdshelpers
import sys
import os
import datetime
import ezdxf    
print(' Using gdspy module version ' + gdspy.__version__)

# ------------------------------------------------------------------------
#                       COMPONENTS      
# ------------------------------------------------------------------------

def frame(cell,
          layer_frame = 0,
          position_frame = (0,0),
          design_size = 8000.0,
          chip_size = 10000.0,
          thickness_frame = 10.0):
    '''
    The Chip area is 10x10mm.
    The Design area is 8x8 mm. (actually 7.4x7.4mm (in order to fit into the board))
    '''
    p1_out = (position_frame[0]-thickness_frame,position_frame[1]-thickness_frame)
    p2_out = (position_frame[0]+ chip_size + thickness_frame,position_frame[1]+ chip_size + thickness_frame)
    outer = gdspy.Rectangle(p1_out,p2_out, layer = layer_frame, datatype=0)

    p1_in = (position_frame[0],position_frame[1])
    p2_in = (chip_size,chip_size)
    inner =  gdspy.Rectangle(p1_in,p2_in, layer = layer_frame, datatype=0)
    frame = gdspy.boolean(outer, inner, "not")
    # frame = gdspy.fast_boolean(outer, inner, 'xor', layer=layer_frame, datatype=0)
    cell.add(frame)

def cross(cell,
          layer_cross = 0,
          position_cross = (0,0),
          length_cross = 0,
          thickness_cross = 0):
    '''
    A cross
    '''
    cross_leg_1 = gdspy.Path(thickness_cross, (position_cross[0]-length_cross/2, position_cross[1]))
    cross_leg_1.segment(length_cross, '+x')
    
    cross_leg_2 = gdspy.Path(thickness_cross, (position_cross[0], position_cross[1]-length_cross/2))
    cross_leg_2.segment(length_cross, '+y')
    cross = gdspy.boolean(cross_leg_1, cross_leg_2, 'or', layer=layer_cross)
    return cross

def markers(cell,
             position_marker = (1000,1000),
             length = 10000.0,
             width = 10000.0,
             layer_markers = 1,
             Numer_markers = 9):
    # Markers for a square chip
    marker_separation = 200.0
    marker_line_sep = 2.5
    #Parameters for automatic alignment
    thickness_automatic = 2.5
    length_automatic = 150 # 67.5
    # Parameters for manual alignment: 
    thickness_manual = 0.5
    length_manual = 10
    #Determine all the positions of the markers
    k = []
    count = []
    set = np.array(np.arange(0, Numer_markers, 1))
    list = np.array([[0,0],[0,marker_separation],[marker_separation,0],[0,-marker_separation],[-marker_separation,0],[0,marker_separation*2],[marker_separation*2,0],[0,-marker_separation*2],[-marker_separation*2,0]])
    for i in set:
        # print(i)
        k.append([[1000,1000]+list[i],[9000,1000]+list[i],[1000,9000]+list[i],[9000,9000]+list[i]])
    k = np.array(k)
    #Generate markers and put them into the defined positions
    for i in range(len(k)):
        for ii in range(len(k[0])):
            #Define the manual markers
            markers_manual = cross(cell,
                                    layer_cross = layer_markers,  
                                    position_cross = (k[i][ii][0], k[i][ii][1]),
                                    length_cross = length_manual,
                                    thickness_cross = thickness_manual)

            #Define the automatic markers
            square_automatic =  gdspy.Rectangle((k[i][ii][0]-7.5,k[i][ii][1]-7.5),(k[i][ii][0]+7.5,k[i][ii][1]+7.5), layer = layer_markers)
            cross_automatic = cross(cell,
                                        layer_cross = layer_markers,
                                        position_cross = (k[i][ii][0],k[i][ii][1]),
                                        length_cross = length_automatic,
                                        thickness_cross = thickness_automatic)
            markers_automatic = gdspy.boolean(cross_automatic,square_automatic,'not')
            count = gdspy.Text("{}".format(i), 8, (k[i][ii][0]+6, k[i][ii][1]-15), layer=layer_markers)
            #now you just need to add the count
            marker = gdspy.boolean(markers_automatic,markers_manual,'or', layer = layer_markers)
            cell.add(marker)  
            cell.add(count) 

def name_chip(cell, 
              layer_name = 2, 
              position_name = (0,0),
              fond_size = 200):
    name = gdspy.Text("{}".format(cell.name), fond_size, (position_name[0]+2000, -position_name[1]+500), layer=layer_name)
    size_name = name.get_bounding_box()[1][0]
    Qdev = gdspy.Text("SQuID Lab, QDev", fond_size, (position_name[0]+size_name + 500, position_name[1]+500), layer=layer_name)
    cell.add(Qdev)
    cell.add(name)

def feedline(cell, 
             layer_feedline = 3,
             position_feedline = (0,0),
             thickness_bondingpath1 = 636.6,
             size_feedline1 = 468.3,
             angle_feedline1 = 99.75,
             thickness_feedline1 = 16.7,
             length_feedline1 = 6200, 
             thickness_bondingpath2 = 300,
             size_feedline2 = 300,
             angle_feedline2 = 100,
             thickness_feedline2 = 10.7,
             length_feedline2 = 6200,            
             seperation_length = 168.3):
    seperation_chip = 10000/2 - ((thickness_bondingpath2 + seperation_length +angle_feedline1)*2  + length_feedline1)/2
    #Define the outer feedline curvature
    path1 = gdspy.Path(thickness_bondingpath1, (position_feedline[0] + seperation_chip, position_feedline[1] + 5000)).segment(size_feedline1,"+x").segment(angle_feedline1,"+x", final_width = thickness_feedline1)
    path1.segment(length_feedline1,"+x")
    path1.segment(angle_feedline1,"+x", final_width = thickness_bondingpath1)
    path1.segment(size_feedline1,"+x")
    #Define the inner feedline curvature
    path2 = gdspy.Path(thickness_bondingpath2, (position_feedline[0] + seperation_chip + seperation_length, position_feedline[1] + 5000)).segment(size_feedline2,"+x").segment(angle_feedline2,"+x", final_width = thickness_feedline2)
    path2.segment(length_feedline2,"+x")
    path2.segment(angle_feedline2,"+x", final_width = thickness_bondingpath2)
    path2.segment(size_feedline2,"+x")
    #Use the boolean function to substract the two curvatures
    total_feedline = gdspy.boolean(path1,path2,"not", layer = layer_feedline)
    cell.add(total_feedline)

def resonators(cell, 
               layer = 4, 
               resistance = 50, ):
    i = 4
    return i



# ------------------------------------------------------------------------
#                       CALL FUNCTIONS      
# ------------------------------------------------------------------------
         

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
        layer_markers = layers['Markers'],
        Numer_markers = N)

name_chip(cell, 
          layer_name = layers['Name_chip'], 
          position_name = (0,0),
          fond_size = 200)

feedline(cell, 
             layer_feedline = layers['Feedline'],
             position_feedline = (0,0),
             thickness_bondingpath1 = 636.6,
             size_feedline1 = 468.3,
             angle_feedline1 = 99.75,
             thickness_feedline1 = 16.7,
             length_feedline1 = 6200, 
             thickness_bondingpath2 = 300,
             size_feedline2 = 300,
             angle_feedline2 = 100,
             thickness_feedline2 = 10.7,
             length_feedline2 = 6200,            
             seperation_length = 168.3)

# resonators(cell, )

    
# ------------------------------------------------------------------------
#                       VIEW CHIP FUNCTIONS      
# ------------------------------------------------------------------------
         
# View the layout using a GUI.
gdspy.LayoutViewer(cells=cell1)