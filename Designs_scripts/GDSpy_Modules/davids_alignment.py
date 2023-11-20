"""
Created on Mon Oct 18th 10:27 2022

@author: David Feldstein i Bofill
@e-mail: dfeldstein98@gmail.com
"""

import numpy as np
import gdspy

print('Using gdspy module version ' + gdspy.__version__)

# ------------------------------------------------------------------------
#                       INPUT OPTIONS      
# ------------------------------------------------------------------------

Status = 'fabrication'
res_fullgap = 'Fine'
dxf = True
Box = False
Output = True

filename = 'Markers_ebeam'
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#                       PARAMETERS      
# ------------------------------------------------------------------------

if __name__ == '__main__':

    cell_example = gdspy.Cell('Example_meander')
    
    layers = {'Markers':0,
              'Frame':1
             }

    # Determine the chip dimensions in um
    chip_x = 8000.0
    chip_y = 8000.0

    # Determine the diced chip dimensions in um
    dice_chip_x = 10000.0
    dice_chip_y = 10000.0

    # Rectangle width
    t_rectangle = 60.0

    

# ------------------------------------------------------------------------

    
# ------------------------------------------------------------------------
#                       COMPONENTS      
# ------------------------------------------------------------------------

def dicing_rectangle(cell,
                     position = (0,0),
                     length = 8000.0,
                     width = 10000.0,
                     thickness = 100.0,
                     layer_rectangle = 0):
        
    '''
    A 8x8 mm rectangle surrounding everything.
    '''
    # Frame
    X = length/2
    Y = width/2
    point1_out = (position[0]-X-thickness,position[1]-Y-thickness)
    point2_out = (position[0]+X+thickness, position[1]+Y+thickness)
    point1_in = (position[0]-X, position[1]-Y)
    point2_in = (position[0]+X, position[1]+Y)
    outer = gdspy.Rectangle(point1_out, point2_out, layer=layer_rectangle, datatype=0)
    inner = gdspy.Rectangle(point1_in, point2_in, layer=layer_rectangle, datatype=0)
    frame = gdspy.fast_boolean(outer, inner, 'xor', layer=layer_rectangle, datatype=0)
    cell.add(frame)



def cross_fun(cell,
         position_cross = (0,0),
         length_cross = 0,
         thickness_cross = 0,
         layer_cross = 0):
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
             position = (0,0),
             length = 10000.0,
             width = 10000.0,
             layer_markers_man = 0,
             layer_markers_aut = 0):
    
    # Markers for a square chip
    marker_separation = 200.0
    marker_line_sep = 3.0
    thickness_line = 2.5
    length_line = 83.0
    length_cross = 10
    thickness_cross = 0.4
    
    markers_all_man = cross_fun(cell,
                     position_cross = (position[0]+length/2,position[1]+chip_y/2),
                     length_cross = length_cross,
                     thickness_cross = thickness_cross,
                     layer_cross = layer_markers_man)
    
    length_line_bare = 2*length_line+length_cross+2*marker_line_sep
    markers_all_auto = cross_fun(cell,
                             position_cross = (position[0]+length/2,position[1]+chip_y/2),
                             length_cross = length_line_bare,
                             thickness_cross = thickness_line,
                             layer_cross = layer_markers_aut)

    bb_0 = np.array(markers_all_man.get_bounding_box())
    marker_box_0 = gdspy.Rectangle(bb_0[0]-marker_line_sep, bb_0[1]+marker_line_sep, layer=layer_markers_aut)
    markers_all_auto = gdspy.boolean(markers_all_auto, marker_box_0, 'not', layer=layer_markers_aut, datatype=0)

    for ii in range(2):
        for jj in range(2):
            for kk in range(5):
                # Cross and cross labels
                position_ky = ((-1)**ii*length/2+position[0],(-1)**jj*length/2+marker_separation*kk+position[1])
                position_kx = ((-1)**ii*length/2+marker_separation*kk+position[0],(-1)**jj*length/2+position[1])
                crossy = cross_fun(cell,
                             position_cross = position_ky,
                             length_cross = length_cross,
                             thickness_cross = thickness_cross,
                             layer_cross = layer_markers_man)

                markers_all_man = gdspy.boolean(markers_all_man, crossy, 'or', layer=layer_markers_man, datatype=0)
                
                # Add text
                texty = gdspy.Text('{}'.format(kk+1), 8, (position_ky[0]+6,position_ky[1]-15),layer = layer_markers_man)
                markers_all_man = gdspy.boolean(markers_all_man, texty, 'or', layer=layer_markers_man, datatype=0)
                crossx = cross_fun(cell,
                             position_cross = position_kx,
                             length_cross = length_cross,
                             thickness_cross = thickness_cross,
                             layer_cross = layer_markers_man)

                markers_all_man = gdspy.boolean(markers_all_man, crossx, 'or', layer=layer_markers_man, datatype=0)
                textx = gdspy.Text('{}'.format(kk+1), 8, (position_kx[0]+6,position_kx[1]-15),layer = layer_markers_man)
                markers_all_man = gdspy.boolean(markers_all_man, textx, 'or', layer=layer_markers_man, datatype=0)
                
                
                length_line_bare = 2*length_line+length_cross+2*marker_line_sep
                cross_lines_barex = cross_fun(cell,
                                         position_cross = position_kx,
                                         length_cross = length_line_bare,
                                         thickness_cross = thickness_line,
                                         layer_cross = layer_markers_aut)
                
                bbx = np.array(crossx.get_bounding_box())
                marker_boxx = gdspy.Rectangle(bbx[0]-marker_line_sep, bbx[1]+marker_line_sep, layer=layer_markers_aut)
                cross_linesx = gdspy.boolean(cross_lines_barex, marker_boxx, 'not', layer=layer_markers_aut, datatype=0)
                markers_all_auto = gdspy.boolean(markers_all_auto, cross_linesx, 'or',layer=layer_markers_aut, datatype=0)
                
                cross_lines_barey = cross_fun(cell,
                                         position_cross = position_ky,
                                         length_cross = length_line_bare,
                                         thickness_cross = thickness_line,
                                         layer_cross = layer_markers_aut)
                
                bby = np.array(crossy.get_bounding_box())
                marker_boxy = gdspy.Rectangle(bby[0]-marker_line_sep, bby[1]+marker_line_sep, layer=layer_markers_aut)
                cross_linesy = gdspy.boolean(cross_lines_barey, marker_boxy, 'not', layer=layer_markers_aut, datatype=0)
                markers_all_auto = gdspy.boolean(markers_all_auto, cross_linesy, 'or',layer=layer_markers_aut, datatype=0)
                
    cell.add(markers_all_man)
    cell.add(markers_all_auto)
    

