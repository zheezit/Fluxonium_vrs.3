"""
Created on Fri Dec 9th 15:35 2022

@author: David Feldstein i Bofill
@e-mail: dfeldstein98@gmail.com
"""

import numpy as np
import gdspy

print('Using gdspy module version ' + gdspy.__version__)

# ------------------------------------------------------------------------
#                       INPUT OPTIONS      
# ------------------------------------------------------------------------

Status = 'simulation'
res_fullgap = 'Fine'
Comsol = False
res_sim = False
Box = False
single_sim_num = 5
Output = True

filename = '10_res_NbTiN'
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#                       PARAMETERS      
# ------------------------------------------------------------------------

if __name__ == '__main__':

    cell_example = gdspy.Cell('Gatemon')
    
    layers = {'Core':0,
              'Coarse beam':1,
              'Fine beam':2,
              'Coarse holes':3,
              'Fine holes':4,
              'Small holes':5,
              'Big holes': 6,
              'Coarse beam 2':7,
              'ALD':8,
              'Markers':9,
              'Frame':10,
              'Contacts': 11,
              'Capacitor': 12,
              'Waveguide':13,
              'Box':14
             }

    # Determine the chip dimensions in um
    chip_x = 8000.0
    chip_y = 8000.0
    
    # Determine the diced chip dimensions in um
    dice_chip_x = 10000.0
    dice_chip_y = 10000.0

    # Determine the width of the waveguide's centerstrip through impedance matching
    wcc = 13
    # Width of the waveguide's gap
    wgap = 4
    # Width of the launcher's central's line width
    wcc_launcher = 300
    # Gap of launcher's cpw
    wgap_launcher = 172.8
    # Thickness of the rectangle which limits the chip perimeter
    t_rectangle = 50.0
    # Length of the launcher
    len_launcher = 300.0
    # Length of the second launcher
    len2_launcher = 300.0-200.0
    # Length of the transmission line
    length = chip_x - 2*(len_launcher+len2_launcher)
    # Length from the leftmost part of the launcher to the rightmost part of the launcher
    length2=chip_x 
    # Width of the chip
    width2=chip_y
    # Y position of the outer part of the transmission line
    pos_y = wcc/2
    # Buffer region up to there are no big holes
    gapSkirt_big = 5.0
    # Buffer region up to there are no small holes
    gapSkirt_small = 0.5
    
    # Number of cpw resonators
    N_cpw = 8
    
    # Multiple CPW resonators coupled to a straight feedline 
    positions_cpw = [(-2800.0, 8.0), (-2000.0, -8.0), (-1200.0, 8.0), (-400.0, -8.0), (400.0, 8.0), (+1200.0, -8.0), (+2000.0, 8.0), (+2800.0, -8.0)]
    directions_cpw = ['+y', '-y', '+y', '-y', '+y', '-y', '+y', '-y']
    wcc_i = wcc * np.ones(N_cpw)
    wgap_i = wgap * np.ones(N_cpw)
    Ns_meanders = np.array([8,4,8,4,8,4,8,4])
    cpw_cc_i = [500,100,500,100,500,100,500,100]
    cpw_end_i = [400,400,400,400,400,400,400,400]
    yMeander_i = [500,500,500,500,500,500,500,500]
    dturn = 100.0
    height_cpw = 2*wgap+wcc+(2*Ns_meanders-1)*dturn+(dturn/2-wcc/2-wgap)
    gapCoupler_i = np.array([1,1,1,1,1,1,1,1,1,1])*3 # Distance between the coupler and the qubit hole
    lambda_res_ii = [0.5,0.25,0.5,0.25,0.5,0.25,0.5,0.25]

    # Qubit islands
    gapCap_i = [20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0] 
    xIsland_i = [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    yIsland_i = [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    yContacts = [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    xHole_i = np.array(xIsland_i)+2*np.array(gapCap_i) 
    yHole_i = np.array(yIsland_i)+np.array(gapCap_i)+np.array(yContacts)
    Roundness_i = [0,0,10,10,20,20,30,30]
    
    if Box == True:
        N_cpw = 1
        Roundness_i[0] = Roundness_i[single_sim_num]
        Ns_meanders[0] = Ns_meanders[single_sim_num]
        cpw_cc_i[0] = cpw_cc_i[single_sim_num]
        cpw_end_i[0] = cpw_end_i[single_sim_num]
        yMeander_i[0] = yMeander_i[single_sim_num]
        height_cpw[0] = height_cpw[single_sim_num]
        gapCoupler_i[0] = gapCoupler_i[single_sim_num]
        lambda_res_ii[0] = lambda_res_ii[single_sim_num]
    
    

# ------------------------------------------------------------------------

    
# ------------------------------------------------------------------------
#                       COMPONENTS      
# ------------------------------------------------------------------------
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
    X = length/2+thickness
    Y = width/2+thickness
    point1_out = (position[0]-X-thickness/2,position[1]-Y-thickness/2)
    point2_out = (position[0]+X+thickness/2, position[1]+Y+thickness/2)
    point1_in = (position[0]-length/2, position[1]-width/2)
    point2_in = (position[0]+length/2, position[1]+width/2)
    outer = gdspy.Rectangle(point1_out, point2_out, layer=layer_rectangle, datatype=0)
    inner = gdspy.Rectangle(point1_in, point2_in, layer=layer_rectangle, datatype=0)
    merged = gdspy.fast_boolean(outer, inner, 'xor', layer=layer_rectangle, datatype=0)
    
    # Add all the elements to the cell
    cell.add(merged)
    
def markers(cell,
             position = (0,0),
             length = 10000.0,
             width = 10000.0,
             layer_markers = 0):
    
    # Markers for a square chip
    marker_separation = 200.0
    marker_line_sep = 3.0
    thickness_line = 2.5
    length_line = 83.0
    length_cross = 10
    thickness_cross = 0.4
    
    markers_all = cross_fun(cell,
                 position_cross = (position[0]+chip_x/2,position[1]+chip_y/2),
                 length_cross = length_cross,
                 thickness_cross = thickness_cross,
                 layer_cross = layer_markers)
    
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
                             layer_cross = layer_markers)

                markers_all = gdspy.boolean(markers_all, crossy, 'or', layer=layer_markers, datatype=0)
                
                # Add text
                texty = gdspy.Text('{}'.format(kk+1), 8, (position_ky[0]+6,position_ky[1]-15),layer = layer_markers)
                markers_all = gdspy.boolean(markers_all, texty, 'or', layer=layer_markers, datatype=0)
                crossx = cross_fun(cell,
                             position_cross = position_kx,
                             length_cross = length_cross,
                             thickness_cross = thickness_cross,
                             layer_cross = layer_markers)

                markers_all = gdspy.boolean(markers_all, crossx, 'or', layer=layer_markers, datatype=0)
                textx = gdspy.Text('{}'.format(kk+1), 8, (position_kx[0]+6,position_kx[1]-15),layer = layer_markers)
                markers_all = gdspy.boolean(markers_all, textx, 'or', layer=layer_markers, datatype=0)
                
                
                length_line_bare = 2*length_line+length_cross+2*marker_line_sep
                cross_lines_barex = cross_fun(cell,
                                         position_cross = position_kx,
                                         length_cross = length_line_bare,
                                         thickness_cross = thickness_line,
                                         layer_cross = layer_markers)
                
                bbx = np.array(crossx.get_bounding_box())
                marker_boxx = gdspy.Rectangle(bbx[0]-marker_line_sep, bbx[1]+marker_line_sep, layer=layer_markers)
                cross_linesx = gdspy.boolean(cross_lines_barex, marker_boxx, 'not', layer=layer_markers, datatype=0)
                markers_all = gdspy.boolean(markers_all, cross_linesx, 'or', layer=layer_markers, datatype=0)
                
                cross_lines_barey = cross_fun(cell,
                                         position_cross = position_ky,
                                         length_cross = length_line_bare,
                                         thickness_cross = thickness_line,
                                         layer_cross = layer_markers)
                
                bby = np.array(crossy.get_bounding_box())
                marker_boxy = gdspy.Rectangle(bby[0]-marker_line_sep, bby[1]+marker_line_sep, layer=layer_markers)
                cross_linesy = gdspy.boolean(cross_lines_barey, marker_boxy, 'not', layer=layer_markers, datatype=0)
                markers_all = gdspy.boolean(markers_all, cross_linesy, 'or', layer=layer_markers, datatype=0)
                
    cell.add(markers_all)

    
    
def meandered_waveguide(cell,
              position = (0,0),
              direction = '+y',
              wcc = 45.0,
              wgap = 0.65,
              yMeander = 200.0,
              d_wvg = 300.0,
              N_wvg = 2,
              cpw_cc = 100,
              cpw_end = 400,
              radius_turn = 0.5,
              lMeander = 400.0,
              c_strength = 3/4,
              gapSkirt_big = 5.0, 
              gapSkirt_small = 0.5, 
              layer_skirt_big = 6, 
              layer_skirt_small = 6,
              coupler = [0,0,0],
              gapCoupler = 10,
              lambda_res = 0.5,
              layer_core = 3,
              layer_gap = 0,
              datatype = 0):
        
    '''
    A meandered waveguide.
    '''

    spec = {'layer': layer_gap, 'datatype': datatype}
    npoints = 10
    precision = 0.00001
 
    # Segment of the meander waveguide next to the feedline
    if lambda_res == 0.5:
        xBase = cpw_cc
    elif lambda_res == 0.25:
        xBase = yMeander
    # Gap at the beginning of the lambda/2 CPW
    xBase_gap = 3*wgap
    # Envelope meander
    spec['layer'] = layer_gap
    meander_wvg_out = gdspy.Path(wcc+2*wgap, (position[0]-wgap-xBase+yMeander/2-xBase_gap, position[1]-wcc-2*wgap))
    meander_wvg_out.segment(xBase+wgap+xBase_gap, '+x', **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\
                .segment(lMeander, **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\

    for i in range(N_wvg-1):
        meander_wvg_out.segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
    
    # To terminate the CPW as a common l/2 resonator
    #meander_wvg_out.segment(cpw_end+wgap, **spec)
    
    # To couple the CPW to a qubit island
    meander_wvg_out.segment(yMeander/2-radius_turn*d_wvg, **spec)\
        .turn(radius_turn*d_wvg, 'l', **spec)   
    
    if lambda_res == 0.25:
        tail_wvg_out = gdspy.Path(wcc+2*wgap, (position[0]-wgap-xBase+yMeander/2-xBase_gap, position[1]-wcc-2*wgap))
        if Comsol == True:
            tail_wvg_out.segment(dturn, '-x', **spec)\
            .turn(radius_turn*d_wvg, 'l', **spec)\
            .segment(cpw_cc+xBase_gap, **spec)
        elif Comsol == False:
            tail_wvg_out.segment(dturn, '-x', **spec)\
            .turn(radius_turn*d_wvg, 'l', **spec)\
            .segment(cpw_cc, **spec)
        meander_wvg_out = gdspy.boolean(meander_wvg_out,tail_wvg_out,'or',**spec)
        
    # Inner meander
    meander_wvg_in = gdspy.Path(wcc, (position[0]-xBase+yMeander/2, position[1]-wcc-2*wgap))
    meander_wvg_in.segment(xBase, '+x', **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\
                .segment(lMeander, **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\

    for i in range(N_wvg-1):
        meander_wvg_in.segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
    # To terminate the CPW as a common l/2 resonator
    #meander_wvg_in.segment(cpw_end, **spec)

    # To couple the CPW to a qubit island
    meander_wvg_in.segment(yMeander/2-radius_turn*d_wvg, **spec)\
        .turn(radius_turn*d_wvg, 'l', **spec)
        
    if lambda_res == 0.25:
        tail_wvg_in = gdspy.Path(wcc, (position[0]-xBase+yMeander/2, position[1]-wcc-2*wgap))
        tail_wvg_in.segment(dturn+xBase_gap+wgap, '-x', **spec)\
            .turn(radius_turn*d_wvg, 'l', **spec)\
            .segment(cpw_cc, **spec)
        meander_wvg_in = gdspy.boolean(meander_wvg_in,tail_wvg_in,'or',**spec)  
        
    # Qubit coupler
    xHole = coupler[0]
    yHole = coupler[1]
    Risl = coupler[2]
    xIsland = coupler[3]
    R = Risl + (xHole-xIsland)/2
    xCoupler = xHole + 2 * wcc
    yCoupler = yHole
    xBuffer = xHole+2*gapCoupler
    yBuffer = yHole+2*gapCoupler
    if Risl == 0:
        g1 = -R
        g2 = -R
        g3 = -R
        g4 = -R
        g5 = -R
        g6 = -R
        g_skirt_small = 0
        g_skirt_big = 0
        g_skirt_small1 = 0
        g_skirt_big1 = 0
        g_skirt_small2 = 0
        g_skirt_big2 = 0
    else:
        g1 = (xBuffer+2*wcc+2*wgap-xHole)/2
        g2 = (xBuffer+2*wcc+4*wgap-xHole)/2
        g3 = (xBuffer+2*wgap-xHole)/2
        g4 = (xBuffer-xHole)/2
        g5 = gapSkirt_small
        g6 = -gapSkirt_small
        g_skirt_small1 = wgap+gapSkirt_small
        g_skirt_big1 = gapSkirt_big
        g_skirt_small2 = -gapSkirt_big
        g_skirt_big2 = -wgap-gapSkirt_small
    
    height_cpw = 2*wgap+wcc+(2*N_wvg-1)*d_wvg+d_wvg/2
    def coupler_fun(out_side, out_up, in_side, in_up, gSkirtbig, gSkirtsmall,bmiddle, layer_i):
        spec['layer'] = layer_i
        
        meander_coupler_out = gdspy.Path(xBuffer+2*wcc+4*wgap+2*out_side, (position[0], position[1]-height_cpw+wgap+out_up))
        meander_coupler_out.segment(yBuffer+2*wcc+4*wgap+2*out_up, '-y',**spec)
        meander_coupler_out.fillet(radius=R+g2+gSkirtbig, points_per_2pi=128*npoints, max_points=199*npoints, precision=precision)

        meander_coupler_in = gdspy.Path(xBuffer+2*wcc+2*wgap+2*in_side, (position[0], position[1]-height_cpw+in_up))
        meander_coupler_in.segment(yBuffer+2*wcc+2*wgap+2*in_up, '-y', **spec)
        meander_coupler_in.fillet(radius=R+g1+gSkirtsmall, points_per_2pi=128*npoints, max_points=199*npoints, precision=precision)

        block_top_in = gdspy.Path(xBuffer+2*wcc+4*wgap+2*out_side, (position[0], position[1]-height_cpw+wgap-c_strength*yCoupler-in_side))
        block_top_in.segment(yCoupler+2*wcc, '-y', **spec)
        block_top_out = gdspy.Path(xBuffer+2*wcc+4*wgap+2*out_side, (position[0], position[1]-height_cpw+wgap-c_strength*yCoupler-wgap-out_side))
        block_top_out.segment(yCoupler+2*wcc, '-y', **spec)
        block_hole_in = gdspy.Path(xBuffer+2*wgap-2*in_side, (position[0], position[1]-height_cpw-wcc-in_side))
        block_hole_in.segment(yBuffer+2*wgap-2*in_side, '-y', **spec)
        block_hole_in.fillet(radius=R+g3-gSkirtsmall, points_per_2pi=128*npoints, max_points=199*npoints, precision=precision)
        block_hole_out = gdspy.Path(xBuffer-2*out_side, (position[0], position[1]-height_cpw+wgap-wcc-2*wgap-out_side))
        block_hole_out.segment(yBuffer-2*out_side, '-y', **spec)
        block_hole_out.fillet(radius=R+g4-gSkirtbig, points_per_2pi=128*npoints, max_points=199*npoints, precision=precision)

        block_in = gdspy.boolean(block_hole_in, block_top_in,"or")
        block_out = gdspy.boolean(block_hole_out, block_top_out,"or")

        meander_coupler_in_cut = gdspy.boolean(meander_coupler_in, block_in,"not")
        meander_coupler_out_cut = gdspy.boolean(meander_coupler_out, block_out,"not")
        meander_coupler_bare = gdspy.boolean(meander_coupler_out_cut, meander_coupler_in_cut,"not")

        block_middle = gdspy.Path(bmiddle, (position[0], position[1]-height_cpw-wcc/2))
        block_middle.segment(6*wgap, '+y', **spec)

        blocks_total = gdspy.boolean(block_middle, meander_wvg_in,"or")
        meander_coupler = gdspy.boolean(meander_coupler_bare, blocks_total,"not")
        return meander_coupler
    
    meander_coupler = coupler_fun(0,0,0,0,0,0,wcc,layer_gap)
    meander_coupler_neg = coupler_fun(gapSkirt_small,gapSkirt_small,-gapSkirt_small,-gapSkirt_small,g5,g6,wcc,layer_gap)
    meander_coupler_bh = coupler_fun(gapSkirt_big,gapSkirt_big,-gapSkirt_big,-gapSkirt_big,g_skirt_big1,g_skirt_small2,wcc-2*gapSkirt_big,layer_skirt_small)
    meander_coupler_Skirt_out = coupler_fun(gapSkirt_big, gapSkirt_big, wgap+gapSkirt_small, wgap+gapSkirt_small,g_skirt_big1,g_skirt_small1,wcc+2*wgap+gapSkirt_big,layer_skirt_big)
    meander_coupler_Skirt_in = coupler_fun(-wgap-gapSkirt_small, -wgap-gapSkirt_small, -gapSkirt_big, -gapSkirt_big,g_skirt_big2,g_skirt_small2,wcc-2*gapSkirt_big,layer_skirt_big)
    meander_coupler_Skirt = gdspy.boolean(meander_coupler_Skirt_in,meander_coupler_Skirt_out, "or", layer = layer_skirt_big)
    
    # Substract CPW intersection part
    #block_middle_skirt = gdspy.Path(wcc+4*wgap, (position[0], position[1]-height_cpw))
    #block_middle_skirt.segment(gapSkirt_big*2, '+y', layer = 18)

    #meander_coupler_Skirt_new = gdspy.boolean(meander_coupler_Skirt, block_middle_skirt,"not")
    
    # Merge inner and outer waveguides
    if Status=='simulation':
        meander_wvg_bare = gdspy.boolean(meander_wvg_out, meander_wvg_in,"not")
        meander_wvg = gdspy.boolean(meander_coupler, meander_wvg_bare,"or")
        #meander_wvg = gdspy.boolean(meander_wvg_out, meander_wvg_in,"not")
    if Status=='fabrication':
        meander_wvg_bare = gdspy.boolean(meander_wvg_out, meander_wvg_in,"not")
        meander_wvg = gdspy.boolean(meander_coupler, meander_wvg_bare,"or",layer=layers['Coarse beam'])

    '''

    Fabrication skirts

    '''

   # Envelope meander skirt
    spec['layer'] = layer_skirt_big
    meander_wvg_out_skirt = gdspy.Path(wcc+2*wgap+2*gapSkirt_small, (position[0]-wgap-xBase+yMeander/2-gapSkirt_small-xBase_gap,position[1]-wcc-2*wgap))
    meander_wvg_out_skirt.segment(xBase+wgap+gapSkirt_small+xBase_gap, '+x', **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\
                .segment(lMeander, **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\

    for i in range(N_wvg-1):
        meander_wvg_out_skirt.segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
    
    # To terminate the CPW as a common l/2 resonator
    #meander_wvg_out_skirt.segment(cpw_end+wgap+gapSkirt_small, **spec)
    
    # To couple the CPW to a qubit island
    meander_wvg_out_skirt.segment(yMeander/2-radius_turn*d_wvg, **spec)\
        .turn(radius_turn*d_wvg, 'l', **spec)\
        .segment(gapSkirt_big, **spec)
        #.arc(radius_turn*d_wvg,np.pi/2,np.pi-np.arcsin((wgap+gapSkirt_small)/(radius_turn*d_wvg)),**spec)
        
    if lambda_res == 0.25:
        tail_wvg_out_skirt = gdspy.Path(wcc+2*wgap+2*gapSkirt_small, (position[0]-wgap-xBase+yMeander/2-gapSkirt_small-xBase_gap,position[1]-wcc-2*wgap))
        tail_wvg_out_skirt.segment(dturn-gapSkirt_small, '-x', **spec)\
            .turn(radius_turn*d_wvg, 'l', **spec)\
            .segment(cpw_cc+gapSkirt_small, **spec)
        meander_wvg_out_skirt = gdspy.boolean(meander_wvg_out_skirt,tail_wvg_out_skirt,'or',**spec)  
        
    
    # Inner meander skirt
    meander_wvg_in_skirt = gdspy.Path(wcc-2*gapSkirt_small, (position[0]-xBase+yMeander/2+gapSkirt_small, position[1]-wcc-2*wgap))
    meander_wvg_in_skirt.segment(xBase-gapSkirt_small, '+x', **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\
                .segment(lMeander, **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\

    for i in range(N_wvg-1):
        meander_wvg_in_skirt.segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
    # To terminate the CPW as a common l/2 resonator
    #meander_wvg_in_skirt.segment(cpw_end-gapSkirt_small, **spec)
    
    # To couple the CPW to a qubit island
    meander_wvg_in_skirt.segment(yMeander/2-radius_turn*d_wvg, **spec)\
        .turn(radius_turn*d_wvg, 'l', **spec)\
        .segment(gapSkirt_big, **spec)
        #.arc(radius_turn*d_wvg,np.pi/2,np.pi-np.arcsin((wgap+gapSkirt_small)/(radius_turn*d_wvg)),**spec)
        
    if lambda_res == 0.25:
        tail_wvg_in_skirt = gdspy.Path(wcc-2*gapSkirt_small, (position[0]-xBase+yMeander/2+gapSkirt_small, position[1]-wcc-2*wgap))
        tail_wvg_in_skirt.segment(dturn+xBase_gap+wgap+gapSkirt_small, '-x', **spec)\
            .turn(radius_turn*d_wvg, 'l', **spec)\
            .segment(cpw_cc+gapSkirt_big, **spec)
        meander_wvg_in_skirt = gdspy.boolean(meander_wvg_in_skirt,tail_wvg_in_skirt,'or',**spec)  
        
    # Outermost skirt meander
    meander_wvg_env_skirt = gdspy.Path(wcc+2*wgap+2*gapSkirt_big, (position[0]-wgap-xBase+yMeander/2-gapSkirt_big-xBase_gap, position[1]-wcc-2*wgap))
    meander_wvg_env_skirt.segment(xBase+wgap+gapSkirt_big+xBase_gap, '+x', **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\
                .segment(lMeander, **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\

    for i in range(N_wvg-1):
        meander_wvg_env_skirt.segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\

    # To terminate the CPW as a common l/2 resonator
    #meander_wvg_env_skirt.segment(cpw_end+wgap+gapSkirt_big, **spec)
        
    # To couple the CPW to a qubit island
    meander_wvg_env_skirt.segment(yMeander/2-radius_turn*d_wvg, **spec)\
        .turn(radius_turn*d_wvg, 'l', **spec)\
        .segment(gapSkirt_big, **spec)
        
    if lambda_res == 0.25:
        tail_wvg_env_skirt = gdspy.Path(wcc+2*wgap+2*gapSkirt_big, (position[0]-wgap-xBase+yMeander/2-gapSkirt_big-xBase_gap, position[1]-wcc-2*wgap))
        tail_wvg_env_skirt.segment(dturn-gapSkirt_big, '-x', **spec)\
            .turn(radius_turn*d_wvg, 'l', **spec)\
            .segment(cpw_cc+gapSkirt_big, **spec)
        meander_wvg_env_skirt = gdspy.boolean(meander_wvg_env_skirt,tail_wvg_env_skirt,'or',**spec) 
    
    # Central line of the meanders with big hole region
    meander_wvg_cc = gdspy.Path(wcc-2*gapSkirt_big, (position[0]-xBase+yMeander/2+gapSkirt_big, position[1]-wcc-2*wgap))
    meander_wvg_cc.segment(xBase-gapSkirt_big, '+x', **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\
                .segment(lMeander, **spec)\
                .turn(radius_turn*d_wvg, 'r', **spec)\

    for i in range(N_wvg-1):
        meander_wvg_cc.segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'l', **spec)\
                    .segment(yMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
                    .segment(lMeander, **spec)\
                    .turn(radius_turn*d_wvg, 'r', **spec)\
    
    # To terminate the CPW as a common l/2 resonator
    # meander_wvg_cc.segment(cpw_end-gapSkirt_big, **spec)
    
    # To couple the CPW to a qubit island   
    meander_wvg_cc.segment(yMeander/2-radius_turn*d_wvg, **spec)\
        .turn(radius_turn*d_wvg, 'l', **spec)\
        .segment(2*gapSkirt_big, **spec)   
    
    if lambda_res == 0.25:
        tail_wvg_cc = gdspy.Path(wcc-2*gapSkirt_big, (position[0]-xBase+yMeander/2+gapSkirt_big, position[1]-wcc-2*wgap))
        tail_wvg_cc.segment(dturn+xBase_gap+wgap+gapSkirt_big, '-x', **spec)\
            .turn(radius_turn*d_wvg, 'l', **spec)\
            .segment(cpw_cc+gapSkirt_big, **spec)
        meander_wvg_cc = gdspy.boolean(meander_wvg_cc,tail_wvg_cc,'or',**spec) 

    # Merge skirt launchers and skirt meanders
    meander_wvg_skirt = gdspy.boolean(meander_wvg_out_skirt, meander_wvg_in_skirt,"not")
    meander_wvg_skirt_neg = gdspy.boolean(meander_wvg_env_skirt,meander_wvg_skirt,"not")
    meander_wvg_skirt_sh_bare = gdspy.boolean(meander_wvg_skirt_neg,meander_wvg_cc,"not",layer = layer_skirt_big)
    meander_wvg_skirt_sh_coupler = gdspy.boolean(meander_wvg_skirt_sh_bare,meander_coupler_neg,"not",layer = layer_skirt_big)
    meander_wvg_skirt_sh = gdspy.boolean(meander_wvg_skirt_sh_coupler,meander_coupler_Skirt,"or",layer = layer_skirt_big)
    
    meander_wvg_env_skirt_bare = gdspy.boolean(meander_wvg_env_skirt,meander_wvg_cc,"not", layer = layer_skirt_small)
    meander_wvg_env_skirt = gdspy.boolean(meander_wvg_env_skirt_bare,meander_coupler_bh,"or", layer = layer_skirt_small)
    
    if direction == '+y':
        meander_wvg = meander_wvg.rotate(1 *np.pi, position)
        meander_wvg_skirt_sh = meander_wvg_skirt_sh.rotate(1 *np.pi, position)
        meander_wvg_env_skirt = meander_wvg_env_skirt.rotate(1 *np.pi, position)
        
    elif direction == '-y':
        meander_wvg = meander_wvg.rotate(0 * np.pi, position)
        meander_wvg_skirt_sh = meander_wvg_skirt_sh.rotate(0 *np.pi, position)
        meander_wvg_env_skirt = meander_wvg_env_skirt.rotate(0 *np.pi, position)

        
    return meander_wvg, meander_wvg_skirt_sh, meander_wvg_env_skirt



 

def waveguide(cell,
              position = (0,0),
              wcc = 45.0,
              wgap = 0.65,
              length = 6000.0,
              length2 = 7000.0,
              width2 = 2000.0,
              wcc_launcher = 150.0,
              wgap_launcher = 7.5,
              len_launcher = 300.0,
              len2_launcher = 300.0,
              gapSkirt_big = 5.0, 
              gapSkirt_small = 0.5, 
              layer_skirt_big = 6, 
              layer_skirt_small = 6, 
              layer_core = 3,
              layer_gap = 0,
              datatype = 0):   
              
        
    '''
    An horizontal waveguide.
    '''
    
    #if Status=='fabrication':
    #    wgap = wgap-0.1
    #    wcc = wcc+0.1
    #    wgap_launcher = wgap_launcher-0.1
    #    wcc_launcher = wcc_launcher+0.1
    #    gapSkirt_small = gapSkirt_small+0.05
    #    gapSkirt_big = gapSkirt_big+0.05
        
    # Straight horizontal waveguide
    total_length = length + 2*(len_launcher + len2_launcher)
    waveguide_points = [(-total_length/2, 0), (-len2_launcher-length/2, 0), (-length/2, 0), (length/2, 0), (+len2_launcher+length/2, 0), (+total_length/2, 0)]
    widths_gaps = [wgap_launcher, wgap_launcher, wgap, wgap, wgap_launcher, wgap_launcher]
    widths_core = [wcc_launcher, wcc_launcher, wcc, wcc, wcc_launcher, wcc_launcher]
    distances = [sum(x) for x in zip(widths_core, widths_gaps)]
    if Status=='simulation':
        gaps_polypath = gdspy.PolyPath(waveguide_points, widths_gaps, number_of_paths=2, distance=distances, layer=layer_gap)
    if Status=='fabrication':
        gaps_polypath = gdspy.PolyPath(waveguide_points, widths_gaps, number_of_paths=2, distance=distances, layer=layers['Coarse beam'])
    
    # Skirts
    # Create Skirt-enlarged launchers and feedline 
    widths_gaps_skirt_big = [wgap_launcher+2*gapSkirt_big, wgap_launcher+2*gapSkirt_big, wgap+2*gapSkirt_big,wgap+2*gapSkirt_big, wgap_launcher+2*gapSkirt_big, wgap_launcher+2*gapSkirt_big]
    widths_core_skirt_big = [wcc_launcher-2*gapSkirt_big, wcc_launcher-2*gapSkirt_big,wcc-2*gapSkirt_big,wcc-2*gapSkirt_big, wcc_launcher-2*gapSkirt_big, wcc_launcher-2*gapSkirt_big]
    distances_skirt_big = [sum(x) for x in zip(widths_core_skirt_big, widths_gaps_skirt_big)]
    gaps_polypath_skirt_big = gdspy.PolyPath(waveguide_points, widths_gaps_skirt_big, number_of_paths=2, distance=distances_skirt_big, layer=layer_skirt_big)

    # Create Skirt-less-enlarged launchers and feedline
    widths_gaps_skirt_small = [wgap_launcher+2*gapSkirt_small, wgap_launcher+2*gapSkirt_small, wgap+2*gapSkirt_small,wgap+2*gapSkirt_small, wgap_launcher+2*gapSkirt_small, wgap_launcher+2*gapSkirt_small]
    widths_core_skirt_small = [wcc_launcher-2*gapSkirt_small, wcc_launcher-2*gapSkirt_small,wcc-2*gapSkirt_small,wcc-2*gapSkirt_small, wcc_launcher-2*gapSkirt_small, wcc_launcher-2*gapSkirt_small]
    distances_skirt_small = [sum(x) for x in zip(widths_core_skirt_small, widths_gaps_skirt_small)]
    gaps_polypath_skirt_small = gdspy.PolyPath(waveguide_points, widths_gaps_skirt_small, number_of_paths=2, distance=distances_skirt_small, layer=layer_skirt_small)

    # Final result
    skirt_polypath = gdspy.boolean(gaps_polypath_skirt_big,gaps_polypath_skirt_small,"not",layer=layer_skirt_big)
    
    
    skirt_feedline_env = gaps_polypath_skirt_big
    
    #skirt_feedline_env = gdspy.boolean(skirt_polypath_big,meander_wvg_env_skirt,"or",layer=layers['Coarse holes'])
    
    
    return gaps_polypath, skirt_polypath, skirt_feedline_env






def holes(layer,
          reference,
          r = 0.04,
          d = 4.0*0.04,
          position = (0,0),
          length = 7000.0,
          width = 2000.0):
    '''
    Makes an array of circular gorundplane holes.
    '''
    
    X = position[0] - length/2
    Y = position[1] - width/2
    h = 0.5*np.sqrt(3)*d
    Nx = int(length/(2*h))
    Ny = int(width/(2*d))
    
    hole1 = gdspy.Round((0,0), r, layer=layer)
    hole2 = gdspy.Round((0,d), r, layer=layer)
    hole3 = gdspy.Round((h,1.5*d), r, layer=layer)
    hole4 = gdspy.Round((h,0.5*d), r, layer=layer)
    reference_cell = gdspy.Cell(reference)
    reference_cell.add(hole1)
    reference_cell.add(hole2)
    reference_cell.add(hole3)
    reference_cell.add(hole4)

    holy_ground = gdspy.CellArray(ref_cell = reference_cell,
                                  columns = Nx,
                                  rows = Ny,
                                  spacing = (2*h, 2*d),
                                  origin = (X, Y))

    #cell.add(holy_ground)
    return holy_ground
    
    
    
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#                       CALL FUNCTIONS      
# ------------------------------------------------------------------------
    

                                                    
gaps_polypath, skirt_polypath, skirt_feedline_env = waveguide(cell = cell_example,
                                                            position = (0,0),
                                                            wcc = wcc,
                                                            wgap = wgap,
                                                            length = length,
                                                            length2 = length2,
                                                            width2 = width2,
                                                            wcc_launcher = wcc_launcher,
                                                            wgap_launcher = wgap_launcher,
                                                            len_launcher = len_launcher,
                                                            len2_launcher = len2_launcher,
                                                            gapSkirt_big = 5.0, 
                                                            gapSkirt_small = 0.5, 
                                                            layer_skirt_big = layers['Fine holes'], 
                                                            layer_skirt_small = layers['Fine holes'], 
                                                            layer_core = layers['Core'],
                                                            layer_gap = layers['Waveguide'],
                                                            datatype = 0)


  
for ii in range(N_cpw): 
    meander_wvg, meander_wvg_skirt_sh, meander_wvg_env_skirt = meandered_waveguide(cell = cell_example,
                                                      position = positions_cpw[ii],
                                                      direction = directions_cpw[ii],
                                                      wcc = wcc_i[ii],
                                                      wgap = wgap_i[ii],
                                                      yMeander = yMeander_i[ii], # Determines the horizontal part of the meander
                                                      d_wvg = dturn, # Determines the diameter of the turn
                                                      N_wvg = Ns_meanders[ii], # Determines the number of turns of the meander
                                                      cpw_cc = cpw_cc_i[ii], # Determines the part of the CPW in 'contact' with the feedline
                                                      cpw_end = cpw_end_i[ii], # Determines the end part of the CPW res
                                                      radius_turn = 0.5, # Factor to detrmine the diameter of the turn
                                                      lMeander = 0.0, # Determines the horizontal part of the meander
                                                      c_strength = 0.7, # Determines vertical length of the coupler, LIMITATION: 02/11/22- CAN ONLY GO UP TO A CERTAIN VALUE, SINCE DOES NOT HAVE STRAIGHT PART
                                                      gapSkirt_big = 5.0, # Distance between objects and the big holes region (in the regions that also have small holes)  (um)
                                                      gapSkirt_small = 0.5, # Distance between objects and holes region  (um)
                                                      coupler = [xHole_i[ii],yHole_i[ii],Roundness_i[ii],xIsland_i[ii]],
                                                      gapCoupler = gapCoupler_i[ii],
                                                      lambda_res = lambda_res_ii[ii],
                                                      layer_skirt_big = layers['Fine holes'], 
                                                      layer_skirt_small = layers['Fine holes'],
                                                      layer_core = layers['Core'],
                                                      layer_gap = layers['Waveguide'],
                                                      datatype = 0)

    if Status=='simulation':
        if res_sim == False:
            # Merge feedline and holes' paths 
            gaps_polypath = gdspy.boolean(gaps_polypath,meander_wvg,"or")
        elif res_sim == True:
            # Merge feedline and holes' paths 
            gaps_polypath = gdspy.boolean(gaps_polypath,meander_wvg,"or")
            
        
    if Status=='fabrication':
        # Add Coarse beam 1 gaps
        gaps_polypath = gdspy.boolean(gaps_polypath,meander_wvg,"or",layer=layers['Coarse beam'])
        # Merge non big holes regions
        skirt_feedline_env = gdspy.boolean(skirt_feedline_env,meander_wvg_env_skirt,"or", layer=layers['Coarse holes'])
        # Merge small holes region
        skirt_polypath = gdspy.boolean(skirt_polypath,meander_wvg_skirt_sh,"or", layer=layers['Fine holes'])
        

             
        
if Status=='fabrication':
    dicing_rectangle(cell = cell_example,
                         position = (0,0),
                         length = dice_chip_x,
                         width = dice_chip_y,
                         thickness = t_rectangle,
                         layer_rectangle = layers['Frame'])
    markers(cell = cell_example,
             position = (0,0),
             length = chip_x,
             width = chip_y,
             layer_markers = layers['Markers'])

    cell_example.add(gaps_polypath)
    cell_example.add(skirt_polypath)
    cell_example.add(skirt_feedline_env)
    
    
    print("Drilling small holes...")
    holy_ground = holes(layer = layers['Small holes'],
                  reference = 'Small_holes',
                  r = 0.05,
                  d = 0.5,
                  position = (0,0),
                  length = chip_x-t_rectangle/2,
                  width = chip_y-t_rectangle/2)
    cell_example.add(holy_ground)
    
    print("Drilling big holes...")
    b = holes(layer = layers['Big holes'],
                  reference = 'Big_holes',
                  r = 0.250,
                  d = 3.0,
                  position = (0,0),
                  length = chip_x-t_rectangle/2,
                  width = chip_y-t_rectangle/2)
    cell_example.add(b)
    

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
        point1_b = (-3550, 2300)
        point2_b = (-1400, -300)
        #point1_b = (-3150, 1300)
        #point2_b = (-2250, -200)
        box = gdspy.Rectangle(point1_b, point2_b, layer=4, datatype=0)
        # Create intersection between box and inversion
        box_inv = gdspy.boolean(inv, box, "and")
        # Remove fracturing
        joined = gdspy.boolean(box_inv, None, "or", max_points=0)
        # Add box to the cell
        cell_example.add(joined)
 # ------------------------------------------------------------------------    
    
# ------------------------------------------------------------------ #
#      VIEWER
# ------------------------------------------------------------------ #

# View the layout using a GUI.
    
#gdspy.LayoutViewer(cells=cell_example)

# ------------------------------------------------------------------ #
#      OUTPUT
# ------------------------------------------------------------------ #

# Output the layout to a GDSII file (default to all created cells).
# Set the units we used to micrometers and the precision to nanometers.
from datetime import datetime
dt = datetime.now()

# if Status == 'simulation':
#     print('We are in a simulation')
# elif Status == 'fabrication':
#     Comsol == False
#     print('We are in the fabrication process')
    


gdspy.write_gds('{:%Y.%m.%d_%H.%M.%S}_{}_sim.gds'.format(dt,filename), unit=1.0e-6, precision=1.0e-9)
# if Output == True:
#     if Status == 'simulation':
#         # if Comsol == True:
#         #     gdspy.write_gds('./Designs_gds/{:%Y.%m.%d_%H.%M.}_{}_simcom.gds'.format(dt,filename), unit=1.0e-6, precision=1.0e-9)
#         #     %run ./macro_dxf.ipynb
#         if Comsol == False:
            
#     # if Status == 'fabrication':
    #     gdspy.write_gds('./Designs_gds/{:%Y.%m.%d_%H.%M.%S}_{}_fab.gds'.format(dt,filename), unit=1.0e-6, precision=1.0e-9)
        

        