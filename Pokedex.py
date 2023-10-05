import json
from Pokemon import *


class Pokedex:
    def __init__(self, src):
        self.src = src
        self.generation = 7
        self.dex_data = self.get_data()
        self.all_names = [pkmn.name for pkmn in self.dex_data]

    def get_data(self):
        pdex = []
        with open(self.src, encoding="utf8") as f:
            json_file = json.load(f)
            for pkmn_data in json_file:
                pdex.append(Pokemon(pkmn_data))
        return pdex

    def get_pkmn(self, name):
        name = name.lower().title()  # Format to match name queries
        for pkmn in self.dex_data:
            if pkmn.name == name:
                return pkmn, True
        return False, False

    def get_av_stat(self, stat):
        return sum(
            [
                float(pkmn.dex_info["base"][stat])
                for pkmn in self.dex_data
                if "base" in pkmn.dex_info.keys()
            ]
        ) / len(self.dex_data)

    def get_av_vec(self):
        stat_list = ["HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]
        return [self.get_av_stat(stat) for stat in stat_list]
