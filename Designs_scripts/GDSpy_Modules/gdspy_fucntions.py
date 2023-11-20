"""
Created on Sun June 10th 2023
@author: Amalie Terese Jiao Paulsen
@e-mail: jiaopaulsen@gmail.com
"""
import numpy as np
import gdspy
# import gdshelpers
# import sys
# import os
# import datetime
# import ezdxf 
import qiskit_metal   
print(' Using gdspy module version ' + gdspy.__version__)

path = r"C:\Users\jiaop\OneDrive\Skrivebord\Fluxonium_vrs.3\Designs"

# ------------------------------------------------------------------------
#                       COMPONENTS      
# ------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------- BASIC COMPONENTS --------------------------------------------------------------------------------------------------------

def wafer(cell,
          radius = 25400,#given in micrometer
          layer = 10,
          ):
    wafer = gdspy.Round((0, 0), radius, tolerance=0.01, layer = layer)
    cell.add(wafer)

def frame(cell,
          layer_frame = 0,
          position_frame = (0,0),
          design_size = 8000.0,
          chip_size = 10000.0,
          thickness_frame = 3.0):
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
        k.append([[1000,1000]+list[i],[9000,1000]+list[i],[1000,9000]+list[i],[9000,9000]+list[i]])
    k = np.array(k)
    circle =  gdspy.Round((position_marker[0]-500, position_marker[1]-500), 100)
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
    cell.add(circle)

def name_chip(cell, 
              layer_name = 2, 
              position_name = (0,0),
              fond_size = 25):
    name = gdspy.Text("{}".format(cell.name), fond_size, (position_name[0]+2000, -position_name[1]+500), layer=layer_name)
    size_name = name.get_bounding_box()[1][0]
    Qdev = gdspy.Text("SQuID Lab", fond_size, (position_name[0]+size_name + 100, position_name[1]+500), layer=layer_name)
    cell.add(Qdev)
    cell.add(name)

def feedline(cell, 
             layer_feedline = 3,
             position_feedline = (0,0),
             thickness_bondingpath1 = 636.6,
             size_feedline1 = 468.3,
             angle_feedline1 = 99.75,
             thickness_feedline1 = 22.7, # the thickness of the outer feedline
             length_feedline1 = 6200, 
             thickness_bondingpath2 = 300,
             size_feedline2 = 300,
             angle_feedline2 = 100,
             thickness_feedline2 = 10.7, # the thickness of the inner feedline
             length_feedline2 = 6200,            
             seperation_length = 168.3):
    seperation_chip = 10000/2 - ((thickness_bondingpath2 + seperation_length +angle_feedline1)*2  + length_feedline1)/2
    # Define the outer feedline curvature
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


# ------------------------------------------------------------------------------------------------- RESONATORS --------------------------------------------------------------------------------------------------------
def resonator_lambda2(cell, 
               layer_resonator = 4, 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 840,    #Change from here
               location_y = False,
               seperation_length = 18,
               coupler_length = 440,
               middle_length = 500,
               nr_turns = 12, 
               total_length = 8918,
               ):
    last_end = total_length-nr_turns*(turn + middle_length)- turn - coupler_length 
    print(last_end)
    if location_y == True: 
        position = (1332 + 568 + location_x,( 5000 + ((10.7)/2 + 6 + seperation_length + (w +s+s)/2 )))
        resonator_outer = gdspy.Path(w + s + s, (position[0] + 24,position[1])) 
        resonator_outer.segment(coupler_length + 24, "-x")
        resonator_outer.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "rr")
            else:
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "ll")
        resonator_outer.segment(last_end + 6, "+x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"-x")
        resonator_inner.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "rr")
            else:
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "ll")
        resonator_inner.segment(last_end, "+x")
    else:
        position = (1332 + 568+ location_x,( 5000 - ((10.7)/2+6 + seperation_length + (w +s+s)/2 )))
        # Define the outer resonator path
        resonator_outer = gdspy.Path(w + s + s, (position[0] + 24,position[1])) 
        resonator_outer.segment(coupler_length + 24, "-x")
        resonator_outer.turn(50, "ll")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "ll")
            else:
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "rr")
        resonator_outer.segment(last_end + 6, "+x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"-x")
        resonator_inner.turn(50, "ll")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "ll")
            else:
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "rr")
        resonator_inner.segment(last_end, "+x")
        #Use the boolean function to substract the two curvatures
    resonator = gdspy.boolean(resonator_outer,resonator_inner,"not", layer = layer_resonator)
    cell.add(resonator)

