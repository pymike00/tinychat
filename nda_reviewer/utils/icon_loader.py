import os
import io
from cairosvg import svg2png
from PIL import Image
import customtkinter as ctk

def load_svg_icon(icon_name, size=(20, 20), color="#1E90FF"):
    icon_path = os.path.join("nda_reviewer", "assets", f"{icon_name}.svg")
    with open(icon_path, 'r') as file:
        svg_data = file.read()
    
    # Replace the color in the SVG
    svg_data = svg_data.replace('stroke="currentColor"', f'stroke="{color}"')
    
    # Convert SVG to PNG
    png_data = svg2png(bytestring=svg_data.encode('utf-8'), output_width=size[0], output_height=size[1])
    
    # Create PIL Image from PNG data
    image = Image.open(io.BytesIO(png_data))
    
    # Convert to CTkImage
    return ctk.CTkImage(light_image=image, dark_image=image, size=size)