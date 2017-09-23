"""
Boulder Caves Editor.

Cave Set editor

Written by Irmen de Jong (irmen@razorvine.net)
License: MIT open-source.
"""

import os
import sys
import random
import getpass
import datetime
import tkinter
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.ttk
import tkinter.filedialog
import tkinter.colorchooser
import pkgutil
from typing import Tuple, List, Dict, Optional
from .game import __version__
from .caves import colorpalette, C64Cave, Cave as BaseCave, CaveSet, Palette, BDCFFOBJECTS
from .objects import GameObject, Direction
from . import tiles, objects, bdcff

# @todo add xy rulers
# @todo add snapping to xy with shift to draw straight lines
# @todo fix cave size issues when editing smaller/larger caves/intermissions
# @todo add support for initial direction of objects


class ScrollableImageSelector(tkinter.Frame):
    def __init__(self, master: tkinter.Widget, listener: 'EditorWindow') -> None:
        super().__init__(master)
        self.listener = listener
        self.treeview = tkinter.ttk.Treeview(self, columns=("tile",), displaycolumns=("tile",), height="5", selectmode=tkinter.BROWSE)
        self.treeview.heading("tile", text="Tile")
        self.treeview.column("#0", stretch=False, minwidth=40, width=40)
        self.treeview.column("tile", stretch=True, width=120)
        tkinter.ttk.Style(self).configure("Treeview", rowheight=24, background="#201000", foreground="#e0e0e0")
        sy = tkinter.Scrollbar(self, orient=tkinter.VERTICAL, command=self.treeview.yview)
        sy.pack(side=tkinter.RIGHT, expand=1, fill=tkinter.Y)
        self.treeview.configure(yscrollcommand=sy.set)
        self.treeview.pack(expand=1, fill=tkinter.Y)
        self.treeview.bind("<<TreeviewSelect>>", self.on_selected)
        self.treeview.bind("<Double-Button-1>", self.on_selected_doubleclick)
        self.selected_object = objects.BOULDER
        self.selected_erase_object = objects.EMPTY
        f = tkinter.Frame(master)
        tkinter.Label(f, text=" Draw: \n(Lmb)").grid(row=0, column=0)
        self.draw_label = tkinter.Label(f)
        self.draw_label.grid(row=0, column=1)
        tkinter.Label(f, text=" Erase: \n(Rmb)").grid(row=0, column=2)
        self.erase_label = tkinter.Label(f)
        self.erase_label.grid(row=0, column=3)
        tkinter.Label(f, text="Select for draw,\ndoubleclick to set erase.").grid(row=1, column=0, columnspan=4)
        f.pack(side=tkinter.BOTTOM, pady=4)

    def on_selected_doubleclick(self, event) -> None:
        item = self.treeview.focus()
        item = self.treeview.item(item)
        selected_name = item["values"][0].lower()
        self.selected_erase_object = objects.EMPTY
        for obj, displaytile in EDITOR_OBJECTS.items():
            if obj.name.lower() == selected_name:
                self.selected_erase_object = obj
                self.erase_label.configure(image=self.listener.tile_images[EDITOR_OBJECTS[obj]])
                self.listener.tile_erase_selection_changed(obj, displaytile)
                break

    def on_selected(self, event) -> None:
        item = self.treeview.focus()
        item = self.treeview.item(item)
        selected_name = item["values"][0].lower()
        self.selected_object = objects.BOULDER
        for obj, displaytile in EDITOR_OBJECTS.items():
            if obj.name.lower() == selected_name:
                self.selected_object = obj
                self.draw_label.configure(image=self.listener.tile_images[EDITOR_OBJECTS[obj]])
                self.listener.tile_selection_changed(obj, displaytile)
                break

    def populate(self, rows: List) -> None:
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        for image, name in rows:
            self.treeview.insert("", tkinter.END, image=image, values=(name,))
        self.treeview.configure(height=min(16, len(rows)))
        self.draw_label.configure(image=self.listener.tile_images[EDITOR_OBJECTS[self.selected_object]])
        self.erase_label.configure(image=self.listener.tile_images[EDITOR_OBJECTS[self.selected_erase_object]])


class Cave(BaseCave):
    def init_for_editor(self, editor: 'EditorWindow') -> None:
        self.editor = editor
        if not self.map:
            self.map = [(objects.EMPTY, Direction.NOWHERE)] * self.width * self.height
        self.snapshot()
        # draw the map into the canvas.
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.editor.set_canvas_tile(x, y, EDITOR_OBJECTS[self.map[x + self.width * y][0]])

    def __setitem__(self, xy: Tuple[int, int], thing: Tuple[GameObject, Direction]) -> None:
        x, y = xy
        obj, direction = thing
        assert isinstance(obj, GameObject) and isinstance(direction, Direction)
        if direction == Direction.NOWHERE:
            if obj in (objects.BUTTERFLY, objects.ALTBUTTERFLY):
                direction = Direction.DOWN      # @todo also support other default directions
            elif obj in (objects.FIREFLY, objects.ALTFIREFLY):
                direction = Direction.LEFT      # @todo also support other default directions
        self.map[x + self.width * y] = (obj, direction)
        self.editor.set_canvas_tile(x, y, EDITOR_OBJECTS[obj])

    def __getitem__(self, xy: Tuple[int, int]) -> Tuple[GameObject, Direction]:
        x, y = xy
        return self.map[x + self.width * y]

    def horiz_line(self, x: int, y: int, length: int, thing: Tuple[GameObject, Direction]) -> None:
        for xx in range(x, x + length):
            self[xx, y] = thing

    def vert_line(self, x: int, y: int, length: int, thing: Tuple[GameObject, Direction]) -> None:
        for yy in range(y, y + length):
            self[x, yy] = thing

    def snapshot(self) -> None:
        self.map_snapshot = self.map.copy()

    def restore(self) -> None:
        if self.map_snapshot:
            for y in range(self.height):
                for x in range(self.width):
                    obj, direction = self.map_snapshot[x + self.width * y]
                    self[x, y] = (obj, direction)
                    self.editor.set_canvas_tile(x, y, EDITOR_OBJECTS[obj])