def resonator_lambda4(cell, 
               layer_resonator = 4, 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 840,    #Change from here
               location_y = False,
               seperation_length = 18,
               coupler_length = 440,
               middle_length = 500,
               nr_turns = 12, 
               total_length = 8918,
               ):
    last_end = total_length-nr_turns*(turn + middle_length)- turn - coupler_length 
    print(last_end)
    if location_y == True: 
        position = (1332 + 568 + location_x,( 5000 + ((10.7)/2 + 6 + seperation_length + (w +s+s)/2 )))
        resonator_outer = gdspy.Path(w + s + s, (position[0],position[1])) 
        resonator_outer.segment(coupler_length, "-x")
        resonator_outer.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "rr")
            else:
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "ll")
        resonator_outer.segment(last_end + 6, "+x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"-x")
        resonator_inner.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "rr")
            else:
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "ll")
        resonator_inner.segment(last_end, "+x")
    else:
        position = (1332 + 568+ location_x,( 5000 - ((10.7)/2+6 + seperation_length + (w +s+s)/2 )))
        # Define the outer resonator path
        resonator_outer = gdspy.Path(w + s + s, (position[0],position[1])) 
        resonator_outer.segment(coupler_length, "-x")
        resonator_outer.turn(50, "ll")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "ll")
            else:
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "rr")
        resonator_outer.segment(last_end + 6, "+x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"-x")
        resonator_inner.turn(50, "ll")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "ll")
            else:
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "rr")
        resonator_inner.segment(last_end, "+x")
        #Use the boolean function to substract the two curvatures
    resonator = gdspy.boolean(resonator_outer,resonator_inner,"not", layer = layer_resonator)
    cell.add(resonator)

def resonator_lambda4_d(cell, 
               layer_resonator = 4, 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 840,    #Change from here
               location_y = False,
               seperation_length = 18,
               coupler_length = 440,
               middle_length = 500,
               nr_turns = 12, 
               total_length = 8918,
               ):
    last_end = total_length-nr_turns*(turn + middle_length)- turn - coupler_length 
    print(last_end)
    if location_y == True: 
        position = (1332 + 568 + location_x,( 5000 + ((10.7)/2 + 6 + seperation_length + (w +s+s)/2 )))
        resonator_outer = gdspy.Path(w + s + s, (position[0],position[1])) 
        resonator_outer.segment(coupler_length, "-x")
        resonator_outer.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "rr")
            else:
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "ll")
        resonator_outer.segment(last_end + 6, "+x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"-x")
        resonator_inner.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "rr")
            else:
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "ll")
        resonator_inner.segment(last_end, "+x")
    else:
        position = (1332 + 568+ location_x,( 5000 - ((10.7)/2+6 + seperation_length + (w +s+s)/2 )))
        # Define the outer resonator path
        resonator_outer = gdspy.Path(w + s + s, (position[0],position[1])) 
        resonator_outer.segment(coupler_length, "+x")
        resonator_outer.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "rr")
            else:
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "ll")
        resonator_outer.segment(last_end + 6, "-x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"+x")
        resonator_inner.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "rr")
            else:
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "ll")
        resonator_inner.segment(last_end, "-x")
        #Use the boolean function to substract the two curvatures
    resonator = gdspy.boolean(resonator_outer,resonator_inner,"not", layer = layer_resonator)
    cell.add(resonator)



# ----------------------------------------------------------------------------------------------------  Resonator qubit --------------------------------------------------------------------------------------------------------




def resonator_lambda4_drive(cell, 
               layer_resonator = 4, 
               w = 10.7, 
               s = 6 , 
               turn = 157, 
               location_x = 840,    #Change from here
               location_y = False,
               seperation_length = 18,
               coupler_length = 440,
               middle_length = 500,
               nr_turns = 12, 
               total_length = 8918,
               ):
    last_end = total_length-nr_turns*(turn + middle_length)- turn - coupler_length 
    print(last_end)
    if location_y == True: 
        position = (1332 + 568 + location_x,( 5000 + ((10.7)/2 + 6 + seperation_length + (w +s+s)/2 )))
        resonator_outer = gdspy.Path(w + s + s, (position[0],position[1])) 
        resonator_outer.segment(coupler_length, "-x")
        resonator_outer.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "rr")
            else:
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "ll")
        resonator_outer.segment(last_end + 6, "+x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"-x")
        resonator_inner.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "rr")
            else:
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "ll")
        resonator_inner.segment(last_end, "+x")
    else:
        position = (1332 + 568+ location_x,( 5000 - ((10.7)/2+6 + seperation_length + (w +s+s)/2 )))
        # Define the outer resonator path
        resonator_outer = gdspy.Path(w + s + s, (position[0],position[1])) 
        resonator_outer.segment(coupler_length, "+x")
        resonator_outer.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_outer.segment(middle_length, "+x")
                resonator_outer.turn(50, "rr")
            else:
                resonator_outer.segment(middle_length, "-x")
                resonator_outer.turn(50, "ll")
        resonator_outer.segment(last_end + 6, "-x")
        #Define the inner resonator path
        new_position = position + (100,100)
        resonator_inner = gdspy.Path(w, position)
        resonator_inner.segment(coupler_length,"+x")
        resonator_inner.turn(50, "rr")
        for i in range(nr_turns):
            if i % 2:  # True, if i is divisible by 2
                resonator_inner.segment(middle_length, "+x")
                resonator_inner.turn(50, "rr")
            else:
                resonator_inner.segment(middle_length, "-x")
                resonator_inner.turn(50, "ll")
        resonator_inner.segment(last_end, "-x")
        #Use the boolean function to substract the two curvatures
    resonator = gdspy.boolean(resonator_outer,resonator_inner,"not", layer = layer_resonator)
    cell.add(resonator)

