import math
from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Pnt, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Display.SimpleGui import init_display

from draw_i_section import create_i_section  
from draw_rectangular_prism import create_rectangular_prism, transform_prism


def rotate_to_z_axis(shape):
    
    trsf = gp_Trsf()
    trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), -1.5708)  
    return BRepBuilderAPI_Transform(shape, trsf, True).Shape()


def create_batten(width=430.0, height=300.0, thickness=10.0):
       return BRepPrimAPI_MakeBox(thickness, width, height).Shape()


def assemble_laced_column():
    
    length = 6096.0
    flange_width = 100.0
    section_depth = 200.0
    flange_thickness = 10.8
    web_thickness = 5.7

    i_section_raw = create_i_section(length, flange_width, section_depth, flange_thickness, web_thickness)
    i_section_z = rotate_to_z_axis(i_section_raw)

    i_section1 = i_section_z

    offset = 355.7
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(0, offset, 0))
    i_section2 = BRepBuilderAPI_Transform(i_section_z, trsf, True).Shape()

    batten = create_batten()

    y_offset = (450.0 - 430.0) / 2  # 10.0
    z_bottom = 0
    z_top = length - 300.0

    trsf1 = gp_Trsf()
    trsf1.SetTranslation(gp_Vec(0, y_offset, z_bottom))
    batten1 = BRepBuilderAPI_Transform(batten, trsf1, True).Shape()

    trsf2 = gp_Trsf()
    trsf2.SetTranslation(gp_Vec(0, y_offset, z_top))
    batten2 = BRepBuilderAPI_Transform(batten, trsf2, True).Shape()

    trsf3 = gp_Trsf()
    trsf3.SetTranslation(gp_Vec(-210.0, y_offset, z_bottom))
    batten3 = BRepBuilderAPI_Transform(batten, trsf3, True).Shape()

    trsf4 = gp_Trsf()
    trsf4.SetTranslation(gp_Vec(-210.0, y_offset, z_top))
    batten4 = BRepBuilderAPI_Transform(batten, trsf4, True).Shape()

    assembly = BRepAlgoAPI_Fuse(i_section1, i_section2).Shape()
    for b in [batten1, batten2, batten3, batten4]:
        assembly = BRepAlgoAPI_Fuse(assembly, b).Shape()

    return assembly


def create_z_pattern_series(start_x1=0, start_y=10.0, back_side=False):
    z_positions = [
        5346.0, 4896.0, 4446.0, 3996.0, 3546.0, 3096.0,
        2646.0, 2196.0, 1746.0, 1296.0, 846.0, 396.0
    ]
    horiz_len = 450.0
    horiz_bar = create_rectangular_prism(length=8.0, breadth=horiz_len, height=100.0)

    bars = []
    for z in z_positions:
        bar = transform_prism(
            horiz_bar,
            translation=(start_x1, start_y, z)
        )
        bars.append(bar)


    if not back_side:
        diag_z_starts = [5830.0, 5380.0, 4930.0, 4480.0, 4030.0, 3580.0,
                         3130.0, 2680.0, 2230.0, 1780.0, 1330.0, 880.0]
        angle = -45
    else:
        diag_z_starts = [880.0, 1330.0, 1780.0, 2230.0, 2680.0,
                         3130.0, 3580.0, 4030.0, 4480.0, 4930.0, 5380.0, 5830.0]
        angle = 45

    diag_length = 450
    height = 100.0

    for z_start in diag_z_starts:
        y_start = start_y
        z_end = z_start - 450  
        y_end = start_y + 430  

        mid_y = (y_start + y_end) / 2
        mid_z = (z_start + z_end) / 2

        diagonal_bar = create_rectangular_prism(length=8.0, breadth=diag_length, height=height)

        centered = transform_prism(
            diagonal_bar,
            translation=(0, -diag_length / 2, -height / 2)
        )

        rotated = transform_prism(
            centered,
            rotation_axis=((0, 0, 0), (1, 0, 0)),
            rotation_angle_deg=angle
        )

        final = transform_prism(
            rotated,
            translation=(start_x1, mid_y, mid_z)
        )

        bars.append(final)

   
    fused = bars[0]
    for bar in bars[1:]:
        fused = BRepAlgoAPI_Fuse(fused, bar).Shape()

    return fused

def transform_prism(shape, translation=(0, 0, 0), rotation_axis=None, rotation_angle_deg=0):
    trsf = gp_Trsf()

    if rotation_axis and rotation_angle_deg != 0:
        origin_pt, direction_vec = rotation_axis
        axis = gp_Ax1(
            gp_Pnt(*origin_pt),
            gp_Dir(*direction_vec)
        )
        angle_rad = math.radians(rotation_angle_deg)
        trsf.SetRotation(axis, angle_rad)
        shape = BRepBuilderAPI_Transform(shape, trsf, True).Shape()

    trsf_translate = gp_Trsf()
    trsf_translate.SetTranslation(gp_Vec(*translation))
    shape = BRepBuilderAPI_Transform(shape, trsf_translate, True).Shape()

    return shape



if __name__ == "__main__":
    model = assemble_laced_column()

    z_pattern_front = create_z_pattern_series()

    z_pattern_back = create_z_pattern_series(start_x1=-210.0, back_side=True)

    model = BRepAlgoAPI_Fuse(model, z_pattern_front).Shape()
    model = BRepAlgoAPI_Fuse(model, z_pattern_back).Shape()

    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(model, update=True)
    display.FitAll()
    start_display()