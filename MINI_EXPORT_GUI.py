import os
import math
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import re
from tkinter import ttk
from PIL import Image, ImageEnhance
import json
import random
import ctypes  # An included library with Python install.
from tk import *

from dnd import *
import hook
from tk import Tk
from constants import *

import tkinter as tk
from dnd import DnDWrapper
import os.path

def save_with_limit(image, path, max_size=250*1024, quality=95):
    """Pokušava spremiti sliku tako da ne prelazi max_size bajtova."""
    temp_quality = quality  # Početna kvaliteta
    while temp_quality > 10:  # Sprječava preveliko smanjenje kvalitete
        image.save(path, optimize=True, quality=temp_quality)
        if os.path.getsize(path) <= max_size:
            break  # Ako je manja od 250 KB, završavamo
        temp_quality -= 1  # Smanjujemo kvalitetu za 5%
        
        
def ReduceOpacity(im, opacity):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im



def _init_tkdnd(master: tk.Tk) -> None:
    """DRAG N DROP"""

    """Add the tkdnd package to the auto_path, and import it"""

    platform = master.tk.call("tk", "windowingsystem")

    if platform == "win32":
        folder = "windows"
    elif platform == "x11":
        folder = "linux"
    elif platform == "aqua":
        folder = "mac"

    package_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder)
    master.tk.call('lappend', 'auto_path', package_dir)
    TkDnDVersion = master.tk.call('package', 'require', 'tkdnd')
    return TkDnDVersion


class Tk(tk.Tk, DnDWrapper):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.TkDnDVersion = _init_tkdnd(self)


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


f = open("data.txt", "w")
f.write("/KRIVI_PUT")



root = Tk()  
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
    foo = ["kae z glavom", "baci baci", "nos ti posran"]
    return (COPY, "DND_Text", random.choice(foo))


def select_eksport_folder():
    directory = filedialog.askdirectory()
    f = open("data.txt", "w")
    f.write(directory)
    folder.set(directory)

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
    f = open("data.txt", "r")
    
    direktorij_za_eksport = f.read()
    
    if direktorij_za_eksport == "E:/PROGRAMIRANJE/JOBFAIR_LIGHTROOM_PLUGIN/PYTHON_EXPORT/FOTO_LIGHTROOM_PLUGIN/KRIVI_PUT":
        Mbox('Greska!', 'Eksport folder nije odabran!', 0)
        return
        
    
    
    print(direktorij_za_eksport)
    #overlay_path = plavi.get()
    #watermark_path = watermark.get()
    folder_path = folder.get()
    print(Var1.get())
    print(Var2.get())
    print(Var3.get())
    print(Var_velicina.get())

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
    
    
    i = 0
    j = 0    
    for _ in file_paths:
        j += 1
    progres['value'] = 0
    for image_path in file_paths:
        progres['value'] += int((1)/j * 100)
        root.update()
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
                            image = image.resize((new_width, new_height))
                            
                            if Var2.get() == 1: 
                               overlay_image = Image.open(overlay_path)
                               overlay_resized = overlay_image.resize(image.size)
                               image.paste(overlay_resized, (0, 0), mask=overlay_resized)

                            if Var1.get() == 1:
                                watermark_image = Image.open(watermark_path)
                                w, h = image.size
                                fr = int(math.sqrt(w * h * pow(0.15, 2)))
                                watermark_resized = watermark_image.resize((fr, fr))
                                watermark_resized = ReduceOpacity(watermark_resized, 0.75)
                                image.paste(watermark_resized, (w - fr, h - fr), mask = watermark_resized)
                                
                            if i+1 < 10:
                                new_path = direktorij_za_eksport + '/' + ime_eventa.get() + '_' + '0' +  str(i+1) + '.jpg'
                            else:
                                new_path = direktorij_za_eksport + '/' + ime_eventa.get() + '_' +  str(i+1) + '.jpg'
                            i = i + 1
                            if Var_velicina.get() == 1:
                                save_with_limit(image, new_path)
                                print("\nosam\n\nosam\n\nosam\n")
                            else:
                                image.save(new_path, optimize=True, quality=100)
                            
                    except OSError:
                        print("Failed to compress")
                        
    progres['value'] = 100
    root.update()
    Mbox("gotovo", "Sve fotke su eksportane!", 0)
    
                    


ime_eventa = Entry(root, width = 60)
ime_eventa.insert(0,'20230517_panel_rasprava_bw_mario_olcar')
ime_eventa.pack(padx = 10, pady = 10)


b1 = ttk.Button(root, text="Odaberi folder za spremanje!", command=select_eksport_folder)
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
Var_velicina = IntVar()


ChkBttn = Checkbutton(root,text= "Watermark", width = 15, variable = Var1)
ChkBttn.pack(padx = 5, pady = 5)

ChkBttn = Checkbutton(root,text= "VEL <250KB", width = 15, variable = Var_velicina)
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



plavi.set("Plavi filter se nalazi u folderu programa")
watermark.set("Watermark se nalazi u folderu programa")

progres = ttk.Progressbar(root, orient=tk.HORIZONTAL)
progres.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()