# ----------------------------------------------------------------------------------------------------  Federico JJ --------------------------------------------------------------------------------------------------------



def format_decimal_places(num, K =0):
    formatted_num = f"{num:.{K}f}"
    return formatted_num

def pads_federico(cell, #this function will make both the capacitor pads and the arms
         layer_pads = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 460,
        capacitor_width = 460,
        arm_width = 3, # size of te arm
        arm_length = 14.8,
        arm_height = 4.5,
        jj_width = 0.3,):
    fond_size = 30
    size = format_decimal_places(jj_width*1000)
    text = gdspy.Text(f"{size}", fond_size, (position[0] + 650, position[1]+3), layer = layer_pads)
    text2 = gdspy.copy(text, - 480)
    pad1 = gdspy.Path(capacitor_height, (position[0], position[1] + capacitor_height/2)).segment(capacitor_width, "+x").segment(0,"+x",arm_width,  axis_offset=-1.5).segment(5, "+x").segment(arm_length - 5 - 1.8, "+x", 1.5).segment(1.8, "+x", 1.5)
    pad2 = gdspy.copy(pad1,2*capacitor_width + 2*arm_length + 0.4).rotate(np.pi,(position[0]+ 2*capacitor_width + 2*arm_length + 0.4, position[1]+ capacitor_width/2))
    rectangle1 = gdspy.Rectangle((position[0]+ 5,position[1] +5), (position[0]+ 35,position[1] + 35))
    rectangle2 = gdspy.copy(rectangle1, 0,420)
    rectangle3 = gdspy.copy(rectangle1, 420,420)
    rectangle4 = gdspy.copy(rectangle1, 420,0)
    pad1 = gdspy.boolean(pad1, rectangle1, "not", layer = layer_pads)
    pad1 = gdspy.boolean(pad1, rectangle2, "not", layer = layer_pads)
    pad1 = gdspy.boolean(pad1, rectangle3, "not", layer = layer_pads)
    pad1 = gdspy.boolean(pad1, rectangle4, "not", layer = layer_pads)
    pad1 = gdspy.boolean(pad1, text2, "not", layer = layer_pads)
    rectangle5 = gdspy.copy(rectangle1, 490) 
    rectangle6 = gdspy.copy(rectangle1, 530)
    rectangle7 = gdspy.copy(rectangle2, 490)
    rectangle8 = gdspy.copy(rectangle2, 530)
    rectangle9 = gdspy.copy(rectangle3, 450)
    rectangle10 = gdspy.copy(rectangle3, 490)
    rectangle11 = gdspy.copy(rectangle4, 450)
    rectangle12 = gdspy.copy(rectangle4, 490)
    pad2 = gdspy.boolean(pad2, rectangle5, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, rectangle6, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, rectangle7, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, rectangle8, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, rectangle9, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, rectangle10, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, rectangle11, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, rectangle12, "not", layer = layer_pads)
    pad2 = gdspy.boolean(pad2, text, "not", layer = layer_pads)
    total_pads = gdspy.boolean(pad1, pad2, "or", layer = layer_pads)
    cell.add(total_pads)

def jj_federico(cell, #this function will make the jj , everything is in um
       layer_jj = 5,
       position_x = 3.0,
       position_y = 3.0, 
       jj_length1 = 5.2,
       jj_length2 = 4.5,
       jj_width = 0.30, # 300 nm
       jj_crossing =2.25,
       ):
    position_jj1 = (position_x,position_y)
    position_jj2 = (position_x-jj_crossing ,position_y - jj_length1 + jj_crossing)
    arm1 = gdspy.Path(jj_width, position_jj1)
    arm1.segment(jj_length1,"-y")
    arm2 = gdspy.Path(jj_width,position_jj2)
    arm2.segment(jj_length2,"+x")
    jj = gdspy.boolean(arm1, arm2, "or" , layer = layer_jj)
    cell.add(jj)
    gate_patches1 = gdspy.Path(jj_width, position_jj1).segment(0.7, "+y")
    gate_patches2 = gdspy.Path(jj_width, (position_jj2[0] + jj_length2,position_jj2[1])).segment(0.7, "+x")
    gate_patches = gdspy.boolean(gate_patches1, gate_patches2, "or", layer = layer_jj + 1)
    cell.add(gate_patches)
    
