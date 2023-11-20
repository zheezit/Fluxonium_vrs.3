"""
Created by Federico Poggiali
QDev SQUID group
"""

import gdspy
import cdes
import numpy as np


def dicing_rectangle(
    position=(0, 0), length=10000.0, width=10000.0, thickness=100.0, layer_rectangle=1, layer_markers=4
):
    """
    A YxY mm rectangle surrounding everything.
    """
    # Frame
    X = length / 2
    Y = width / 2 + thickness
    point1_out = (position[0] - X - thickness / 2, position[1] - Y - thickness / 2)
    point2_out = (position[0] + X + thickness / 2, position[1] + Y + thickness / 2)
    point1_in = (position[0] - length / 2, position[1] - width / 2)
    point2_in = (position[0] + length / 2, position[1] + width / 2)
    outer = gdspy.Rectangle(point1_out, point2_out, layer=layer_rectangle, datatype=0)
    inner = gdspy.Rectangle(point1_in, point2_in, layer=layer_rectangle, datatype=0)
    merged = gdspy.fast_boolean(outer, inner, "xor", layer=layer_rectangle, datatype=0)

    # Add all the elements to the cell
    design_final = cdes.GenericShape()
    components = [merged]

    for component in components:
        design_final.add_to_drawing(component)

    return design_final


def cross_fun(position_cross=(0, 0), length_cross=0, thickness_cross=0, layer_cross=0):
    """
    A cross
    """
    cross_leg_1 = gdspy.Path(thickness_cross, (position_cross[0] - length_cross / 2, position_cross[1]))
    cross_leg_1.segment(length_cross, "+x")

    cross_leg_2 = gdspy.Path(thickness_cross, (position_cross[0], position_cross[1] - length_cross / 2))
    cross_leg_2.segment(length_cross, "+y")
    cross = gdspy.boolean(cross_leg_1, cross_leg_2, "or", layer=layer_cross)
    return cross


def markers(position=(0, 0), length=8000.0, width=8000.0, layer_markers_man=3, layer_markers_aut=5):
    # Markers for a square chip
    chip_x = length
    chip_y = width
    marker_separation = 200.0
    marker_line_sep = 3.0
    thickness_line = 2.5
    length_line = 83.0
    length_cross = 10
    thickness_cross = 0.4

    markers_all_man = cross_fun(
        position_cross=(position[0] + chip_x / 2, position[1] + chip_y / 2),
        length_cross=length_cross,
        thickness_cross=thickness_cross,
        layer_cross=layer_markers_man,
    )

    length_line_bare = 2 * length_line + length_cross + 2 * marker_line_sep
    markers_all_auto = cross_fun(
        position_cross=(position[0] + chip_x / 2, position[1] + chip_y / 2),
        length_cross=length_line_bare,
        thickness_cross=thickness_line,
        layer_cross=layer_markers_aut,
    )

    bb_0 = np.array(markers_all_man.get_bounding_box())
    marker_box_0 = gdspy.Rectangle(bb_0[0] - marker_line_sep, bb_0[1] + marker_line_sep, layer=layer_markers_aut)
    markers_all_auto = gdspy.boolean(markers_all_auto, marker_box_0, "not", layer=layer_markers_aut, datatype=0)

    for ii in range(2):
        for jj in range(2):
            for kk in range(5):
                # Cross and cross labels
                position_ky = (
                    (-1) ** ii * length / 2 + position[0],
                    (-1) ** jj * length / 2 + marker_separation * kk + position[1],
                )
                position_kx = (
                    (-1) ** ii * length / 2 + marker_separation * kk + position[0],
                    (-1) ** jj * length / 2 + position[1],
                )
                crossy = cross_fun(
                    position_cross=position_ky,
                    length_cross=length_cross,
                    thickness_cross=thickness_cross,
                    layer_cross=layer_markers_man,
                )

                markers_all_man = gdspy.boolean(markers_all_man, crossy, "or", layer=layer_markers_man, datatype=0)

                # Add text
                texty = gdspy.Text(
                    "{}".format(kk + 1), 8, (position_ky[0] + 6, position_ky[1] - 15), layer=layer_markers_man
                )
                markers_all_man = gdspy.boolean(markers_all_man, texty, "or", layer=layer_markers_man, datatype=0)
                crossx = cross_fun(
                    position_cross=position_kx,
                    length_cross=length_cross,
                    thickness_cross=thickness_cross,
                    layer_cross=layer_markers_man,
                )

                markers_all_man = gdspy.boolean(markers_all_man, crossx, "or", layer=layer_markers_man, datatype=0)
                textx = gdspy.Text(
                    "{}".format(kk + 1), 8, (position_kx[0] + 6, position_kx[1] - 15), layer=layer_markers_man
                )
                markers_all_man = gdspy.boolean(markers_all_man, textx, "or", layer=layer_markers_man, datatype=0)

                length_line_bare = 2 * length_line + length_cross + 2 * marker_line_sep
                cross_lines_barex = cross_fun(
                    position_cross=position_kx,
                    length_cross=length_line_bare,
                    thickness_cross=thickness_line,
                    layer_cross=layer_markers_aut,
                )

                bbx = np.array(crossx.get_bounding_box())
                marker_boxx = gdspy.Rectangle(
                    bbx[0] - marker_line_sep, bbx[1] + marker_line_sep, layer=layer_markers_aut
                )
                cross_linesx = gdspy.boolean(
                    cross_lines_barex, marker_boxx, "not", layer=layer_markers_aut, datatype=0
                )
                markers_all_auto = gdspy.boolean(
                    markers_all_auto, cross_linesx, "or", layer=layer_markers_aut, datatype=0
                )

                cross_lines_barey = cross_fun(
                    position_cross=position_ky,
                    length_cross=length_line_bare,
                    thickness_cross=thickness_line,
                    layer_cross=layer_markers_aut,
                )

                bby = np.array(crossy.get_bounding_box())
                marker_boxy = gdspy.Rectangle(
                    bby[0] - marker_line_sep, bby[1] + marker_line_sep, layer=layer_markers_aut
                )
                cross_linesy = gdspy.boolean(
                    cross_lines_barey, marker_boxy, "not", layer=layer_markers_aut, datatype=0
                )
                markers_all_auto = gdspy.boolean(
                    markers_all_auto, cross_linesy, "or", layer=layer_markers_aut, datatype=0
                )

    # Initialize cdes.GenericShape() and add marker:
    marker = [markers_all_auto, markers_all_man]

    return marker


def to_generic_shape(gds_objects):
    design_final = cdes.GenericShape()
    components = gds_objects

    for component in components:
        design_final.add_to_drawing(component)

    return design_final
