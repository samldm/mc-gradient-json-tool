# Minecraft JSON gradient generator. If you use this script in any of your personal projects, please credit me and link the repository.
# Original Script by Bash Elliott.

# Fork by @SamLDM

import tkinter as tk
import numpy as np
from tkinter import ttk
from tkinter.colorchooser import askcolor

def hextorgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgbtohex(rgb):
    return '%02x%02x%02x' % rgb

def get_readable_text_color(background_color):
    r, g, b = hextorgb(background_color)
    luminance = 0.299 * r / 255 + 0.587 * g / 255 + 0.114 * b / 255
    text_color = "black" if luminance > 0.5 else "white"
    return text_color


def create_gradient(_text, _colorA, _colorB, bold=False, underline=False, italics=False):
    text = list(_text)
    num_points = len(text)
    colorA = hextorgb(_colorA)
    colorB = hextorgb(_colorB)
    points = np.linspace(colorA, colorB, num_points, dtype=int)
    hexes = [rgbtohex(tuple(point)) for point in points]

    final = '["",'
    for i in range(len(hexes)):
        do_bold = '"bold":true,' if bold else ''
        do_underline = '"underlined":true,' if underline else ''
        do_italics = '"italic":true,' if italics else ''
        final += '{{"text":"{}",{}{}{}"color":"#{}"}}'.format(
            text[i], do_bold, do_italics, do_underline, hexes[i]
        )
        if i != len(hexes) - 1:
            final += ','
    final += ']'
    return final

def generate_gradient():
    text = text_entry.get()
    userColorA = colorA_var.get()
    userColorB = colorB_var.get()
    bold = bold_var.get()
    underline = underline_var.get()
    italics = italics_var.get()
    print(text, userColorA, userColorB, bold, underline, italics)

    if text == "" or userColorA == "" or userColorB == "":
        return
    
    result = create_gradient(text, userColorA, userColorB, bold, underline, italics)
    result_text.set(result)
    print(result)

def colorA_callback():
    picker_result = askcolor(title="Choose start color")
    colorA_var.set(("" + picker_result[1]))
    color = picker_result[1]
    colorA_button.configure(text=(color or "click to choose"), fg=(color and get_readable_text_color(color) or '#ffffff'), bg=(color or '#45b592'))

def colorB_callback():
    picker_result = askcolor(title="Choose end color")
    colorB_var.set(("" + picker_result[1]))
    color = picker_result[1]
    colorB_button.configure(text=(color or "click to choose"), fg=(color and get_readable_text_color(color) or '#ffffff'), bg=(color or '#45b592'))

# window
root = tk.Tk()
root.minsize(width=260, height=300)
root.title("MCGT")

# top frame
top_frame = ttk.Frame(master=root, padding=(15, 15))
top_frame.pack(fill=tk.BOTH)

title_label = ttk.Label(master=top_frame, text="MCGradientTool", font=("Arial", 18))
title_label.pack(fill=tk.X)

# input frame
input_frame = ttk.Frame(master=root, padding=(15, 0))
input_frame.pack(fill=tk.X)

# input widgets
text_label = ttk.Label(master=input_frame, text="Text:")
text_label.pack(fill=tk.X)

text_entry = ttk.Entry(master=input_frame)
text_entry.pack(fill=tk.X)

colorA_var = tk.StringVar()
colorA_label = ttk.Label(master=input_frame, text="Start color:")
colorA_label.pack(fill=tk.X)

colorA_button = tk.Button(master=input_frame, command=colorA_callback, text="click to choose", fg='#ffffff', bg='#45b592', bd=0, padx=10)
colorA_button.pack(fill=tk.X)

colorB_var = tk.StringVar()
colorB_label = ttk.Label(master=input_frame, text="End color:")
colorB_label.pack(fill=tk.X)

colorB_button = tk.Button(master=input_frame, command=colorB_callback, text="click to choose", fg='#ffffff', bg='#45b592', bd=0, padx=10)
colorB_button.pack(fill=tk.X)



#   checkbox frame
checkbox_frame = ttk.Frame(master=input_frame, padding="10")
checkbox_frame.pack(fill=tk.X)

#   checkboxes
bold_var = tk.BooleanVar()
bold_checkbox = ttk.Checkbutton(master=checkbox_frame, text="Bold", variable=bold_var)
bold_checkbox.pack(side=tk.LEFT)

underline_var = tk.BooleanVar()
underline_checkbox = ttk.Checkbutton(master=checkbox_frame, text="Underline", variable=underline_var)
underline_checkbox.pack(side=tk.LEFT)

italics_var = tk.BooleanVar()
italics_checkbox = ttk.Checkbutton(master=checkbox_frame, text="Italics", variable=italics_var)
italics_checkbox.pack(side=tk.LEFT)


#   generate button

generate_button = tk.Button(master=input_frame, command=generate_gradient, text="Generate", fg='#ffffff', bg='#45b592', bd=0)
generate_button.pack(fill=tk.X)

#   result text

result_text = tk.StringVar()
result_entry = ttk.Entry(master=input_frame, textvariable=result_text, state="readonly")
result_entry.pack(fill=tk.X)


root.mainloop()