def patches_federico(cell, # this function will secure the jj
            layer_patches = 7,
            patch1 =(1,1),
            patch2 = (2,2),
            patch_width = 1.1,
            patch_length = 2.25,  
       ):
    patch1 = gdspy.Rectangle(patch1,(patch1[0] + patch_width , patch1[1] - patch_length), layer = layer_patches)
    patch2 = gdspy.Rectangle(patch2,(patch2[0] + patch_length, patch2[1] + patch_width), layer = layer_patches)
    cell.add(patch1)
    cell.add(patch2)

def jj_manhattan_federico(cell, #this function will make both the capacitor pads and the arms
        layer_manhattan = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 460.0,
        capacitor_width = 460.0,
        arm_width = 3.0, # size of te arm
        arm_length = 14.8,
        arm_height = 4.5,
        jj_length1 = 5.2,
        jj_length2 = 4.5, 
        jj_width = 0.30,): # 300 nm 
    position_jj_x = position[0] + capacitor_width + arm_length - 1.8/2 
    position_jj_y = position[1] + capacitor_height/2 + arm_width/2 + 0.05
    position_patch1_x = position[0] +  capacitor_width + arm_length - 1.5
    position_patch1_y = position[1] + capacitor_height/2 + arm_width - 1.5/2
    position_patch2_x = position_patch1_x + 1.45
    position_patch2_y = position_patch1_y - arm_height + 0.2
    pads_federico(cell, #this function will make both the capacitor pads and the arms
         layer_pads = layer_manhattan,
        position = position, #position of the jj
        capacitor_height = capacitor_height,
        capacitor_width = capacitor_width,
        arm_width = arm_width, # size of te arm
        arm_length = arm_length,
        arm_height = arm_height,
        jj_width = jj_width)
    jj_federico(cell, #this function will make the jj , everything is in um
        layer_jj = layer_manhattan +1,
        position_x = position_jj_x,
        position_y = position_jj_y, 
        jj_length1 = jj_length1,
        jj_length2 = jj_length2, 
        jj_width = jj_width, # 300 nm
        jj_crossing =2 + jj_width/2,)
    patches_federico(cell, # this function will secure the jj
            layer_patches = layer_manhattan +3,
            patch1 =(position_patch1_x,position_patch1_y),
            patch2 = (position_patch2_x,position_patch2_y),
            patch_width = 1.1,
            patch_length = 2.25,)

# ----------------------------------------------------------------------------------------------------  Amalie JJ --------------------------------------------------------------------------------------------------------


def pads_jj(cell, #this function will make both the capacitor pads and the arms
         layer_pads = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 120,
        capacitor_width = 120,
        arm_width = 3, # size of te arm
        jj_arm_length = 14.8,
        arm_height = 4.5,
        pad_arm_length = 120,
        jj_width = 0.3,
        nr_junctions = 36,
        jj_array_distance_x = 2.5,
        jj_array_width = 0.420,
        jj_array_arm = 18,
        inverse = True
        ):
    inv = 15
    fond_size = 30
    size = format_decimal_places(jj_width*1000)
    text = gdspy.Text(f"{size}", fond_size, (position[0] + 100, position[1]+3), layer = layer_pads)
    pad1 = gdspy.Path(capacitor_height, (position[0], position[1] + capacitor_height/2)).segment(capacitor_width, "+x")
    pad1.fillet(30)
    pad1_arm1 = gdspy.Path(18, (position[0], position[1] + capacitor_height/2)).segment(capacitor_width + pad_arm_length, "+x")
    pad1_arm1.fillet(2)
    pad1_arm1.segment(0,"+x",arm_width,  axis_offset=-1.5).segment(5, "+x").segment(jj_arm_length - 5 - 1.8, "+x", 1.5).segment(1.8, "+x", 1.5)
    pad1 = gdspy.boolean(pad1,pad1_arm1, "or")
    pad2 = gdspy.copy(pad1,2*capacitor_width + 2*jj_arm_length + 0.4 + pad_arm_length*2).rotate(np.pi,(position[0]+ 2*capacitor_width + 2*jj_arm_length + 0.4 + pad_arm_length*2, position[1]+ capacitor_width/2))
    pad1 = gdspy.boolean(pad1, text, "not", layer = layer_pads)
    total_pads = gdspy.boolean(pad1, pad2, "or", layer = layer_pads)
    jj_array_arm_length = (nr_junctions/2 + 2 )* (jj_array_distance_x + jj_array_width)
    position_1_jj_array_arm_x = position[0]+capacitor_width + pad_arm_length + jj_arm_length -jj_array_arm_length/2
    position_1_jj_array_arm_y =  position[1] + capacitor_height/2
    jj_array_arm1 = gdspy.Path(3.5, (position_1_jj_array_arm_x, position_1_jj_array_arm_y)).segment(jj_arm_length + jj_array_arm, "+y")
    jj_array_arm1.fillet(3)
    jj_array_arm2 = gdspy.copy(jj_array_arm1, jj_array_arm_length)
    total_pads = gdspy.boolean(pad1, pad2, "or", layer = layer_pads)
    total_pads = gdspy.boolean(total_pads, jj_array_arm1,"or", layer = layer_pads)
    total_pads = gdspy.boolean(total_pads, jj_array_arm2,"or", layer = layer_pads)
    if inverse:
        inverse = gdspy.Path(capacitor_height + inv, (position[0] - inv, position[1] + capacitor_height/2)).segment(capacitor_width + 2*inv, "+x").segment(0,"+x",jj_array_arm + inv)
        inverse.segment(270 - 2*inv,"+x").segment(0,"+x", capacitor_height + inv).segment(capacitor_width + 2*inv, "+x")
        total_pads = gdspy.boolean(inverse, total_pads, "not", layer = layer_pads)
    cell.add(total_pads)


    
