import csv
from Pokedex import *
import numpy as np
from Heatmap import *
from Team import *


class Evaluator:
    def __init__(self, team, pdex, src_chart):
        self.pdex = pdex
        self.src_chart = src_chart
        self.strype_chart = np.array(self.get_chart())
        self.defype_chart = self.strype_chart.T
        self.type_map = {
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
        self.team = team

    def get_chart(self):
        with open(self.src_chart) as f:
            csv_file = list(csv.reader(f))[1:]
            chart = [[float(el) for el in row[1:]] for row in csv_file]
            return chart

    def get_vec(self, pkmn, type_chart):
        types = pkmn.types
        str_vec = np.array([])
        for typ in types:
            type_index = self.type_map[typ]
            if len(str_vec) == 0:
                str_vec = type_chart[type_index]
            elif len(str_vec) != 0:
                str_vec = str_vec * type_chart[type_index]
        return str_vec

    def get_mat(self, mode="str"):  # mode in {str, def}
        mat = []
        type_chart = np.array(self.get_chart())
        if mode == "def":
            type_chart = type_chart.T
        for pkmn in self.team.members:
            mat.append(self.get_vec(pkmn, type_chart))
        return np.vstack(mat)

    def suggest_alts(self):
        for pkmn in self.team.members:
            self.suggest_alt(pkmn)

    def suggest_alt(self, poke):
        for pkmn in self.pdex.dex_data:
            if (
                all(poke.stat_vec < pkmn.stat_vec)
                and poke.types == pkmn.types
                and poke.name != pkmn.name
            ):
                print(f"{pkmn.name} has better stats and the same typing as {poke.name}.")


# if __name__ == "__main__":
#     p = Pokedex("pokedex.json")
#     t.add_member("milotic")
#     t.add_member("gastrodon")
#     t.add_member("bastiodon")
#     t.add_member("gyarados")
#     t.add_member("leafeon")
#     t.add_member("yanmega")
#     t.show_team()
#     e = Evaluator(t, p, "type_chart.csv")
#     def_mat = e.get_mat(mode="def")
#     generate_heatmap(e, def_mat, "Defensive Matchups", "def_matchups2.png", "red")
#     str_mat = e.get_mat(mode="str")
#     generate_heatmap(e, str_mat, "Offensive Matchups", "off_matchups2.png", "green")
#     print(p.get_av_vec())
#     print(t.stat_mat())
#     e.suggest_alts()
