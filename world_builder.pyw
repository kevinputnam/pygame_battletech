import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3 or better.")

from os.path import expanduser, isdir, isfile, dirname
import subprocess

import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import simpledialog
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
from tkinter.messagebox import askyesno
from tkinter.messagebox import showinfo
import tkinter.scrolledtext as scrolledtext
import PIL
from PIL import ImageTk, Image
from functools import partial
import tempfile
import manageSettings

title="2D World Builder"
settingsFileName = "settings.json"
homePath = expanduser("~")
tileSize = 8

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.title = title
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.define_fonts()
        self.create_widgets()
        self.collision_map = {}
        self.triggers = {}
        self.settings = manageSettings.load(settingsFileName)
        if "worldDir" in self.settings and isdir(self.settings["worldDir"]):
            self.worldDir = self.settings["worldDir"]
        else:
            self.worldDir = homePath
        if "worldFile" in self.settings and isfile(self.settings["worldFile"]):
            self.worldFile = self.settings["worldFile"]
        else:
            self.worldFile = None

    def define_fonts(self):
        self.boldLabelFont = font.Font(family='Verdana',size=-12, weight='bold')
        self.labelFont = font.Font(family='Verdana',size=-12)

    def create_widgets(self):
        self.winfo_toplevel().title(self.title)
        self.buttons = []

        self.menubar = tk.Menu(self.master)

        fileMenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open",command=self.openWorld,accelerator="Ctrl+O")
        fileMenu.add_command(label="New",command=self.newWorld,accelerator="Ctrl+N")
        fileMenu.add_command(label="Save",command=self.saveWorld,accelerator="Ctrl+S")

        helpMenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Help",menu=helpMenu)
        helpMenu.add_command(label="About",command=self.showAbout)

        self.master.config(menu=self.menubar)

        self.bind_all("<Control-o>", self.openWorldAccelerator)
        self.bind_all("<Control-n>", self.newWorldAccelerator)
        self.bind_all("<Control-s>", self.saveWorldAccelerator)

        self.mapFrame = tk.Frame(self, bd=2,relief=tk.SUNKEN)
        self.mapFrame.grid_rowconfigure(0,weight=1)
        self.mapFrame.grid_columnconfigure(0, weight=1)
        xscroll = tk.Scrollbar(self.mapFrame, orient=tk.HORIZONTAL)
        xscroll.grid(row=1,column=0,sticky=tk.E+tk.W)
        yscroll = tk.Scrollbar(self.mapFrame)
        yscroll.grid(row=0, column=1,sticky=tk.N+tk.S)
        self.mapCanvas= tk.Canvas(self.mapFrame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        self.mapCanvas.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        xscroll.config(command=self.mapCanvas.xview)
        yscroll.config(command=self.mapCanvas.yview)
        self.mapFrame.place(x=5,y=5,width=600,height=630)

        self.mapCursor = None
        self.mapImg = None
        self.editingCollisions = False
        self.editingTriggers = False
        self.mapBlockDrawing = True
        self.mapCollisionBlocks = {}
        self.mapTriggerBlocks = {}
        self.mapCanvas.config(scrollregion=self.mapCanvas.bbox(tk.ALL))
        self.mapCanvas.bind('<Motion>',self.mousePosiiton)
        self.mapCanvas.bind('<Button-1>',self.canvasClick)
        self.mapCanvas.bind('<B1-Motion>',self.canvasDrag)

        coordLbl = tk.Label(self,text="Tile coordinates (x,y): ",fg="gray")
        coordLbl.place(x=10,y=640)

        self.xyCoordValLbl = tk.Label(self,text="(-,-)",fg="gray")
        self.xyCoordValLbl.place(x=150,y=640)

        self.statusView = scrolledtext.ScrolledText(self)
        self.statusView.place(x=10,y=670,width=780)
        self.statusView["padx"]="3"
        self.statusView["border"]="0"
        self.statusView["height"]="15"

        self.statusView.columnconfigure(0,weight=1)
        self.statusView.rowconfigure(0,weight=1)

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.place(x=650,y=25)


        self.optionList = ['none']
        self.scenePicker = ttk.Combobox(self.buttonFrame,values=self.optionList,width=10)
        self.scenePicker.pack(side="top",pady=3)

        self.btn_switch_scene = tk.Button(self.buttonFrame)
        self.formatButton(self.btn_switch_scene,"gray")
        self.btn_switch_scene["text"]='Switch Scene'
        self.btn_switch_scene["command"] = partial(self.switchScene)
        self.btn_switch_scene.pack(side="top",pady=3,fill=tk.BOTH)

        self.btn_add_scene = tk.Button(self.buttonFrame)
        self.formatButton(self.btn_add_scene,"gray")
        self.btn_add_scene["text"]='Add Scene'
        self.btn_add_scene["command"] = partial(self.addScene)
        self.btn_add_scene.pack(side="top",pady=3,fill=tk.BOTH)

        self.btn_rmv_scene = tk.Button(self.buttonFrame)
        self.formatButton(self.btn_rmv_scene,"gray")
        self.btn_rmv_scene['text']='Remove Scene'
        self.btn_rmv_scene['command']=partial(self.removeScene)
        self.btn_rmv_scene.pack(side="top",pady=3, fill=tk.BOTH)

        separator = ttk.Separator(self.buttonFrame, orient='horizontal')
        separator.pack(side="top",pady=3, fill=tk.BOTH)

        #self.btn_edit_collisions = tk.Button(self.buttonFrame)
        #self.formatButton(self.btn_edit_collisions,"gray")
        #self.btn_edit_collisions["text"]='Edit Collisions'
        #self.btn_edit_collisions["command"] = partial(self.editCollisions)
        #self.btn_edit_collisions.pack(side="top",pady=3,fill=tk.BOTH)

        #self.btn_edit_triggers = tk.Button(self.buttonFrame)
        #self.formatButton(self.btn_edit_triggers,"gray")
        #self.btn_edit_triggers["text"]='Edit Triggers'
        #self.btn_edit_triggers["command"] = partial(self.editTriggers)
        #self.btn_edit_triggers.pack(side="top",pady=3, fill=tk.BOTH)

        self.btn_change_img = tk.Button(self.buttonFrame)
        self.formatButton(self.btn_change_img,"gray")
        self.btn_change_img["text"]='Change Image'
        self.btn_change_img["command"] = partial(self.changeImage)
        self.btn_change_img.pack(side="top",pady=3, fill=tk.BOTH)

        self.btn_change_name = tk.Button(self.buttonFrame)
        self.formatButton(self.btn_change_name,"gray")
        self.btn_change_name["text"]='Change Name'
        self.btn_change_name["command"] = partial(self.changeName)
        self.btn_change_name.pack(side="top",pady=3, fill=tk.BOTH)

        self.btn_print_collision_map = tk.Button(self.buttonFrame)
        self.formatButton(self.btn_print_collision_map,"gray")
        self.btn_print_collision_map["text"]='Get Collision Map'
        self.btn_print_collision_map["command"] = partial(self.getCollisionMap)
        self.btn_print_collision_map.pack(side="top",pady=3, fill=tk.BOTH)

    def formatButton(self,button,txtColor):
        btnFont = font.Font(family='Verdana', size=-12, weight='bold')
        button["font"] = btnFont
        button["fg"] = txtColor
        button["bg"]="#a2b5cd"
        button["border"]="0"

    def addButtons(self,choices,encounters):
        for widget in self.buttonFrame.winfo_children():
            widget.destroy()
        for choice in choices:
            button = tk.Button(self.buttonFrame)
            self.formatButton(button,"gray")
            button["text"]=choice
            buttonCommand = partial(self.buttonPush,choice)
            button["command"] = buttonCommand
            button.pack(side="left",padx=3)
        if len(encounters) > 0:
            label = tk.Label(self.buttonFrame,text="encounters: ",fg="gray")
            label.pack(side="left",padx=3)
        for encounter in encounters:
            button = tk.Button(self.buttonFrame,text=encounter)
            self.formatButton(button,"gray")
            buttonCommand = partial(self.encounterButtonPush,encounter)
            button["command"]=buttonCommand
            button.pack(side="left",padx=3)

    ##########################
    # Callback       methods #
    ##########################

    def mousePosiiton(self,event):
        if self.mapImg:
            canvas_x, canvas_y = self.mapCanvas.canvasx(event.x), self.mapCanvas.canvasy(event.y)
            tile_x = int(canvas_x/tileSize)
            tile_y = int(canvas_y/tileSize)
            if tile_x >= self.mapImg.width()/tileSize:
                tile_x = int((self.mapImg.width()-1)/tileSize)
            if tile_y >= self.mapImg.height()/tileSize:
                tile_y = int((self.mapImg.height()-1)/tileSize)
            print('x: '+ str(tile_x) +' y: ' + str(tile_y))
            self.xyCoordValLbl["text"] = "("+str(tile_x)+","+str(tile_y)+")"

            map_x = tile_x*tileSize
            map_y = tile_y*tileSize

            if not self.mapCursor:
                self.mapCursor = self.mapCanvas.create_rectangle(map_x,map_y,map_x+tileSize,map_y+tileSize)
            else:
                self.mapCanvas.coords(self.mapCursor,map_x,map_y,map_x+tileSize,map_y+tileSize)

    def canvasClick(self,event):
        if self.mapImg:
            canvas_x, canvas_y = self.mapCanvas.canvasx(event.x), self.mapCanvas.canvasy(event.y)
            tile_x = int(canvas_x/tileSize)
            tile_y = int(canvas_y/tileSize)
            if tile_x >= self.mapImg.width()/tileSize:
                tile_x = int((self.mapImg.width()-1)/tileSize)
            if tile_y >= self.mapImg.height()/tileSize:
                tile_y = int((self.mapImg.height()-1)/tileSize)

            map_x = tile_x*tileSize
            map_y = tile_y*tileSize

            if (tile_x,tile_y) in self.mapCollisionBlocks:
                self.mapBlockDrawing = False
                self.mapCanvas.delete(self.mapCollisionBlocks[(tile_x,tile_y)])
                del self.mapCollisionBlocks[(tile_x,tile_y)]
            else:
                self.mapBlockDrawing = True
                self.mapCollisionBlocks[(tile_x,tile_y)] = self.mapCanvas.create_rectangle(map_x,map_y,map_x+tileSize,map_y+tileSize,fill="red")

    def canvasDrag(self,event):
        if self.mapImg:
            canvas_x, canvas_y = self.mapCanvas.canvasx(event.x), self.mapCanvas.canvasy(event.y)
            tile_x = int(canvas_x/tileSize)
            tile_y = int(canvas_y/tileSize)
            if tile_x >= self.mapImg.width()/tileSize:
                tile_x = int((self.mapImg.width()-1)/tileSize)
            if tile_y >= self.mapImg.height()/tileSize:
                tile_y = int((self.mapImg.height()-1)/tileSize)

            map_x = tile_x*tileSize
            map_y = tile_y*tileSize

            if self.mapBlockDrawing:
                if not (tile_x,tile_y) in self.mapCollisionBlocks:
                    self.mapCollisionBlocks[(tile_x,tile_y)] = self.mapCanvas.create_rectangle(map_x,map_y,map_x+tileSize,map_y+tileSize,fill="red")
            else:
                if (tile_x,tile_y) in self.mapCollisionBlocks:
                    self.mapCanvas.delete(self.mapCollisionBlocks[(tile_x,tile_y)])
                    del self.mapCollisionBlocks[(tile_x,tile_y)]

    ##########################
    # Button command methods #
    ##########################

    def switchScene(self):
        if self.scenePicker.get():
            self.printSomething("Changing scene to "+ self.scenePicker.get() +".\n")

    def addScene(self):
        self.printSomething("Adding Scene: <scene name>.\n")
        sceneName = simpledialog.askstring('Add Scene','Name of the new scene:')
        if sceneName:
            self.optionList.append(sceneName)
            self.scenePicker.configure(values=self.optionList)
            self.scenePicker.set(sceneName)

    def removeScene(self):
        self.printSomething("Remove Scene: <scene name>?\n")

    def editCollisions(self):
        self.printSomething('Editing Collisions!\n')

    def editTriggers(self):
        self.printSomething('Editing Triggers!\n')

    def changeImage(self):
        img_path = askopenfilename(initialdir=self.worldDir, title="Pick and image.")
        if img_path:
            if isfile:
                self.printSomething('Change Image to ' + img_path + '.\n')
                try:
                    self.mapImg = ImageTk.PhotoImage(Image.open(img_path))
                    self.mapCanvas.create_image(0,0,image=self.mapImg,anchor='nw')
                    self.mapCanvas.config(scrollregion=self.mapCanvas.bbox(tk.ALL))

                except PIL.UnidentifiedImageError:
                    self.printSomething(img_path + " doesn't seem to be an image.\n")
                    showinfo('title',img_path + " is not an image.")


    def changeName(self):
        self.printSomething('Change name.\n')

    def getCollisionMap(self):
        if self.mapImg:
            self.collision_map = []
            for y in range(int((self.mapImg.height())/tileSize)):
                for x in range(int((self.mapImg.width())/tileSize)):
                    if (x,y) in self.mapCollisionBlocks:
                        self.collision_map.append(1)
                    else:
                        self.collision_map.append(0)
            print(self.collision_map)

    def buttonPush(self,choice):
        self.updateLocation(choice)

    def openWorld(self):
        path = askopenfilename(initialdir=self.worldDir, title="Open a world to edit.")
        if path:
            self.settings["worldFile"] = path
            self.settings["worldDir"] = dirname(path)
            self.worldDir = dirname(path)
            manageSettings.save(settingsFileName,self.settings)

    def newWorld(self):
        self.openSaveWorldAsDialog()

    def saveWorld(self):
        path = self.worldFile
        if not path:
            self.openSaveWorldAsDialog()

    def openWorldAccelerator(self,event):
        self.openWorld()

    def newWorldAccelerator(self,event):
        self.newWorld()

    def saveWorldAccelerator(self,event):
        self.saveWorld()

    def quitApplication(self):
        self.master.destroy()

    def showAbout(self):
        showinfo("About","Created by Kevin Putnam, 14/10/2022\n\n\"Fly you fools!\"\n               - Gandalf")

    #########################
    # Advanced menu methods #
    #########################

    ######################
    # GUI update methods #
    ######################

    def printSomething(self,theString,pos=tk.END):
        self.statusView.see("end")
        self.statusView.configure(state='normal')
        self.statusView.insert(pos,theString)
        self.statusView.configure(state='disabled')

    ##################
    # Worker methods #
    ##################

    def openSaveWorldAsDialog(self):
        path = asksaveasfilename(initialdir=self.worldDir,title="Choose a filename for this world.")
        if path:
            if isfile(path):
                showerror("File already exists. Choose a different file name.")
            else:
                self.settings["worldFile"] = path
                self.settings["worldDir"] = dirname(path)
                self.worldDir = dirname(path)
                manageSettings.save(settingsFileName,self.settings)

    ##################################################
    # Convenience methods for repeated functionality #
    ##################################################



#########################
# Main Application loop #
#########################

root = tk.Tk()
root.geometry("800x900+50+50")
root.resizable(False, False)
app = Application(master=root)
app.mainloop()