def pads_jj_array(cell, #this function will make both the capacitor pads and the arms
         layer_pads = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 120,
        capacitor_width = 120,
        arm_width = 3, # size of te arm
        jj_arm_length = 14.8,
        arm_height = 4.5,
        pad_arm_length = 120,
        jj_width = 0.3,
        nr_junctions = 36,
        jj_array_arm_length = 100,
        jj_array_arm = 18,
        jj_array_arm_width = 1.5,
        inverse = True, 
        ):
    inv = 15
    fond_size = 30
    size = format_decimal_places(nr_junctions)
    text = gdspy.Text(f"{size}", fond_size, (position[0] + 100, position[1]+3), layer = layer_pads)
    pad1 = gdspy.Path(capacitor_height, (position[0], position[1] + capacitor_height/2)).segment(capacitor_width, "+x")
    pad1.fillet(30)
    pad1_arm1 = gdspy.Path(18, (position[0], position[1] + capacitor_height/2)).segment(capacitor_width + pad_arm_length, "+x")
    pad1_arm1.fillet(2)
    pad1_arm1.segment(0,"+x",arm_width,  axis_offset=-1.5).segment(5, "+x").segment(jj_arm_length - 5 - 1.8, "+x", 1.5).segment(1.8, "+x", 1.5)
    pad1 = gdspy.boolean(pad1,pad1_arm1, "or")
    pad2 = gdspy.copy(pad1,2*capacitor_width + 2*jj_arm_length + 0.4 + pad_arm_length*2).rotate(np.pi,(position[0]+ 2*capacitor_width + 2*jj_arm_length + 0.4 + pad_arm_length*2, position[1]+ capacitor_width/2))
    pad1 = gdspy.boolean(pad1, text, "not", layer = layer_pads)
    total_pads = gdspy.boolean(pad1, pad2, "or", layer = layer_pads)
    position_1_jj_array_arm_x = position[0]+capacitor_width + pad_arm_length + jj_arm_length -jj_array_arm_length/2
    position_1_jj_array_arm_y =  position[1] + capacitor_height/2
    jj_array_arm1 = gdspy.Path(jj_array_arm_width, (position_1_jj_array_arm_x, position_1_jj_array_arm_y)).segment(jj_arm_length + jj_array_arm, "+y")
    jj_array_arm1.fillet(1)
    jj_array_arm2 = gdspy.copy(jj_array_arm1, jj_array_arm_length)
    total_pads = gdspy.boolean(pad1, pad2, "or", layer = layer_pads)
    total_pads = gdspy.boolean(total_pads, jj_array_arm1,"or", layer = layer_pads)
    total_pads = gdspy.boolean(total_pads, jj_array_arm2,"or", layer = layer_pads)
    if inverse:
        inverse = gdspy.Path(capacitor_height + inv, (position[0] - inv, position[1] + capacitor_height/2)).segment(capacitor_width + 2*inv, "+x")
        inverse.segment(0,"+x",jj_arm_length + jj_array_arm + 3*inv, axis_offset= - inv).segment(270 - 2*inv,"+x").segment(0,"+x", capacitor_height + inv, axis_offset=+ inv).segment(capacitor_width + 2*inv, "+x")
        total_pads = gdspy.boolean(inverse, total_pads, "not", layer = layer_pads)
    cell.add(total_pads)

