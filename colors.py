# colors.py 

def convert_hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class Colors:
    TanLight = convert_hex_to_rgb("#dabc94")
    TanDark = convert_hex_to_rgb("#c49e78")
