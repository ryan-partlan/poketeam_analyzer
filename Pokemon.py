import numpy as np


class Pokemon:
    def __init__(self, dex_info):
        self.dex_info = dex_info
        self.name = dex_info["name"]["english"]
        self.types = dex_info["type"]
        if "base" in self.dex_info.keys():
            self.stat_vec = self.get_stat_vec()
        else:
            self.stat_vec = np.zeros(6)
        self.hp, self.atk, self.df, self.spatk, self.spdef, self.speed = self.stat_vec
        self.stat_total = sum(self.stat_vec)

    def get_stat_vec(self):
        hp = float(self.dex_info["base"]["HP"])
        atk = float(self.dex_info["base"]["Attack"])
        df = float(self.dex_info["base"]["Defense"])
        spatk = float(self.dex_info["base"]["Sp. Attack"])
        spdef = float(self.dex_info["base"]["Sp. Defense"])
        speed = float(self.dex_info["base"]["Speed"])
        return np.array([hp, atk, df, spatk, spdef, speed])