def jj(cell, #this function will make the jj , everything is in um
       layer_jj = 5,
       position_x = 3.0,
       position_y = 3.0, 
       jj_length1 = 5.2,
       jj_length2 = 4.5,
       jj_width = 0.30, # 300 nm
       jj_crossing =2.25,
       ):
    position_jj1 = (position_x,position_y)
    position_jj2 = (position_x-jj_crossing ,position_y - jj_length1 + jj_crossing)
    arm1 = gdspy.Path(jj_width, position_jj1)
    arm1.segment(jj_length1,"-y")
    arm2 = gdspy.Path(jj_width,position_jj2)
    arm2.segment(jj_length2,"+x")
    jj = gdspy.boolean(arm1, arm2, "or" , layer = layer_jj)
    cell.add(jj)
    gate_patches1 = gdspy.Path(jj_width, position_jj1).segment(0.7, "+y")
    gate_patches2 = gdspy.Path(jj_width, (position_jj2[0] + jj_length2,position_jj2[1])).segment(0.7, "+x")
    gate_patches = gdspy.boolean(gate_patches1, gate_patches2, "or", layer = layer_jj + 1)
    cell.add(gate_patches)

def jj_array(cell, #this function will make the jj , everything is in um
       layer_jj_array = 5,
       position_x = 3.0,
       position_y = 3.0, 
       jj_long =12, 
       jj_short= 6,
       jj_array_width = 0.420, # 420 nm 
       jj_array_distance_x = 2.5, 
       jj_array_distance_y = 3,
       nr_junctions = 36, #has to be able to be divided by  6
       ):
    nr_jj_short = nr_junctions/2
    nr_jj_long = nr_jj_short
    distance = nr_jj_short *jj_array_distance_x
    jj_long = gdspy.Path(jj_array_width, (position_x,position_y)).segment(jj_long, "+y")
    jj_long.fillet(1)
    repetitions = (nr_junctions)/6 
    jj_short1 = gdspy.Path(jj_array_width,(position_x-4.5,position_y+2)).segment(jj_short,"+x")
    jj_short1.fillet(1)
    jj_short2 = gdspy.copy(jj_short1, dx = (jj_array_distance_x + jj_array_width ), dy = jj_array_distance_y)
    jj_short3 = gdspy.copy(jj_short1, dx = (jj_array_distance_x + jj_array_width )*2, dy = jj_array_distance_y*2)
    jj_total1 = gdspy.boolean(jj_short1, jj_short2, "or", layer = layer_jj_array)
    jj_total1 = gdspy.boolean(jj_total1, gdspy.copy(jj_long, dx = jj_array_distance_x + jj_array_width), "or", layer = layer_jj_array)
    jj_total1 = gdspy.boolean(jj_total1, jj_short3, "or", layer = layer_jj_array)
    jj_total1 = gdspy.boolean(jj_total1, gdspy.copy(jj_long, dx = (jj_array_distance_x + jj_array_width)*2), "or", layer = layer_jj_array)
    jj_total1 = gdspy.boolean(jj_total1, jj_long, "or", layer = layer_jj_array)
    jj_total = gdspy.copy(jj_total1)
    for i in range(int(repetitions)):
        jj_total = gdspy.boolean(jj_total, gdspy.copy(jj_total1, dx = (jj_array_distance_x + jj_array_width ) * (3 * i) ), "or", layer = layer_jj_array)
    jj_total = gdspy.boolean(jj_total,  gdspy.copy(jj_short1, dx = (jj_array_distance_x + jj_array_width)*nr_jj_long), "or", layer = layer_jj_array)
    # add a short in the end
    cell.add(jj_total)


def patches(cell, # this function will secure the jj
            layer_patches = 7,
            patch1_position =(1,1),
            patch2_position = (2,2),
            patch_width = 1.1,
            patch_length = 2.25,  
       ):
    patch1 = gdspy.Rectangle(patch1_position,(patch1_position[0] + patch_width , patch1_position[1] - patch_length), layer = layer_patches)
    patch2 = gdspy.Rectangle(patch2_position,(patch2_position[0] + patch_length, patch2_position[1] + patch_width), layer = layer_patches)
    cell.add(patch1)
    cell.add(patch2)

def patches_jj_array(cell, # this function will secure the jj
            layer_patches = 7,  
            patch1_position =(1,1),
            patch2_position = (2,2),
            patch_width = 1.1,
            patch_length = 2.25,    
       ):
    patch1 = gdspy.Rectangle(patch1_position,(patch1_position[0] + patch_width , patch1_position[1] + patch_length), layer = layer_patches)
    patch2 = gdspy.Rectangle(patch2_position,(patch2_position[0] + patch_width, patch2_position[1] + patch_length), layer = layer_patches)
    cell.add(patch1)
    cell.add(patch2)

# def jj_array(cell, 
#              ):
#     jj_array = gdspy.Rect((0,0), (100,100))
#     cell.add(jj_array)

