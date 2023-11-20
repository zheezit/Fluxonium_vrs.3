import gdspy
import cdes
import numpy as np
from devdesign.JJsdesign.jj import *
from devdesign.essentials.shapes import *
from devdesign.essentials.essentials import *
from devdesign.essentials.markers import *

""" This code file creates an array of Jospehson Junctions with a pads around them."""

# Global settings of the device
global_settings = {
    "unit": 1.0e-6,
    "precision": 1.0e-9,
    "chip_size": [10000, 10000],
    "origin": "bottom_left_corner",
    "subtract_outside_metallizations": False,
    "main_layer": 0,
    "include_traps": False,
    "marker_layer": 10,
}

""" -------- """

# Design settings for Jospehson Junction
settings = {
    "Pad": 1,
    "pad_size_x": 600,
    "pad_size_y": 600,
    "pad_distance": 15,
    "offset": 1,
}


def sqaure_pad_sx(pad_size_x, pad_size_y, l, size_jj="size_jj"):
    pad = gdspy.Rectangle((0, 0), (pad_size_x, pad_size_y), layer=l)
    pad = center_app_point(pad)

    size_text = 0.075 * pad_size_x

    # label at top
    label_t = gdspy.Text(size_jj, size_text, position=(0, 0), horizontal=True, layer=l, datatype=0)
    label_t = center_app_point(label_t)
    label_t.translate(0, pad_size_y / 2 - (size_text) * 1.05)
    pad = gdspy.boolean(pad, label_t, "not", layer=l)

    # create label at bottom
    label_b = gdspy.Text(size_jj, size_text, position=(0, 0), horizontal=True, layer=l, datatype=0)
    label_b = center_app_point(label_b)
    label_b.translate(0, -pad_size_y / 2 + (size_text) * 1.05)
    pad = gdspy.boolean(pad, label_b, "not", layer=l)

    offset = 0.075 * pad_size_x

    # create sqaures to mark sx_pad
    sq = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq = center_app_point(sq)
    sq.translate(-pad_size_x / 2 + offset, -pad_size_x / 2 + offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    sq = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq = center_app_point(sq)
    sq.translate(+pad_size_x / 2 - offset, -pad_size_x / 2 + offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    sq = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq = center_app_point(sq)
    sq.translate(+pad_size_x / 2 - offset, +pad_size_x / 2 - offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    sq = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq = center_app_point(sq)
    sq.translate(-pad_size_x / 2 + offset, +pad_size_x / 2 - offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    return pad


def probe_sx(l):
    probe_points = [(0, 0), (7, 0), (15, 2.5), (19, 2.5), (19, 4.5), (0, 4.5)]
    probe_p = gdspy.Polygon(probe_points, layer=l)

    return probe_p


def sqaure_pad_dx(pad_size_x, pad_size_y, l, size_jj="size_jj"):
    pad = gdspy.Rectangle((0, 0), (pad_size_x, pad_size_y), layer=l)
    pad = center_app_point(pad)

    size_text = 0.075 * pad_size_x

    # label at top
    label_t = gdspy.Text(size_jj, size_text, position=(0, 0), horizontal=True, layer=l, datatype=0)
    label_t = center_app_point(label_t)
    label_t.translate(0, pad_size_y / 2 - (size_text) * 1.05)
    pad = gdspy.boolean(pad, label_t, "not", layer=l)

    # create label at bottom
    label_b = gdspy.Text(size_jj, size_text, position=(0, 0), horizontal=True, layer=l, datatype=0)
    label_b = center_app_point(label_b)
    label_b.translate(0, -pad_size_y / 2 + (size_text) * 1.05)
    pad = gdspy.boolean(pad, label_b, "not", layer=l)

    offset = 0.075 * pad_size_x

    # create sqaures to mark sx_pad
    sq_1 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_2 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_1 = center_app_point(sq_1)
    sq_2 = center_app_point(sq_2).translate(0.05 * pad_size_x + 0.01 * pad_size_x, 0)
    sq = gdspy.boolean(sq_1, sq_2, "or", layer=l)
    sq = center_app_point(sq)
    sq.translate(-pad_size_x / 2 + offset, -pad_size_x / 2 + offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    sq_1 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_2 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_1 = center_app_point(sq_1)
    sq_2 = center_app_point(sq_2).translate(0.05 * pad_size_x + 0.01 * pad_size_x, 0)
    sq = gdspy.boolean(sq_1, sq_2, "or", layer=l)
    sq = center_app_point(sq)
    sq.translate(-pad_size_x / 2 + offset, +pad_size_x / 2 - offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    sq_1 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_2 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_1 = center_app_point(sq_1)
    sq_2 = center_app_point(sq_2).translate(0.05 * pad_size_x + 0.01 * pad_size_x, 0)
    sq = gdspy.boolean(sq_1, sq_2, "or", layer=l)
    sq = center_app_point(sq)
    sq.translate(+pad_size_x / 2 - offset, +pad_size_x / 2 - offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    sq_1 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_2 = gdspy.Rectangle((0, 0), (0.05 * pad_size_x, 0.05 * pad_size_y), layer=l)
    sq_1 = center_app_point(sq_1)
    sq_2 = center_app_point(sq_2).translate(0.05 * pad_size_x + 0.01 * pad_size_x, 0)
    sq = gdspy.boolean(sq_1, sq_2, "or", layer=l)
    sq = center_app_point(sq)
    sq.translate(+pad_size_x / 2 - offset, -pad_size_x / 2 + offset)
    pad = gdspy.boolean(pad, sq, "not", layer=l)

    return pad


def probe_dx(l):
    probe_points = [(0, 0), (0, -4.5), (-19, -4.5), (-19, -2.5), (-15, -2.5), (-7, -0)]
    probe_p = gdspy.Polygon(probe_points, layer=l)

    return probe_p


def pads(pad_size_x, pad_size_y, dist_x_jj, dist_y_jj, l, size_jj="size_jj"):
    pad = sqaure_pad_sx(pad_size_x, pad_size_y, l, size_jj=size_jj)
    pad_size = size(pad)
    probe_obj = probe_sx(l)
    probe_obj = probe_obj.translate(pad_size[0] / 2, 0)
    sx = gdspy.boolean(pad, probe_obj, "or", layer=l)
    sx = center_app_point(sx)

    pad = sqaure_pad_dx(pad_size_x, pad_size_y, l, size_jj=size_jj)
    pad_size = size(pad)
    probe_obj = probe_dx(l)
    probe_obj = probe_obj.translate(-pad_size[0] / 2, -dist_y_jj)
    dx = gdspy.boolean(pad, probe_obj, "or", layer=l)
    dx = center_app_point(dx)

    size_sx = size(sx)
    size_dx = size(dx)

    sx.translate(-size_sx[1] / 2, 0)
    dx.translate(size_dx[1] / 2 + dist_x_jj, 0)

    pads = gdspy.boolean(sx, dx, "or", layer=l)
    pads = center_app_point(pads)

    return pads


def jj(size_electrode, length, l):
    p1 = 0.8
    p2 = p1 - 0.2
    bottom_electrode = gdspy.Rectangle((0, 0), (p1 * length, size_electrode), layer=l)
    bottom_electrode_u = gdspy.Rectangle((p1 * length, 0), (length, size_electrode), layer=l + 1)
    top_electrode = gdspy.Rectangle((0, 0), (size_electrode, p1 * length), layer=l)
    top_electrode_u = gdspy.Rectangle((0, p1 * length), (size_electrode, length), layer=l + 1)

    top_electrode.translate(0, -0.2 * length)
    bottom_electrode.translate(-0.2 * length, 0)

    bottom_electrode_u.translate(-0.2 * length, 0)
    top_electrode_u.translate(0, -0.2 * length)

    jj_cross = gdspy.boolean(bottom_electrode, top_electrode, "or", layer=l)
    jj_undercut = gdspy.boolean(bottom_electrode_u, top_electrode_u, "or", layer=l + 1)

    ov_sub = -0.4  # overlap to substrate
    patch_t = gdspy.Rectangle((-p2, p2 * length - ov_sub), (size_electrode + p2, length), layer=l + 1)
    patch_b = gdspy.Rectangle((p2 * length - ov_sub, -p2), (length, size_electrode + p2), layer=l + 2)

    patch_b.translate(-0.2 * length, 0)
    patch_t.translate(0, -0.2 * length)

    patches = gdspy.boolean(patch_b, patch_t, "or", layer=l + 2)

    return jj_cross, jj_undercut, patches


def DUT_manhattan_classic_patch(size, layer, name="DUT_manhattan_classic_patch"):
    pads_obj = pads(400, 400, 21, -2.7, layer, size_jj=str(int(size * 10e2)) + "nm")
    manhattan, undercut, patch = jj(size, 7, layer + 1)

    device_cell = gdspy.Cell(name)
    device_cell.add(pads_obj)

    jj_cell = gdspy.Cell("JJ_manhattan_" + str(int(size * 10e2)) + "nm")
    jj_cell.add([manhattan, undercut, patch])

    ref = gdspy.CellReference(jj_cell, (-2.5, -1.1))
    device_cell.add(ref)

    return device_cell, jj_cell


device, jj_cell = DUT_manhattan_classic_patch(0.100, 53)


ground_plane = gdspy.Rectangle((0, 0), (10000, 10000), layer=1)
# insert markers
markers = markers(position=(5000, 5000), length=7000.0, width=7000.0, layer_markers_man=3, layer_markers_aut=5)

chip = gdspy.Cell("Chip")
chip.add(gdspy.CellArray(device, 7, 14, origin=(2500, 2100), spacing=(875, 450)))
chip.add(gdspy.CellArray(device, 1, 12, origin=(1500, 3000), spacing=(875, 450)))
chip.add(gdspy.CellArray(device, 1, 12, origin=(8700, 3000), spacing=(875, 450)))
chip.add(gdspy.CellArray(device, 6, 1, origin=(3300, 1600), spacing=(875, 450)))
chip.add(gdspy.CellArray(device, 6, 1, origin=(3300, 8600), spacing=(875, 450)))
chip.add(ground_plane)
chip.add(markers)

writer = gdspy.GdsWriter("/Users/federicopoggiali/Desktop/JJ_chip.gds", unit=1.0e-6, precision=1.0e-9)
writer.write_cell(jj_cell)
writer.write_cell(device)
writer.write_cell(chip)


writer.close()