# the objects available in the editor, with their tile number that is displayed
# (not all objects are properly recognizable in the editor by their default tile)
EDITOR_OBJECTS = {
    objects.AMOEBA: objects.AMOEBA.tile(),
    objects.BOULDER: objects.BOULDER.tile(),
    objects.BRICK: objects.BRICK.tile(),
    objects.BUTTERFLY: objects.BUTTERFLY.tile(2),
    objects.DIAMOND: objects.DIAMOND.tile(),
    objects.DIRT: objects.DIRT.tile(),
    objects.EMPTY: objects.EMPTY.tile(),
    objects.FIREFLY: objects.FIREFLY.tile(1),
    objects.HEXPANDINGWALL: objects.HEXPANDINGWALL.tile(),
    objects.INBOXBLINKING: objects.ROCKFORD.tile(),
    objects.MAGICWALL: objects.MAGICWALL.tile(2),
    objects.OUTBOXCLOSED: objects.OUTBOXBLINKING.tile(1),
    objects.SLIME: objects.SLIME.tile(1),
    objects.STEEL: objects.STEEL.tile(),
    objects.VEXPANDINGWALL: objects.VEXPANDINGWALL.tile(),
    objects.VOODOO: objects.VOODOO.tile()
}


class EditorWindow(tkinter.Tk):
    visible_columns = 40
    visible_rows = 22
    max_columns = 200
    max_rows = 200

    def __init__(self) -> None:
        super().__init__()
        self.geometry("+200+40")
        title = "Boulder Caves Editor {version:s} - by Irmen de Jong".format(version=__version__)
        self.wm_title(title)
        self.appicon = tkinter.PhotoImage(data=pkgutil.get_data(__name__, "gfx/gdash_icon_48.gif"))
        self.wm_iconphoto(self, self.appicon)
        if sys.platform == "win32":
            # tell windows to use a new toolbar icon
            import ctypes
            myappid = 'net.Razorvine.Bouldercaves.editor'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.playfield_columns = self.visible_columns
        self.playfield_rows = self.visible_rows
        rightframe = tkinter.Frame(self)
        cf = tkinter.Frame(rightframe)
        w, h = tiles.tile2pixels(self.visible_columns, self.visible_rows)
        self.canvas = tkinter.Canvas(cf, width=w * 2, height=h * 2, borderwidth=16, background="black", highlightthickness=1)
        self.canvas.grid(row=0, column=0)
        sy = tkinter.Scrollbar(cf, orient=tkinter.VERTICAL, command=self.canvas.yview)
        sx = tkinter.Scrollbar(cf, orient=tkinter.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)
        sy.grid(row=0, column=1, sticky=tkinter.N + tkinter.S)
        sx.grid(row=1, column=0, sticky=tkinter.E + tkinter.W)
        cf.pack()
        bf = tkinter.Frame(rightframe)
        f = tkinter.Frame(bf)
        tkinter.Label(f, text="Cave name:").grid(column=0, row=0, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Cave description:").grid(column=0, row=1, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="caveset Author:").grid(column=0, row=2, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="caveset WWW:").grid(column=0, row=3, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="caveset Date:").grid(column=0, row=4, sticky=tkinter.E, pady=2)
        self.cavename_var = tkinter.StringVar(value="A: test")
        self.cavedescr_var = tkinter.StringVar(value="A test cave.")
        self.cavesetauthor_var = tkinter.StringVar(value=getpass.getuser())
        self.cavesetwww_var = tkinter.StringVar()
        self.cavesetdate_var = tkinter.StringVar(value=datetime.datetime.now().date())
        self.caveintermission_var = tkinter.BooleanVar()
        tkinter.Entry(f, textvariable=self.cavename_var).grid(column=1, row=0, pady=2)
        tkinter.Entry(f, textvariable=self.cavedescr_var).grid(column=1, row=1, pady=2)
        tkinter.Entry(f, textvariable=self.cavesetauthor_var).grid(column=1, row=2, pady=2)
        tkinter.Entry(f, textvariable=self.cavesetwww_var).grid(column=1, row=3, pady=2)
        tkinter.Entry(f, textvariable=self.cavesetdate_var).grid(column=1, row=4, pady=2)
        tkinter.Checkbutton(f, text=" this is an Intermission.", variable=self.caveintermission_var,
                            selectcolor=self.cget("background")).grid(column=1, row=5, pady=2)
        f.pack(side=tkinter.LEFT, anchor=tkinter.N)
        defaults = bdcff.BdcffCave()
        f = tkinter.Frame(bf)
        tkinter.Label(f, text="Time limit [{:d}] :".format(defaults.cavetime)).grid(column=0, row=0, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Amoeba slow time [{:d}] :".format(defaults.amoebatime)).grid(column=0, row=1, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Magic wall time [{:d}] :".format(defaults.magicwalltime)).grid(column=0, row=2, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Amoeba limit factor [{:.4f}] :".format(defaults.amoebafactor)).grid(column=0, row=3, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Slime permeability [{:.4f}] :".format(defaults.slimepermeability)).grid(column=0, row=4, sticky=tkinter.E, pady=2)
        self.cavetimelimit_var = tkinter.IntVar(value=defaults.cavetime)
        self.caveamoebatime_var = tkinter.IntVar(value=defaults.amoebatime)
        self.cavemagicwalltime_var = tkinter.IntVar(value=defaults.magicwalltime)
        self.caveamoebafactor_var = tkinter.DoubleVar(value=defaults.amoebafactor)
        self.caveslimepermeability_var = tkinter.DoubleVar(value=defaults.slimepermeability)
        tkinter.Entry(f, width=8, textvariable=self.cavetimelimit_var).grid(column=1, row=0, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.caveamoebatime_var).grid(column=1, row=1, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.cavemagicwalltime_var).grid(column=1, row=2, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.caveamoebafactor_var).grid(column=1, row=3, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.caveslimepermeability_var).grid(column=1, row=4, pady=2)
        f.pack(side=tkinter.LEFT, padx=16, anchor=tkinter.N)
        f = tkinter.Frame(bf)
        self.cavediamondsrequired_var = tkinter.IntVar(value=defaults.diamonds_required)
        self.cavediamondvaluenorm_var = tkinter.IntVar(value=defaults.diamondvalue_normal)
        self.cavediamondvalueextra_var = tkinter.IntVar(value=defaults.diamondvalue_extra)
        self.cavewidth_var = tkinter.IntVar(value=self.playfield_columns)
        self.caveheight_var = tkinter.IntVar(value=self.playfield_rows)
        tkinter.Label(f, text="Diamonds required [{:d}] :".format(defaults.diamonds_required)).grid(column=0, row=0, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Diamond value normal [{:d}] :".format(defaults.diamondvalue_normal)).grid(column=0, row=1, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Diamond value extra [{:d}] :".format(defaults.diamondvalue_extra)).grid(column=0, row=2, sticky=tkinter.E, pady=(2, 16))
        tkinter.Label(f, text="Cave Width [{:d}] :".format(self.playfield_columns)).grid(column=0, row=3, sticky=tkinter.E, pady=2)
        tkinter.Label(f, text="Cave Height [{:d}] :".format(self.playfield_rows)).grid(column=0, row=4, sticky=tkinter.E, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.cavediamondsrequired_var).grid(column=1, row=0, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.cavediamondvaluenorm_var).grid(column=1, row=1, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.cavediamondvalueextra_var).grid(column=1, row=2, pady=(2, 16))
        tkinter.Entry(f, width=8, textvariable=self.cavewidth_var, state=tkinter.DISABLED).grid(column=1, row=3, pady=2)
        tkinter.Entry(f, width=8, textvariable=self.caveheight_var, state=tkinter.DISABLED).grid(column=1, row=4, pady=2)
        f.pack(side=tkinter.LEFT, padx=16, anchor=tkinter.N)

        bf.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        rightframe.pack(side=tkinter.RIGHT, padx=4, pady=4, fill=tkinter.BOTH, expand=1)

        buttonsframe = tkinter.Frame(self)
        lf = tkinter.LabelFrame(buttonsframe, text="Select object")
        self.imageselector = ScrollableImageSelector(lf, self)
        self.imageselector.pack(padx=4, pady=4)

        lf.pack(expand=1, fill=tkinter.BOTH)
        lf = tkinter.LabelFrame(buttonsframe, text="Keyboard commands")
        tkinter.Label(lf, text="F - flood fill").pack(anchor=tkinter.W, padx=4)
        tkinter.Label(lf, text="R - drop 10 objects randomly").pack(anchor=tkinter.W, padx=4)
        tkinter.Label(lf, text="S - make snapshot").pack(anchor=tkinter.W, padx=4)
        tkinter.Label(lf, text="U - restore snapshot").pack(anchor=tkinter.W, padx=4)
        tkinter.Label(lf, text="(activate map first)").pack(anchor=tkinter.W, padx=4)
        lf.pack(fill=tkinter.X, pady=4)
        lf = tkinter.LabelFrame(buttonsframe, text="Misc. edit")
        tkinter.Button(lf, text="Load", command=self.load).grid(column=0, row=0)
        tkinter.Button(lf, text="Save", command=self.save).grid(column=1, row=0)
        tkinter.Button(lf, text="Randomize", command=self.randomize).grid(column=0, row=1)
        tkinter.Button(lf, text="Wipe", command=self.wipe).grid(column=1, row=1)
        tkinter.Button(lf, text="Playtest", command=self.playtest).grid(column=0, row=2)
        tkinter.Button(lf, text="Defaults", command=self.set_defaults).grid(column=1, row=2)
        lf.pack(fill=tkinter.X, pady=4)
        lf = tkinter.LabelFrame(buttonsframe, text="Commodore-64 colors")
        self.c64colors_var = tkinter.IntVar()
        c64_check = tkinter.Checkbutton(lf, text="Enable retro palette", variable=self.c64colors_var, selectcolor=self.cget("background"),
                                        command=lambda: self.c64_colors_switched(self.c64colors_var.get()))
        c64_check.grid(column=0, row=0)
        self.c64random_button = tkinter.Button(lf, text="Random", state=tkinter.DISABLED, command=self.c64_colors_randomize)
        self.c64random_button.grid(column=0, row=1)
        tkinter.Button(lf, text="Edit", command=self.palette_edit).grid(column=1, row=1)
        lf.pack(fill=tkinter.X, pady=4)
        buttonsframe.pack(side=tkinter.LEFT, anchor=tkinter.N)
        self.buttonsframe = buttonsframe
        self.canvas.bind("<KeyPress>", self.keypress)
        self.canvas.bind("<KeyRelease>", self.keyrelease)
        self.canvas.bind("<Button-1>", self.mousebutton_left)
        self.canvas.bind("<Button-2>", self.mousebutton_middle)
        self.canvas.bind("<Button-3>", self.mousebutton_right)
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.c_tiles = []      # type: List[str]
        self.tile_images = []  # type: List[tkinter.PhotoImage]
        self.canvas_tag_to_tilexy = {}      # type: Dict[int, Tuple[int, int]]
        self.c64colors = False
        self.create_tile_images(Palette())
        self.wipe(False)
        self.create_canvas_playfield(self.playfield_columns, self.playfield_rows)
        w, h = tiles.tile2pixels(self.playfield_columns, self.playfield_rows)
        self.canvas.configure(scrollregion=(0, 0, w * 2, h * 2))
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.populate_imageselector()
        self.randomize_initial_values = None   # type: Tuple

    def init_new_cave(self, only_steel_border=False):
        if not only_steel_border:
            self.cave = Cave(0, self.cavename_var.get(), self.cavedescr_var.get(), self.playfield_columns, self.playfield_rows)
            self.cave.init_for_editor(self)
        steel = (objects.STEEL, Direction.NOWHERE)
        self.cave.horiz_line(0, 0, self.playfield_columns, steel)
        self.cave.horiz_line(0, self.playfield_rows - 1, self.playfield_columns, steel)
        self.cave.vert_line(0, 1, self.playfield_rows - 2, steel)
        self.cave.vert_line(self.playfield_columns - 1, 1, self.playfield_rows - 2, steel)
        if not only_steel_border:
            self.flood_fill(2, 2, (objects.DIRT, Direction.NOWHERE))

    def populate_imageselector(self):
        rows = []
        for obj, displaytile in sorted(EDITOR_OBJECTS.items(), key=lambda t: t[0].name):
            rows.append((self.tile_images_small[displaytile], obj.name.title()))
        self.imageselector.populate(rows)

    def destroy(self) -> None:
        super().destroy()

    def keypress(self, event) -> None:
        if event.char == 'f':
            current = self.canvas.find_withtag(tkinter.CURRENT)
            if current:
                tx, ty = self.canvas_tag_to_tilexy[current[0]]
                self.flood_fill(tx, ty, (self.imageselector.selected_object, Direction.NOWHERE))
        elif event.char == 'r':
            obj, direction = self.imageselector.selected_object, Direction.NOWHERE
            for _ in range(10):
                x = random.randrange(1, self.cave.width - 1)
                y = random.randrange(1, self.cave.height - 1)
                self.cave[x, y] = (obj, direction)
        elif event.char == 's':
            self.snapshot()
        elif event.char == 'u':
            self.restore()

    def keyrelease(self, event) -> None:
        pass

    def mousebutton_left(self, event) -> None:
        self.canvas.focus_set()
        current = self.canvas.find_withtag(tkinter.CURRENT)
        if current:
            if self.imageselector.selected_object:
                x, y = self.canvas_tag_to_tilexy[current[0]]
                self.cave[x, y] = (self.imageselector.selected_object, Direction.NOWHERE)

    def mousebutton_middle(self, event) -> None:
        pass

    def mousebutton_right(self, event) -> None:
        current = self.canvas.find_withtag(tkinter.CURRENT)
        if current:
            x, y = self.canvas_tag_to_tilexy[current[0]]
            self.cave[x, y] = (self.imageselector.selected_erase_object, Direction.NOWHERE)

    def mouse_motion(self, event) -> None:
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        current = self.canvas.find_closest(cx, cy)
        if current:
            x, y = self.canvas_tag_to_tilexy[current[0]]
            if event.state & 0x100:
                # left mouse button drag
                self.cave[x, y] = (self.imageselector.selected_object, Direction.NOWHERE)
            elif event.state & 0x600:
                # right / middle mouse button drag
                self.cave[x, y] = (self.imageselector.selected_erase_object, Direction.NOWHERE)

    def create_tile_images(self, colors: Palette) -> None:
        source_images = tiles.load_sprites(self.c64colors, colors, scale=2)
        self.tile_images = [tkinter.PhotoImage(data=image) for image in source_images]
        source_images = tiles.load_sprites(self.c64colors, colors, scale=1)
        self.tile_images_small = [tkinter.PhotoImage(data=image) for image in source_images]

    def create_canvas_playfield(self, width: int, height: int) -> None:
        # create the images on the canvas for all tiles (fixed position)
        if width < 4 or width > 200 or height < 4 or height > 200:
            raise ValueError("invalid playfield/cave width or height")
        self.playfield_columns = width
        self.playfield_rows = height
        self.canvas.delete(tkinter.ALL)
        self.c_tiles.clear()
        self.canvas_tag_to_tilexy.clear()
        selected_tile = EDITOR_OBJECTS[self.imageselector.selected_object]
        for y in range(self.playfield_rows):
            for x in range(self.playfield_columns):
                sx, sy = tiles.tile2pixels(x, y)
                obj, direction = self.cave[x, y]
                tile = self.canvas.create_image(sx * 2, sy * 2, image=self.tile_images[EDITOR_OBJECTS[obj]],
                                                activeimage=self.tile_images[selected_tile],
                                                anchor=tkinter.NW, tags="tile")
                self.c_tiles.append(tile)
                self.canvas_tag_to_tilexy[tile] = (x, y)

    def tile_selection_changed(self, object: GameObject, tile: int) -> None:
        image = self.tile_images[tile]
        for c_tile in self.c_tiles:
            self.canvas.itemconfigure(c_tile, activeimage=image)

    def tile_erase_selection_changed(self, object: GameObject, tile: int) -> None:
        pass

    def set_canvas_tile(self, x: int, y: int, tile: int) -> None:
        c_tile = self.canvas.find_closest(x * 32, y * 32)
        self.canvas.itemconfigure(c_tile, image=self.tile_images[tile])

    def flood_fill(self, x: int, y: int, thing: Tuple[GameObject, Direction]) -> None:
        target = self.cave[x, y][0]
        if target == thing[0]:
            return

        def flood(x, y):
            t = self.cave[x, y][0]
            if t != target:
                return
            self.cave[x, y] = thing
            flood(x - 1, y)
            flood(x + 1, y)
            flood(x, y - 1)
            flood(x, y + 1)

        flood(x, y)

    def snapshot(self) -> None:
        self.cave.snapshot()

    def restore(self) -> None:
        self.cave.restore()

    def wipe(self, confirm=True) -> None:
        if confirm and not tkinter.messagebox.askokcancel("Confirm", "Wipe cave?", parent=self.buttonsframe):
            return
        self.init_new_cave()
        self.snapshot()

    def randomize(self) -> None:
        RandomizeDialog(self.buttonsframe, "Randomize Cave", self, self.randomize_initial_values)

    def palette_edit(self) -> None:
        original_palette = self.cave.colors.copy()
        palette = PaletteDialog(self.buttonsframe, "Edit Palette", self, self.cave.colors).result
        if palette:
            self.cave.colors = palette
        else:
            self.cave.colors = original_palette
            self.apply_new_palette(original_palette)

    def do_random_fill(self, rseed: int, randomprobs: Tuple[int, int, int, int], randomobjs: Tuple[str, str, str, str]) -> None:
        editor_objects_by_name = {obj.name.lower(): obj for obj in EDITOR_OBJECTS}
        randomseeds = [0, rseed]
        for y in range(1, self.playfield_rows - 1):
            for x in range(0, self.playfield_columns):
                objname = objects.DIRT.name.lower()
                C64Cave.bdrandom(randomseeds)
                for randomobj, randomprob in zip(randomobjs, randomprobs):
                    if randomseeds[0] < randomprob:
                        objname = randomobj.lower()
                self.cave[x, y] = (editor_objects_by_name[objname], Direction.NOWHERE)
        self.init_new_cave(only_steel_border=True)
        self.randomize_initial_values = (rseed, randomprobs, randomobjs)

    def c64_colors_switched(self, switch: bool) -> None:
        self.c64random_button.configure(state=tkinter.NORMAL if switch else tkinter.DISABLED)
        self.c64colors = bool(switch)
        self.create_tile_images(self.cave.colors)
        self.populate_imageselector()
        self.create_canvas_playfield(self.playfield_columns, self.playfield_rows)

    def c64_colors_randomize(self) -> None:
        if self.c64colors:
            self.cave.colors.randomize()
            self.apply_new_palette(self.cave.colors)

    def apply_new_palette(self, colors: Palette) -> None:
        if self.c64colors:
            self.create_tile_images(colors)
            self.populate_imageselector()
            self.create_canvas_playfield(self.playfield_columns, self.playfield_rows)
            self.canvas.configure(background="#{:06x}".format(colors.rgb_border))

    def load(self):
        if not tkinter.messagebox.askokcancel("Confirm", "Load cave and lose current one?", parent=self.buttonsframe):
            return
        gamefile = tkinter.filedialog.askopenfilename(title="Load caveset file", defaultextension=".bdcff",
                                                      filetypes=[("boulderdash", ".bdcff"),
                                                                 ("boulderdash", ".bd"),
                                                                 ("text", ".txt")],
                                                      parent=self.buttonsframe)
        caveset = CaveSet(gamefile, caveclass=Cave)
        if caveset.num_caves > 1:
            cavenum = CaveSelectionDialog(self.buttonsframe, caveset.cave_names(), self).result
            if cavenum is None:
                return
        else:
            cavenum = 1
        cave = caveset.cave(cavenum)
        cave.init_for_editor(self)
        self.cave = cave
        self.set_cave_properties(self.cave)
        self.c64_colors_switched(self.c64colors)  # make sure tiles are redrawn

    def set_cave_properties(self, cave: Cave) -> None:
        self.cavename_var.set(cave.name)
        self.cavedescr_var.set(cave.description)
        self.cavesetauthor_var.set(cave.author or getpass.getuser())
        self.cavesetdate_var.set(cave.date or str(datetime.datetime.now().date()))
        self.cavesetwww_var.set(cave.www)
        self.cavediamondsrequired_var.set(cave.diamonds_required)
        self.cavediamondvaluenorm_var.set(cave.diamondvalue_normal)
        self.cavediamondvalueextra_var.set(cave.diamondvalue_extra)
        self.caveamoebafactor_var.set(cave.amoebafactor)
        self.caveamoebatime_var.set(cave.amoeba_slowgrowthtime)
        self.cavemagicwalltime_var.set(cave.magicwall_millingtime)
        self.caveintermission_var.set(cave.intermission)
        self.cavetimelimit_var.set(cave.time)
        self.caveslimepermeability_var.set(cave.slime_permeability)
        self.caveintermission_var.set(cave.intermission)

    def save(self, gamefile: Optional[str]=None) -> bool:
        if not self.sanitycheck():
            return False
        caveset = bdcff.BdcffParser()
        caveset.num_caves = 1
        caveset.name = "playtest caveset"
        caveset.author = self.cavesetauthor_var.get()
        caveset.www = self.cavesetwww_var.get()
        caveset.date = self.cavesetdate_var.get()
        caveset.description = "for playtesting the cave"
        cave = bdcff.BdcffCave()
        cave.name = self.cavename_var.get()
        cave.description = self.cavedescr_var.get()
        cave.width = self.cave.width
        cave.height = self.cave.height
        cave.cavetime = self.cavetimelimit_var.get()
        cave.diamonds_required = self.cavediamondsrequired_var.get()
        cave.diamondvalue_normal = self.cavediamondvaluenorm_var.get()
        cave.diamondvalue_extra = self.cavediamondvalueextra_var.get()
        cave.amoebatime = self.caveamoebatime_var.get()
        cave.amoebafactor = self.caveamoebafactor_var.get()
        cave.magicwalltime = self.cavemagicwalltime_var.get()
        cave.slimepermeability = self.caveslimepermeability_var.get()
        cave.intermission = self.caveintermission_var.get()
        cave.cavedelay = 3 if cave.intermission else 8
        c = self.cave.colors
        cave.color_border, cave.color_screen, cave.color_fg1, cave.color_fg2, cave.color_fg3, cave.color_amoeba, cave.color_slime = \
            c.border, c.screen, c.fg1, c.fg2, c.fg3, c.amoeba, c.slime
        BDCFFSYMBOL = {(obj, direction): symbol for symbol, (obj, direction) in BDCFFOBJECTS.items()}
        for y in range(0, self.cave.height):
            mapline = ""
            for x in range(0, self.cave.width):
                obj, direction = self.cave[x, y]
                mapline += BDCFFSYMBOL[obj, direction]
            cave.map.maplines.append(mapline)
        caveset.caves.append(cave)
        gamefile = gamefile or tkinter.filedialog.asksaveasfilename(title="Save single cave as", defaultextension=".bdcff",
                                                                    filetypes=[("boulderdash", ".bdcff"),
                                                                               ("boulderdash", ".bd"),
                                                                               ("text", ".txt")],
                                                                    parent=self.buttonsframe)
        if gamefile:
            with open(gamefile, "wt") as out:
                caveset.write(out)
            return True
        return False

    def sanitycheck(self):
        # check that the level is sane:
        # edge must be all steel wall, or inbox/outbox.
        # we should have at least 1 inbox and at least 1 outbox.
        inbox_count = len([x for x, _ in self.cave.map if x == objects.INBOXBLINKING])
        outbox_count = len([x for x, _ in self.cave.map if x in (objects.OUTBOXCLOSED, objects.OUTBOXBLINKING)])
        enclosed_ok = True
        edge_objs_allowed = {objects.STEEL, objects.INBOXBLINKING, objects.OUTBOXBLINKING, objects.OUTBOXCLOSED}
        for x in range(0, self.cave.width):
            enclosed_ok &= self.cave[x, 0][0] in edge_objs_allowed
            enclosed_ok &= self.cave[x, self.cave.height - 1][0] in edge_objs_allowed
        for y in range(0, self.cave.height):
            enclosed_ok &= self.cave[0, y][0] in edge_objs_allowed
            enclosed_ok &= self.cave[self.cave.width - 1, y][0] in edge_objs_allowed
        messages = []
        if inbox_count <= 0:
            messages.append("There should be at least one INBOX.")
        if outbox_count <= 0:
            messages.append("There should be at least one OUTBOX.")
        if not enclosed_ok:
            messages.append("The edge of the level should be STEEL (or INBOX or OUTBOX).")
        if messages:
            messages.insert(0, "There are some problems with the current cave:")
            tkinter.messagebox.showerror("Cave sanity check failed", "\n\n".join(messages), parent=self.buttonsframe)
            return False
        return True

    def playtest(self) -> None:
        print("\n\nPLAYTESTING: saving temporary cave file...")
        gamefile = os.path.expanduser("~/.bouldercaves/_playtest_cave.bdcff")
        if self.save(gamefile):
            # launch the game in a separate process
            import subprocess
            from . import game
            env = os.environ.copy()
            env["PYTHONPATH"] = sys.path[0]
            parameters = [sys.executable, "-m", game.__name__, "--synth", "--playtest", "--game", gamefile]
            if self.c64colors_var.get():
                parameters.append("--c64colors")
            print("PLAYTESTING: launching game in playtest mode...\n")
            subprocess.Popen(parameters, env=env)

    def set_defaults(self) -> None:
        if not tkinter.messagebox.askokcancel("Confirm", "Set all cave parameters to defaults?", parent=self.buttonsframe):
            return
        self.set_cave_properties(Cave(0, "Test.", "A test cave.", self.visible_columns, self.visible_rows))


class RandomizeDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, title: str, editor: EditorWindow, initial_values: Tuple) -> None:
        self.editor = editor
        self.initial_values = initial_values
        super().__init__(parent=parent, title=title)

    def body(self, master: tkinter.Widget) -> tkinter.Widget:
        if not self.initial_values:
            self.initial_values = (199, (100, 60, 25, 15),
                                   (objects.EMPTY.name, objects.BOULDER.name, objects.DIAMOND.name, objects.FIREFLY.name))
        self.rseed_var = tkinter.IntVar(value=self.initial_values[0])
        self.rp1_var = tkinter.IntVar(value=self.initial_values[1][0])
        self.rp2_var = tkinter.IntVar(value=self.initial_values[1][1])
        self.rp3_var = tkinter.IntVar(value=self.initial_values[1][2])
        self.rp4_var = tkinter.IntVar(value=self.initial_values[1][3])
        self.robj1_var = tkinter.StringVar(value=self.initial_values[2][0].title())
        self.robj2_var = tkinter.StringVar(value=self.initial_values[2][1].title())
        self.robj3_var = tkinter.StringVar(value=self.initial_values[2][2].title())
        self.robj4_var = tkinter.StringVar(value=self.initial_values[2][3].title())
        tkinter.Label(master, text="Fill the cave with randomized stuff, using the C-64 BD randomizer.\n").pack()
        f = tkinter.Frame(master)
        tkinter.Label(f, text="Random seed (0-255): ").grid(row=0, column=0)
        tkinter.Label(f, text="Random probability (0-255): ").grid(row=1, column=0)
        tkinter.Label(f, text="Random probability (0-255): ").grid(row=2, column=0)
        tkinter.Label(f, text="Random probability (0-255): ").grid(row=3, column=0)
        tkinter.Label(f, text="Random probability (0-255): ").grid(row=4, column=0)
        rseed = tkinter.Entry(f, textvariable=self.rseed_var, width=4, font="monospace")
        rp1 = tkinter.Entry(f, textvariable=self.rp1_var, width=4, font="monospace")
        rp2 = tkinter.Entry(f, textvariable=self.rp2_var, width=4, font="monospace")
        rp3 = tkinter.Entry(f, textvariable=self.rp3_var, width=4, font="monospace")
        rp4 = tkinter.Entry(f, textvariable=self.rp4_var, width=4, font="monospace")
        rseed.grid(row=0, column=1)
        rp1.grid(row=1, column=1)
        rp2.grid(row=2, column=1)
        rp3.grid(row=3, column=1)
        rp4.grid(row=4, column=1)
        options = sorted([obj.name.title() for obj in EDITOR_OBJECTS])
        tkinter.OptionMenu(f, self.robj1_var, *options).grid(row=1, column=2, stick=tkinter.W)
        tkinter.OptionMenu(f, self.robj2_var, *options).grid(row=2, column=2, stick=tkinter.W)
        tkinter.OptionMenu(f, self.robj3_var, *options).grid(row=3, column=2, stick=tkinter.W)
        tkinter.OptionMenu(f, self.robj4_var, *options).grid(row=4, column=2, stick=tkinter.W)
        f.pack()
        tkinter.Label(master, text="\n\nWARNING: DOING THIS WILL WIPE THE CURRENT CAVE!").pack()
        return rp1

    def validate(self) -> bool:
        try:
            vs = self.rseed_var.get()
            v1 = self.rp1_var.get()
            v2 = self.rp1_var.get()
            v3 = self.rp1_var.get()
            v4 = self.rp1_var.get()
        except tkinter.TclError as x:
            tkinter.messagebox.showerror("Invalid entry", str(x), parent=self)
            return False
        else:
            if not (0 <= vs <= 255) or not (0 <= v1 <= 255) or not(0 <= v2 <= 255) or not(0 <= v3 <= 255) or not(0 <= v4 <= 255):
                tkinter.messagebox.showerror("Invalid entry", "One or more of the values is invalid.", parent=self)
                return False
        return True

    def apply(self) -> None:
        vs = self.rseed_var.get()
        v1 = self.rp1_var.get()
        v2 = self.rp2_var.get()
        v3 = self.rp3_var.get()
        v4 = self.rp4_var.get()
        o1 = self.robj1_var.get()
        o2 = self.robj2_var.get()
        o3 = self.robj3_var.get()
        o4 = self.robj4_var.get()
        self.editor.do_random_fill(vs, (v1, v2, v3, v4), (o1, o2, o3, o4))


class PaletteDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, title: str, editor: EditorWindow, colors: Palette) -> None:
        self.editor = editor
        self.colors = colors
        self.result = None  # type: Palette
        self.palettergbbuttons = {}   # type: Dict[str, tkinter.Button]
        self.color_vars = {}   # type: Dict[str, tkinter.Variable]
        super().__init__(parent=parent, title=title)

    def body(self, master: tkinter.Widget) -> Optional[tkinter.Widget]:
        colors = [("fg1", self.colors.fg1), ("fg2", self.colors.fg2), ("fg3", self.colors.fg3),
                  ("amoeba", self.colors.amoeba), ("slime", self.colors.slime),
                  ("screen", self.colors.screen), ("border", self.colors.border)]
        for colornum, (name, value) in enumerate(colors):
            color_var = tkinter.StringVar(value=value)
            self.color_vars[name] = color_var
            tkinter.Label(master, text="{:s} color: ".format(name.title())).grid(row=colornum, sticky=tkinter.E)
            rf = tkinter.Frame(master)
            for num, color in enumerate(colorpalette):
                tkcolor = "#{:06x}".format(color)
                rb = tkinter.Radiobutton(rf, variable=color_var, indicatoron=False, value=num,
                                         activebackground=tkcolor, command=lambda n=name: self.palette_color_chosen(n),
                                         offrelief=tkinter.FLAT, relief=tkinter.FLAT, overrelief=tkinter.RIDGE,
                                         bd=5, bg=tkcolor, selectcolor=tkcolor, width=2, height=1)
                rb.pack(side=tkinter.LEFT)
                if num == value:
                    rb.select()
            rf.grid(row=colornum, column=1, pady=4, sticky=tkinter.W)
            tkinter.Label(master, text="RGB:").grid(row=colornum, column=2)
            rgbb = tkinter.Button(master, text="rgb", command=lambda n=name: self.rgb_color_chosen(n))
            rgbb.grid(row=colornum, column=3)
            if type(value) is str:
                fgtkcolor = "#{:06x}".format(0xffffff ^ int(value[1:], 16))
                rgbb.configure(text="RGB", bg=value, fg=fgtkcolor)
            self.palettergbbuttons[name] = rgbb
        return None

    def palette_color_chosen(self, colorname: str) -> None:
        # reset the rgb button of this color row
        dummybutton = tkinter.Button(self)
        self.palettergbbuttons[colorname].configure(text="rgb", bg=dummybutton.cget("bg"), fg=dummybutton.cget("fg"))
        self.editor.apply_new_palette(self.palette)

    def rgb_color_chosen(self, colorname: str) -> None:
        color = self.color_vars[colorname].get()
        if not color.startswith("#"):
            color = "#{:06x}".format(colorpalette[int(color)])
        rgbcolor = tkinter.colorchooser.askcolor(title="Choose a RGB color", parent=self, initialcolor=color)
        if rgbcolor[1] is not None:
            tkcolor = rgbcolor[1]
            fgtkcolor = "#{:06x}".format(0xffffff ^ int(tkcolor[1:], 16))
            self.color_vars[colorname].set(tkcolor)
            self.palettergbbuttons[colorname].configure(text="RGB", bg=tkcolor, fg=fgtkcolor)
            self.editor.apply_new_palette(self.palette)

    def apply(self) -> None:
        self.result = self.palette

    @property
    def palette(self) -> Palette:
        return Palette(self.color_vars["fg1"].get(),
                       self.color_vars["fg2"].get(),
                       self.color_vars["fg3"].get(),
                       self.color_vars["amoeba"].get(),
                       self.color_vars["slime"].get(),
                       self.color_vars["screen"].get(),
                       self.color_vars["border"].get())


class CaveSelectionDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, cavenames: List[str], editor: EditorWindow) -> None:
        self.editor = editor
        self.cavenames = cavenames
        self.result = None
        super().__init__(parent=parent, title="Select the cave to load")

    def body(self, master: tkinter.Widget) -> tkinter.Widget:
        tkinter.Label(master, text="Currently you can only edit a single cave.\nThe selected file contains multiple caves:").pack()
        f = tkinter.Frame(master)
        self.lb = tkinter.Listbox(f, bd=1, font="monospace", height=min(25, len(self.cavenames)),
                                  width=max(10, max(len(name) for name in self.cavenames)))
        for name in self.cavenames:
            self.lb.insert(tkinter.END, name)
        sy = tkinter.Scrollbar(f, orient=tkinter.VERTICAL, command=self.lb.yview)
        self.lb.configure(yscrollcommand=sy.set)
        self.lb.pack(side=tkinter.LEFT)
        sy.pack(side=tkinter.RIGHT, expand=1, fill=tkinter.Y)
        f.pack(pady=8)
        tkinter.Label(master, text="Select the single cave to load from this caveset file.").pack()
        return self.lb

    def apply(self) -> None:
        selection = self.lb.curselection()
        self.result = (selection[0] + 1) if selection else None


def start() -> None:
    window = EditorWindow()
    window.mainloop()


if __name__ == "__main__":
    start()