def jj_manhattan(cell, #this function will make both the capacitor pads and the arms
        layer_manhattan = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 460.0,
        capacitor_width = 460.0,
        arm_width = 3.0, # size of te arm
        jj_arm_length = 14.8,
        arm_height = 4.5,
        pad_arm_length = 120,
        jj_length1 = 5.2,
        jj_length2 = 4.5, 
        jj_width = 0.30,
        jj_array_arm = 18,
        nr_junctions = 300,
        jj_array_width = 0.420,
        jj_array_distance_x = 2.5,
        inverse = True,
        ): # 300 nm 
    position_jj_x = position[0] + capacitor_width + jj_arm_length + pad_arm_length - 1.8/2 
    position_jj_y = position[1] + capacitor_height/2 + arm_width/2 + 0.05
    position_patch1_x = position[0] +  capacitor_width + jj_arm_length + pad_arm_length - 1.5
    position_patch1_y = position[1] + capacitor_height/2 + arm_width - 1.5/2
    position_patch2_x = position_patch1_x + 1.45 + 0.45 
    position_patch2_y = position_patch1_y - arm_height + 0.15
    pads_jj(cell, #this function will make both the capacitor pads and the arms
         layer_pads = layer_manhattan,
        position = position, #position of the jj
        capacitor_height = capacitor_height,
        capacitor_width = capacitor_width,
        arm_width = arm_width, # size of te arm
        jj_arm_length = jj_arm_length,
        arm_height = arm_height,
        pad_arm_length = pad_arm_length,
        jj_width = jj_width,
        nr_junctions = nr_junctions,
        jj_array_distance_x = jj_array_distance_x,
        jj_array_width = jj_array_width,
        jj_array_arm = jj_array_arm,
        inverse = inverse,
        )
    jj(cell, #this function will make the jj , everything is in um
        layer_jj = layer_manhattan +1,
        position_x = position_jj_x,
        position_y = position_jj_y, 
        jj_length1 = jj_length1,
        jj_length2 = jj_length2, 
        jj_width = jj_width, # 300 nm
        jj_crossing =2 + jj_width/2,)
    patches(cell, # this function will secure the jj
            layer_patches = layer_manhattan +3,
            patch1_position =(position_patch1_x,position_patch1_y),
            patch2_position = (position_patch2_x,position_patch2_y),
            patch_width = 1.2,
            patch_length = 1.8,)
    



def jj_manhattan_array(cell, #this function will make both the capacitor pads and the arms
        layer_manhattan = 5,
        position = (2000,2000), #position of the jj
        capacitor_height = 460.0,
        capacitor_width = 460.0,
        arm_width = 3.0, # size of te arm
        jj_arm_length = 14.8,
        arm_height = 4.5,
        pad_arm_length = 120,
        jj_length1 = 5.2,
        jj_length2 = 4.5, 
        jj_width = 0.30,
        jj_array_arm = 18,
        nr_junctions = 36,
        jj_long = 12, 
        jj_short = 6,
        jj_array_width = 0.420,
        jj_array_distance_x = 2.5,
        jj_array_distance_y = 3,
        jj_array_arm_width = 1.5, 
        inverse = True
        ): # 300 nm 
    jj_array_arm_length = (nr_junctions/2 + 1 )* (jj_array_distance_x + jj_array_width) + 0.5

    position_jj_array_x = position[0] + capacitor_width + pad_arm_length + jj_arm_length - ((nr_junctions/2 -1 )* (jj_array_distance_x + jj_array_width))/2 
    position_jj_array_y = position[1] + capacitor_height/2 + arm_height/2 + jj_array_arm
    
    position_patch1_x = position[0] +  capacitor_width + pad_arm_length + jj_arm_length - jj_array_arm_length/2 - jj_array_arm_width/2
    position_patch1_y = position[1] + capacitor_height/2 + jj_array_arm + jj_array_distance_y
    position_patch2_x = position_patch1_x + jj_array_arm_length
    position_patch2_y = position_patch1_y
    pads_jj_array(cell, #this function will make both the capacitor pads and the arms
         layer_pads = layer_manhattan,
        position = position, #position of the jj
        capacitor_height = capacitor_height,
        capacitor_width = capacitor_width,
        arm_width = arm_width, # size of te arm
        jj_arm_length = jj_arm_length,
        arm_height = arm_height,
        pad_arm_length = pad_arm_length,
        jj_width = jj_width,
        nr_junctions = nr_junctions,
        jj_array_arm_length = jj_array_arm_length,
        jj_array_arm = jj_array_arm,
        jj_array_arm_width = jj_array_arm_width,
        inverse = inverse,
        )
    jj_array(cell, #this function will make the jj , everything is in um
       layer_jj_array = layer_manhattan +1,
       position_x = position_jj_array_x,
       position_y = position_jj_array_y, 
       jj_long =jj_long, 
       jj_short= jj_short,
       jj_array_width = jj_array_width, # 420 nm 
       jj_array_distance_x = jj_array_distance_x, 
       jj_array_distance_y = jj_array_distance_y,
       nr_junctions = nr_junctions, #has to be able to be divided by  6
       )
    patches_jj_array(cell, # this function will secure the jj
            layer_patches = layer_manhattan +3,
            patch1_position =(position_patch1_x,position_patch1_y),
            patch2_position = (position_patch2_x,position_patch2_y),
            patch_width = jj_array_arm_width,
            patch_length = 2.5,)
    
    







