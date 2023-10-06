import numpy as np

from Pokedex import *

pdex = Pokedex("pokedex.json")
TYPE_MAPPING = {
    "Normal": 0,
    "Fire": 1,
    "Water": 2,
    "Electric": 3,
    "Grass": 4,
    "Ice": 5,
    "Fighting": 6,
    "Poison": 7,
    "Ground": 8,
    "Flying": 9,
    "Psychic": 10,
    "Bug": 11,
    "Rock": 12,
    "Ghost": 13,
    "Dragon": 14,
    "Dark": 15,
    "Steel": 16,
    "Fairy": 17,
}


class Team:
    def __init__(self):
        self.members = []

    def add_member(self, name):
        if len(self.members) >= 6:
            # print("Team is full!")
            return None
        else:
            pkmn, retrieved = pdex.get_pkmn(name)
            if retrieved:
                self.members.append(pkmn)
            return pkmn

    def remove_member(self, name):
        name = name.lower()
        for pkmn in self.members:
            pokemon_name = pkmn.name.lower()
            if pokemon_name == name:
                self.members.remove(pkmn)
                return

    def clear_team(self):
        self.members = []

    def show_team(self):
        for pkmn in self.members:
            print(pkmn.name, pkmn.types)

    def stat_mat(self):
        return np.vstack([pkmn.stat_vec for pkmn in self.members])

    def hp_vec(self):
        return [pkmn.hp for pkmn in self.members]

    def atk_vec(self):
        return [pkmn.atk for pkmn in self.members]

    def def_vec(self):
        return [pkmn.df for pkmn in self.members]

    def spatk_vec(self):
        return [pkmn.spatk for pkmn in self.members]

    def spdef_vec(self):
        return [pkmn.spdef for pkmn in self.members]

    def spe_vec(self):
        return [pkmn.speed for pkmn in self.members]

    def mem_names(self):
        return [pkmn.name for pkmn in self.members]
