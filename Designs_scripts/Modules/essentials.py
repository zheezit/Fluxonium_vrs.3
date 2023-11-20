import cdes
import gdspy


def size(poly):
    box = poly.get_bounding_box()
    x_dist = box[1][0] - box[0][0]
    y_dist = box[1][1] - box[0][1]
    return abs(x_dist), abs(y_dist)


def size_x(poly):
    box = poly.get_bounding_box()
    x_dist = box[1][0] - box[0][0]
    return abs(x_dist)


def size_y(poly):
    box = poly.get_bounding_box()
    y_dist = box[1][1] - box[0][1]
    return abs(y_dist)


def center_app_point(poly):
    x, y = size(poly)
    min_point = poly.get_bounding_box()[0]
    # transalte to cordinate (0,0)
    poly.translate(-min_point[0], -min_point[1])
    poly.translate(-x / 2, -y / 2)

    return poly


def to_generic_shape(gds_objects):

    design_final = cdes.GenericShape()
    components = gds_objects

    for component in components:
        design_final.add_to_drawing(component)

    return design_final