# --------------------------------------------------------------------------------------------------------------- Fluxonium --------------------------------------------------------------------------------------------------------------

# def jj_manhattan_array(cell, #this function will make both the capacitor pads and the arms
#         layer_manhattan = 5,
#         position = (2000,2000), #position of the jj
#         capacitor_height = 460.0,
#         capacitor_width = 460.0,
#         arm_width = 3.0, # size of te arm
#         jj_arm_length = 14.8,
#         arm_height = 4.5,
#         pad_arm_length = 120,
#         jj_length1 = 5.2,
#         jj_length2 = 4.5, 
#         jj_width = 0.30,
#         jj_array_arm = 18,
#         nr_junctions = 36,
#         jj_long = 12, 
#         jj_short = 6,
#         jj_array_width = 0.420,
#         jj_array_distance_x = 2.5,
#         jj_array_distance_y = 3,
#         jj_array_arm_width = 1.5, 
#         ): # 300 nm 
#     position_jj_x = position[0] + capacitor_width + jj_arm_length + pad_arm_length - 1.8/2 
#     position_jj_y = position[1] + capacitor_height/2 + arm_width/2 + 0.05
#     jj_array_arm_length = (nr_junctions/2 + 1 )* (jj_array_distance_x + jj_array_width) + 0.5

#     position_jj_array_x = position[0] + capacitor_width + pad_arm_length + jj_arm_length - ((nr_junctions/2 -1 )* (jj_array_distance_x + jj_array_width))/2 
#     position_jj_array_y = position[1] + capacitor_height/2 + arm_height/2 + jj_array_arm
    
#     position_patch1_x = position[0] +  capacitor_width + pad_arm_length + jj_arm_length - jj_array_arm_length/2 - jj_array_arm_width/2
#     position_patch1_y = position[1] + capacitor_height/2 + jj_array_arm + jj_array_distance_y
#     position_patch2_x = position_patch1_x + jj_array_arm_length
#     position_patch2_y = position_patch1_y
#     pads_jj_array(cell, #this function will make both the capacitor pads and the arms
#          layer_pads = layer_manhattan,
#         position = position, #position of the jj
#         capacitor_height = capacitor_height,
#         capacitor_width = capacitor_width,
#         arm_width = arm_width, # size of te arm
#         jj_arm_length = jj_arm_length,
#         arm_height = arm_height,
#         pad_arm_length = pad_arm_length,
#         jj_width = jj_width,
#         nr_junctions = nr_junctions,
#         jj_array_arm_length = jj_array_arm_length,
#         jj_array_arm = jj_array_arm,
#         jj_array_arm_width = jj_array_arm_width,
#         )
#     jj_array(cell, #this function will make the jj , everything is in um
#        layer_jj_array = layer_manhattan +1,
#        position_x = position_jj_array_x,
#        position_y = position_jj_array_y, 
#        jj_long =jj_long, 
#        jj_short= jj_short,
#        jj_array_width = jj_array_width, # 420 nm 
#        jj_array_distance_x = jj_array_distance_x, 
#        jj_array_distance_y = jj_array_distance_y,
#        nr_junctions = nr_junctions, #has to be able to be divided by  6
#        )
#     patches_jj_array(cell, # this function will secure the jj
#             layer_patches = layer_manhattan +3,
#             patch1_position =(position_patch1_x,position_patch1_y),
#             patch2_position = (position_patch2_x,position_patch2_y),
#             patch_width = jj_array_arm_width,
#             patch_length = 2.5,)
#     jj(cell, #this function will make the jj , everything is in um
#         layer_jj = layer_manhattan +1,
#         position_x = position_jj_x,
#         position_y = position_jj_y, 
#         jj_length1 = jj_length1,
#         jj_length2 = jj_length2, 
#         jj_width = jj_width, # 300 nm
#         jj_crossing =2 + jj_width/2,)
#     patches(cell, # this function will secure the jj
#             layer_patches = layer_manhattan +3,
#             patch1_position =(position_patch1_x,position_patch1_y),
#             patch2_position = (position_patch2_x,position_patch2_y),
#             patch_width = 1.2,
#             patch_length = 1.8,)
    