import pymel.core as pm

def change(target, color):
    shape = pm.listRelatives(target, shapes = True)

    dic = {'black': 1,
        'dark_grey': 2,
        'light_grey': 3,
        'red': 4,
        'dark_blue': 5,
        'blue': 6,
        'dark_green': 7,
        'dark_purple': 8,
        'pink': 9,
        'orange': 10,
        'brown': 11,
        'bright_orange': 12,
        'bright_red': 13,
        'bright_green': 14,
        'dark_blue': 15,
        'white': 16, 
        'yellow': 17,
        'light_blue': 18,
        'light_green': 19,
        'light_pink': 20,
        'light_orange': 21,
        'light_yellow': 22,
        's_green': 23,
        's_orange': 24,
        's_yellow': 25,
        's_lime': 26,
        's_green2': 27,
        's_blue': 28,
        's_blue2': 29,
        's_purple': 30,
        's_red': 31,
        }
    
    shape_name = shape[0].name()
    pm.setAttr(shape_name + '.overrideEnabled', True)
    pm.setAttr(shape_name + '.overrideColor', dic[color])

    shape[0].setObjectColor(8)

