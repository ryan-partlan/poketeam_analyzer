import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Pokedex import *
from Team import *
from Evaluator import *



pdex = Pokedex("pokedex.json")
team = Team()
# t.add_member("milotic")
# t.add_member("gastrodon")
# t.add_member("bastiodon")
# t.add_member("gyarados")
# t.add_member("leafeon")
# t.add_member("yanmega")
# t.show_team()
# def_mat = e.get_mat(mode="def")
# generate_heatmap(e, def_mat, "Defensive Matchups", "def_matchups2.png", "red")
# str_mat = e.get_mat(mode="str")
# generate_heatmap(e, str_mat, "Offensive Matchups", "off_matchups2.png", "green")
# print(p.get_av_vec())
# print(t.stat_mat())
# e.suggest_alts()


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Pokemon Team Analyser')

        # Full screen.
        # self.state('zoomed')
        self.evaluator = Evaluator(team, pdex, "type_chart.csv")
        # 3 rows x 2 columns grid.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)
        self.grid_rowconfigure(7, weight=0)
        self.grid_rowconfigure(8, weight=0)
        self.grid_rowconfigure(9, weight=0)
        self.grid_rowconfigure(10, weight=1)  # Image generation row
        self.grid_rowconfigure(11, weight=1)  # Image generation row
        self.grid_rowconfigure(12, weight=0)
        self.grid_rowconfigure(13, weight=0)
        self.grid_rowconfigure(14, weight=0)
        self.grid_rowconfigure(15, weight=0)
        self.grid_rowconfigure(16, weight=0)
        self.grid_rowconfigure(17, weight=0)
        self.grid_rowconfigure(18, weight=0)
        self.grid_rowconfigure(19, weight=0)
        self.grid_rowconfigure(20, weight=0)
        self.grid_rowconfigure(21, weight=0)
        self.alts_box_var = tk.StringVar()
        self.alts_box_var.set("Select Alt")
        # self.alts_box = tk.Entry(self)
        self.alts_box = tk.OptionMenu(self, self.alts_box_var, [])
        self.alts_box.grid(row=10, column=0, columnspan=3, sticky='wn')
        # self.team_frame = tk.Frame(self)
        # self.team_frame.grid(row=3, column=0, rowspan=6, columnspan=3, sticky='we')
        self.n_pokes = 0
        self.used_slots = set() # dict of where pokemon are placed in the team
        self.all_slots = {0, 1, 2, 3, 4, 5}
        self.ana_btn = None
        self.list_box()

    def list_box(self):
        # Put the filter in a frame at the top spanning across the columns.
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, columnspan=1, sticky='we')

        # Put the filter label and entry box in the frame.
        tk.Label(frame, text='Filter:').pack(side='left')

        self.filter_box = tk.Entry(frame)
        self.filter_box.pack(side='left', fill='x', expand=True)

        # A listbox with scrollbars.
        yscrollbar = tk.Scrollbar(self, orient='vertical')
        yscrollbar.grid(row=1, column=1, sticky='ns')

        xscrollbar = tk.Scrollbar(self, orient='horizontal')
        xscrollbar.grid(row=2, column=0, sticky='we')

        self.listbox = tk.Listbox(self, yscrollcommand=yscrollbar.set)

        self.listbox.grid(row=1, column=0, sticky='nswe')

        yscrollbar.config(command=self.listbox.yview)
        xscrollbar.config(command=self.listbox.xview)

        def lb_left_click(event):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.listbox.nearest(event.y))
            self.listbox.activate(self.listbox.nearest(event.y))
            selection = self.listbox.get(self.listbox.curselection())
            self.add_on_click(sel=selection)

        self.listbox.bind("<Button-1>", lb_left_click)

        # The current filter. Setting it to None initially forces the first update.
        self.curr_filter = None

        # All of the items for the listbox.
        self.items = pdex.all_names
        self.init_add_button()
        # The initial update.
        self.on_tick()

    def init_add_button(self):
        self.add_button = tk.Button(self, text="Add", command=self.add_on_click)
        self.add_button.grid(row=0, column=1)
        # self.add_button.pack()

    def on_tick(self):
        if self.filter_box.get() != self.curr_filter:
            # The contents of the filter box has changed.
            self.curr_filter = self.filter_box.get()
            # Refresh the listbox.
            self.listbox.delete(0, 'end')
            for item in self.items:
                if self.curr_filter in item:
                    self.listbox.insert('end', item)
        if self.n_pokes >= 6 and self.ana_btn == None:
            self.ana_btn = self.make_analyze_button()
            self.ana_btn.grid(row=10, column=1, sticky="ne")
        elif self.n_pokes < 6 and self.ana_btn != None:
            self.ana_btn.after(10, self.ana_btn.destroy())
            self.ana_btn = None
        self.after(250, self.on_tick)

    def swap_for_alt(self, pkmn, alt):
        pass ##TODO: CLICKABLE DROPDOWN FOR ALTS
    def add_on_click(self, sel=None):
        if sel:
            poke = team.add_member(sel)
        else:
            poke = team.add_member(self.curr_filter)
        if poke:
            avail_slots = self.all_slots - self.used_slots
            slot = avail_slots.pop()
            self.used_slots.add(slot)
            self.all_slots.remove(slot)
            slot = slot + 4
            pkmn = tk.Label(self, text=poke.name)
            pkmn.grid(row=slot, column=0)
            sug_btn = self.make_suggest_button(poke, slot)
            self.make_delete_button(pkmn, sug_btn, slot)

    def make_analyze_button(self):
        ana_btn = ttk.Button(self, text="Analyze", command=self.display_analysis)
        return ana_btn

    def make_delete_button(self, pkmn, sug_btn, slot):
        del_btn = ttk.Button(self, text='Delete')
        del_btn['command'] = self.remove_member(pkmn, del_btn, sug_btn, slot)
        del_btn.grid(row=slot, column=1, sticky="e")
        self.n_pokes += 1
    def make_suggest_button(self, pkmn, slot):
        sug_btn = ttk.Button(self, text='Suggest')
        sug_btn['command'] = self.suggest_alt(pkmn)
        sug_btn.grid(row=slot, column=2, sticky="w")
        return sug_btn

    def remove_member(self, pkmn, del_btn, sug_btn, slot):
        # Curried function that deletes the Pokemon and button itself
        def rmv():
            team.remove_member(pkmn.cget("text"))
            # pkmn.after(10, pkmn.destroy())
            # del_btn.after(10, del_btn.destroy())
            pkmn.destroy()
            del_btn.destroy()
            sug_btn.destroy()
            self.used_slots.remove(slot - 4)
            self.all_slots.add(slot - 4)
            self.all_slots
            self.n_pokes -= 1
        return rmv
    def suggest_alt(self, pkmn):
        def alt():
            alt_list = self.evaluator.suggest_alt(pkmn)
            self.display_alts(alt_list)
        return alt
    # def display_alts(self, alts_list):
    #     self.alts_box.delete(0, "end")
    #     str_alts = ", ".join([alt.name for alt in alts_list])
    #     self.alts_box.insert(0, str_alts)
    def display_alts(self, alts_list):
        str_alts = [alt.name for alt in alts_list]
        self.alts_box_var.set("Alts found")
        self.alts_box["menu"].delete(0, "end")
        for item in str_alts:
            self.alts_box["menu"].add_command(
                label=item
            )

    def display_analysis(self):
        self.analysis_frame = tk.Frame(self, background="black", padx=5, pady=5)
        self.analysis_title = tk.Label(self, text="Analysis", font="Helvetica 15")
        self.analysis_title.grid(row=0, column=3)
        self.analysis_frame.grid(row=1, column=3, rowspan=20)
        def_mat = self.evaluator.get_mat(mode="def")
        generate_heatmap(self.evaluator, def_mat, "Defensive Matchups", "def_matchups.png", "red")
        str_mat = self.evaluator.get_mat(mode="str")
        generate_heatmap(self.evaluator, str_mat, "Offensive Matchups", "off_matchups.png", "green")
        stat_mat = team.stat_mat()
        generate_heatmap(self.evaluator, stat_mat, "Stats", "stat_mat.png", "blue")
        self.show_graphic("def_matchups.png", (1, 3), rowspan=4)
        self.show_graphic("off_matchups.png", (6, 3), rowspan=4)
        self.show_graphic("stat_mat.png", (11, 3), rowspan=4)

    def show_graphic(self, path, coords, rowspan=5):
        row, column = coords
        image = Image.open(path)
        display = ImageTk.PhotoImage(image)
        label = tk.Label(self.analysis_frame, image=display)
        label.image = display
        label.grid(row=row, column=column, rowspan=rowspan, sticky="ew")


Gui().mainloop()

