import sys
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


def create_rectangular_prism(length=430.0, breadth=100.0, height=8.0):
    box = BRepPrimAPI_MakeBox(length, breadth, height).Shape()
    return box


def transform_prism(box, translation=(0, 0, 0), rotation_axis=None, rotation_angle_deg=0):
    trsf = gp_Trsf()

    if rotation_axis and rotation_angle_deg != 0:
        point, direction = rotation_axis
        axis = gp_Ax1(gp_Pnt(*point), gp_Dir(*direction))
        trsf.SetRotation(axis, rotation_angle_deg * 3.1415926535 / 180)

    trsf.SetTranslation(gp_Vec(*translation))
    prism = BRepBuilderAPI_Transform(box, trsf, True).Shape()
    return prism


def display_prism(shape):

    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(shape, update=True)
    start_display()


if __name__ == "__main__":
    flat_bar = create_rectangular_prism()
    positioned_bar = transform_prism(flat_bar, translation=(0, 0, 100))
    display_prism(positioned_bar)