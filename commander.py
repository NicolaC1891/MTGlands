"""
The module contains the Commander class to store and update the color combination.
"""


class Commander:
    """
    The class to determine color combinations, store and update the current combination.

    Attributes:
         colors (str): Current deck colors, updated upon each action with mana button.
         combination(str): Color combination name by key from combinations dict.
    """

    combinations = {
        "C": "COLORLESS",
        "CW": "MONOWHITE",
        "CU": "MONOBLUE",
        "BC": "MONOBLACK",
        "CR": "MONORED",
        "CG": "MONOGREEN",
        "CUW": "AZORIUS",
        "CRW": "BOROS",
        "BCU": "DIMIR",
        "BCG": "GOLGARI",
        "CGR": "GRUUL",
        "CRU": "IZZET",
        "BCW": "ORZHOV",
        "BCR": "RAKDOS",
        "CGW": "SELESNYA",
        "CGU": "SIMIC",
        "BCGW": "ABZAN",
        "CGUW": "BANT",
        "BCUW": "ESPER",
        "BCRU": "GRIXIS",
        "CRUW": "JESKAI",
        "BCGR": "JUND",
        "BCRW": "MARDU",
        "CGRW": "NAYA",
        "BCGU": "SULTAI",
        "CGRU": "TEMUR",
        "BCGRU": "SANS-WHITE (GLINT)",
        "BCGRW": "SANS-BLUE (DUNE)",
        "CGRUW": "SANS-BLACK (INK)",
        "BCGUW": "SANS-RED (WITCH)",
        "BCRUW": "SANS-GREEN (YORE)",
        "BCGRUW": "FIVE COLORS",
    }

    def __init__(self):
        """
        Initializes with starting color (C = colorless)
        """
        self.colors = ["C"]
        self.combination = "COLORLESS"

    def update(self) -> None:
        """
        Updates the current color combination of Commander instance.
        :return: None. Updates own color combination attribute from own colors attribute.
        """
        cur_colors = sorted(self.colors)
        self.combination = self.combinations.get("".join(cur_colors), "unknown")