# Test things
#thing = gdspy.Path(10,(0,0))
#thing.segment(30,'+y')
#thing.fillet(radius=3, points_per_2pi=128, max_points=199, precision=0.001)
#cell_example.add(thing)

#xr = (10+4)/10
#yr = (30+4)/30
#wow = gdspy.copy(thing,0,0)
#wow.scale(xr,yr,center=(0,15))
#cell_example.add(wow)

#amazing = gdspy.Path(14,(0,-2))
#amazing.segment(34,'+y',layer=2)
#amazing.fillet(radius=3+(14-10)/2, points_per_2pi=128, max_points=199, precision=0.001)
#cell_example.add(amazing) 
 
# Test things
#thing = gdspy.Path(10,(0,0))
#thing.segment(30,'+y')
#thing.arc(100, 0,np.pi/2,layer=4)
#thing.turn(100, 'r', layer=5 )
#cell_example.add(thing) 

# Test things
#thing1 = gdspy.Path(10,(0,0),3,0)
#thing1.segment(30,'+y')
#thing2 = gdspy.Path(8,(0,0),3,0)
#thing2.segment(29,'+y')
#thing = gdspy.boolean(thing1,thing2,'not',layer=5)
#cell_example.add(thing)

# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#                       CALL FUNCTIONS      
# ------------------------------------------------------------------------
         

        
if Status=='fabrication':
    frame = dicing_rectangle(cell = cell_example,
                         position = (0,0),
                         length = dice_chip_x,
                         width = dice_chip_y,
                         thickness = t_rectangle,
                         layer_rectangle = layers['Frame'])
    markers(cell = cell_example,
                     position = (0,0),
                     length = chip_x,
                     width = chip_y,
                     layer_markers_man = layers['Markers'],
                     layer_markers_aut = layers['Markers'])

    

if Status == 'simulation':
    # Create rectangle covering the whole chip
    point1_in = (-length2/2, -width2/2)
    point2_in = (length2/2, width2/2)
    rectangle = gdspy.Rectangle(point1_in, point2_in, layer=5, datatype=0)
    # Create inversion
    inv = gdspy.boolean(rectangle, gaps_polypath, "not")
    
    if Box == False:
        # Add inversion to the cell
        cell_example.add(inv)
        
    if Box == True:
        # BOX
        # Create rectangle covering one resonator
        #point1_b = (0, -96)
        #point2_b = (1200, 1900)
        point1_b = (-3050, 1200)
        point2_b = (-1800, -1200)
        box = gdspy.Rectangle(point1_b, point2_b, layer=4, datatype=0)
        # Create intersection between box and inversion
        box_inv = gdspy.boolean(inv, box, "and")
        # Add box to the cell
        cell_example.add(box_inv)
 # ------------------------------------------------------------------------    
    
# ------------------------------------------------------------------ #
#      VIEWER
# ------------------------------------------------------------------ #

# View the layout using a GUI.
    
gdspy.LayoutViewer(cells=cell_example)

# ------------------------------------------------------------------ #
#      OUTPUT
# ------------------------------------------------------------------ #

# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
from datetime import datetime
dt = datetime.now()


if Status == 'fabrication':
    print('We are in the fabrication process')
    
    
if Output == True:
    if Status == 'fabrication':
        gdspy.write_gds('./Designs_gds/{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt,filename), unit=1.0e-6, precision=1.0e-9)
        if dxf == True:
            gdspy.write_gds('./Designs_gds/{:%Y.%m.%d_%H.%M}_{}_fab.gds'.format(dt,filename), unit=1.0e-6, precision=1.0e-9)
            # %run ./macro_dxf.ipynb
