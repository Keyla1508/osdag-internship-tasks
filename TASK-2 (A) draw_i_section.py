from OCC.Core.gp import gp_Vec, gp_Trsf
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Display.SimpleGui import init_display

def create_i_section(length, flange_width, height, flange_thickness, web_thickness):
    web_height = height - 2 * flange_thickness

    bottom_flange = BRepPrimAPI_MakeBox(length, flange_width, flange_thickness).Shape()

    top_flange = BRepPrimAPI_MakeBox(length, flange_width, flange_thickness).Shape()
    move_top = gp_Trsf()
    move_top.SetTranslation(gp_Vec(0, 0, height - flange_thickness))
    top_flange = BRepBuilderAPI_Transform(top_flange, move_top, True).Shape()

    web = BRepPrimAPI_MakeBox(length, web_thickness, web_height).Shape()
    move_web = gp_Trsf()
    move_web.SetTranslation(gp_Vec(0, (flange_width - web_thickness) / 2, flange_thickness))
    web = BRepBuilderAPI_Transform(web, move_web, True).Shape()

    section = BRepAlgoAPI_Fuse(bottom_flange, top_flange).Shape()
    section = BRepAlgoAPI_Fuse(section, web).Shape()

    return section

if __name__ == "__main__":
    length = 6096.0
    flange_width = 100.0
    height = 200.0
    flange_thickness = 10.8
    web_thickness = 5.7

    section = create_i_section(length, flange_width, height, flange_thickness, web_thickness)

    display, start_display, *_ = init_display()
    display.DisplayShape(section, update=True)
    display.FitAll()
    start_display()
