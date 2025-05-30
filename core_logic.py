"""
This module contains all functions that implement the core logic of the application when the main button is pressed:
forming a SQL query, executing the query, retrieving the list of lands, processing the list to display in the widget,
and updating the widget.
"""

from typing import List, Tuple


def form_query(colors: list, power: str, utility: int) -> str:
    """
    Forms a SQL query using outer parameters.
    :param colors: List of Commander colors.
    :param power: Status of option radiobutton.
    :param utility: Status of check button.
    :return: SQL query string.
    """

    def allow_forbid(colors: list, _isallowed: bool) -> str:
        """
        Adds to (removes from) the selection the lands with colors that are (not) in the Commander combination.
        :param colors: List of colors from Commander instance attribute.
        :param _isallowed: Bool value instructing whether to allow or forbid inclusion of lands depending on colors.
        :return: String with additional query condition.
        """
        processed_colors = set(colors) if _isallowed else set('WUBRG') - set(colors)  # Colors to include or exclude
        criterion = '= 1' if _isallowed else '= 0'

        color_conditions = []
        for color in processed_colors:
            color_conditions.append(f"{color} {criterion}")
#       print(color_conditions)

        if _isallowed:
            return f"({' OR '.join(color_conditions)} OR Type = 'Anyland')"
        else:
            return f" AND ({' AND '.join(color_conditions)})" if color_conditions else ""    # else for 5-color decks

    def _is_fetchland(colors: list) -> str:
        """
        Allows Fetchlands to be selected if they produce at least one allowed color, regardless of forbidden colors.
        :param colors: List of colors from Commander instance attribute.
        :return: String with additional query condition.
        """
        return f" OR (Type = 'Fetch' AND {allow_forbid(colors, _isallowed=True)})"

    def power_range(power: str) -> str:
        """
        Limits the land selection to those having the respective value in the Power field.
        :param power: String value from radiobutton status variable.
        :return: String with additional query condition.
        """
        power_levels = {
            "Starter": " AND Power LIKE '%1%'",
            "Collector": " AND Power LIKE '%2%'",
            "Elite": " AND Power LIKE '%3%'"}      # Error logic not added due to selection via GUI. May add later.
        return power_levels[power]

    def show_utility(utility: int) -> str:
        """
        Includes (by default) or excludes Utility lands from selection.
        :param utility: Integer value from check button status.
        :return: String with additional query condition.
        """
        return "" if utility == 1 else " AND Type != 'Utility'"

    def suit_deck(colors: list) -> str:
        """
        Refines the land selection with lands suitable to be played in decks with a certain number of colors.
        :param colors: List of colors from Commander instance attribute.
        :return: String with additional query condition.
        """
        return f" AND Suit LIKE '%{len(colors) - 1}%'"

    query = (f"SELECT Name, Type FROM MTG_lands WHERE "
             f"(({allow_forbid(colors, True)}"    # ...produces at least one allowed color or is colorless or produces any...
             f"{allow_forbid(colors, False)})"    # ...does not produce any forbidden color...
             f"{_is_fetchland(colors)})"    # ...forbidden rule does not apply to Fetchlands...
             f"{power_range(power)}"          # ...is played in deck of respective power level...
             f"{show_utility(utility)}"     # ...can be a Utility land
             f"{suit_deck(colors)}"
             f" ORDER BY Type")        # ...is suitable for decks with the given number of colors.
#   print(query)
    return query


def select_lands(query: str, cursor) -> List[Tuple]:
    """
    Executes the query and retrieves a list of appropriate lands.
    :param query: String with query from previous function.
    :param cursor: sqlite3 cursor object.
    :return: List of lands from SQL database.
    """
    cursor.execute(query)
    lands = cursor.fetchall()
    return lands


def process_lands(lands: List[Tuple]) -> str:
    output_text = "\n".join(land[0] for land in lands)                     # release
#   output_text = "\n".join(f"{land[0]} - {land[1]}" for land in lands)    # debugging
    return output_text
