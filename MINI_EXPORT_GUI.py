import os
import math
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import re
from tkinter import ttk
import tkinterDnD 
from PIL import Image
import json
import random

direktorij_za_eksport = "E:\PROGRAMIRANJE\JOBFAIR_LIGHTROOM_PLUGIN\PYTHON_EXPORT\FOTO_LIGHTROOM_PLUGIN\KRIVI_PUT"


root = tkinterDnD.Tk()  
root.title("Mini_export_FOTOKSET beta")

stringvar = tk.StringVar()
folder = tk.StringVar();
folder.set('Export folder jos nije odabran!')
stringvar.set('drag and drop slike ovdje')

watermark = tk.StringVar();
watermark.set('Watermark jos nije odabran!')

plavi = tk.StringVar();
plavi.set('Plavi filter jos nije odabran!')



def drop(event):
    # This function is called when stuff is dropped into a widget
    global a
    stringvar.set(event.data)
    print(stringvar.get())

def kreni():
    print("kreni")

def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    foo = ["kae z glavom", "dolje uprava", "baci baci", "nos ti posran"]
    return (tkinterDnD.COPY, "DND_Text", random.choice(foo))


def select_folder():
    directory = filedialog.askdirectory()
    direktorij_za_eksport = directory
    print("selektan: " + direktorij_za_eksport)
    folder.set(directory)
    print(folder.get())

def select_watermark():
    directory = filedialog.askopenfilename()
    watermark.set(directory)
    print(watermark.get())

def select_filter():
    directory = filedialog.askopenfilename()
    plavi.set(directory)
    print(plavi.get())

def citaj_podatke(): #podaci u obliku JSON dictionary     
    f = open("demofile.txt", "r")
    podatci = json.loads(f.read())
    return podatci




def glavna_funk():

    #overlay_path = plavi.get()
    #watermark_path = watermark.get()
    folder_path = folder.get()
    print(Var1.get())
    print(Var2.get())
    print(Var3.get())

    if int(Var3.get()) == 1:
        target_size = 1024
    else:
        target_size = 2048




    overlay_path = 'plavi_filter.png'
    watermark_path = 'FOTO_watermark.png'
    #folder_path = 'E:\GOOGLE_DRIVE\prijenos\TEST_PROGRAM'

    pattern = r'\{([^}]+)\}|([^ ]+)'
    matches = re.findall(pattern, stringvar.get())

    # Initialize an empty list to store individual file paths
    file_paths = []

    # Iterate through the matches and add them to the list
    for match in matches:
        # If the match is enclosed in curly braces, use the content inside the braces
        if match[0]:
            file_paths.append(match[0])
        # If the match is not enclosed in curly braces, use the whole match
        elif match[1]:
            file_paths.append(match[1])
    i = 0
    
    progres = ttk.Progressbar(root, orient=tk.HORIZONTAL)
    progres.pack(fill="both", expand=True, padx=10, pady=10)
    i = 0
    j = len(file_paths)
    progres['value'] = 0
    for image_path in file_paths:
        print(direktorij_za_eksport)
        progres['value'] += 5
        if image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        with Image.open(image_path) as image:
                            width, height = image.size

                            # Calculate the aspect ratio
                            aspect_ratio = width / height

                            # Set the new width and height based on the target size and aspect ratio
                            if aspect_ratio > 1:  # Landscape image
                                new_width = target_size
                                new_height = int(target_size / aspect_ratio)
                            else:  # Portrait image
                                new_height = target_size
                                new_width = int(target_size * aspect_ratio)

                            # Resize and save the image
                            image.resize((new_width, new_height))
                            
                            if Var2.get() == 1: 
                               overlay_image = Image.open(overlay_path)
                               overlay_resized = overlay_image.resize(image.size)
                               image.paste(overlay_resized, (0, 0), mask=overlay_resized)

                            if Var1.get() == 1:
                                watermark_image = Image.open(watermark_path)
                                w, h = image.size
                                fr = int(math.sqrt(w * h * pow(0.15, 2)))
                                watermark_resized = watermark_image.resize((fr, fr))
                                image.paste(watermark_resized, (w - fr, h - fr), mask = watermark_resized)
                            new_path = direktorij_za_eksport + '/' + ime_eventa.get() + '_' + str(i) + '.jpg';
                            i = i + 1
                            image.save(new_path, optimize=True, quality=100)
                            
                    except OSError:
                        print("Failed to compress")


ime_eventa = Entry(root, width = 60)
ime_eventa.insert(0,'20230517_panel_rasprava_bw_mario_olcar')
ime_eventa.pack(padx = 10, pady = 10)



b1 = ttk.Button(root, text="Odaberi folder za spremanje!", command=select_folder)
b1.pack(fill="both", expand=True, padx=10, pady=10)
"""""
b2 = ttk.Button(root, text="Odaberi watermark!", command=select_watermark)
b2.pack(fill="both", expand=True, padx=10, pady=3)

b3 = ttk.Button(root, text="Odaberi plavi filter!", command=select_filter)
b3.pack(fill="both", expand=True, padx=10, pady=10)
"""""
label_1 = tk.Label(root, textvar=folder, relief="solid")
label_1.pack(fill="both", expand=True, padx=10, pady=10)


label_watermark = tk.Label(root, textvar=watermark, relief="solid")
label_watermark.pack(fill="both", expand=True, padx=10, pady=3)

label_plavi = tk.Label(root, textvar=plavi, relief="solid")
label_plavi.pack(fill="both", expand=True, padx=10, pady=10)

label_2 = ttk.Label(root, ondrop=drop, ondragstart=drag_command,
                    textvar=stringvar, width=50,
                    padding=50, relief="solid", font="helvetica 14", 
justify="center", )
label_2.pack(fill="both", expand=FALSE, padx=10, pady=10)

Var1 = IntVar()
Var2 = IntVar()

ChkBttn = Checkbutton(root,text= "Watermark", width = 15, variable = Var1)
ChkBttn.pack(padx = 5, pady = 5)

ChkBttn2 = Checkbutton(root,text= "Plavi filter",  width = 15, variable = Var2)
ChkBttn2.pack(padx = 5, pady = 5)

Var3 = StringVar()
Var3.set(2)

RBttn = Radiobutton(root, text = "1024", variable = Var3,
                    value = 1)
RBttn.pack(padx = 5, pady = 5)

RBttn2 = Radiobutton(root, text = "2048", variable = Var3,
                     value = 2 )
RBttn2.pack(padx = 5, pady = 5)

b = ttk.Button(root, text="Kreni!", command=glavna_funk)
b.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()