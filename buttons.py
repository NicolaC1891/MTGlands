"""
This module contains classes to create all GUI buttons.
"""

import tkinter as tk  # To use regular tkinter styles
import core_logic as cl
import filesave as fs
from layout import *


class ManaButton:
    """
    The class to create a mana symbol toggle button that updates Commander color combination when pressed.

    Attributes:
        location (Frame): Tkinter frame to hold all mana buttons.
        image_on (PhotoImage): Button image in ON position.
        image_off (PhotoImage): Button image in OFF position.
        manacolor (str): Mana symbol added to Commander color combination.
        button_toggle (IntVar): Tkinter variable to store current button status.
        button(Button): ttk button with toggle command.
    """

    def __init__(
        self, location: Frame, image_on, image_off, manacolor: str, commander: Commander, deck_label: DeckLabel
    ):
        """
        Initializes the ManaButton with frame, images, mana color, button variable, and button itself.
        :param location: Tkinter frame to hold all mana buttons
        :param image_on: Button image in ON position.
        :param image_off: Button image in OFF position.
        :param manacolor: Mana symbol (from WUBRGC) to add to Commander color combination.
        :param commander: Commander class instance that stores and updates color combination.
        :param deck_label: Tkinter label that displays current color combination.
        """
        self.location = location
        self.image_on = image_on
        self.image_off = image_off
        self.manacolor = manacolor
        self.button_toggle = IntVar()
        self.button = ttk.Button(
            master=self.location, image=image_off, command=lambda: self.button_action(commander, deck_label)
        )

    def button_action(self, commander: Commander, deck_label: DeckLabel) -> None:
        """
        Processes press button action by changing status value, Commander color combination, and deck label text.
        :param commander: Commander class instance that stores and updates color combination.
        :param deck_label: Tkinter label that displays current color combination.
        :return: None. Just updates Commander class instance.
        """
        if self.button_toggle.get() == 1:
            self.button_toggle.set(0)
            self.button.config(image=self.image_off)
            commander.colors.remove(self.manacolor)
            commander.update()
            deck_label.update(commander)
        else:
            self.button_toggle.set(1)
            self.button.config(image=self.image_on)
            commander.colors.append(self.manacolor)
            commander.update()
            deck_label.update(commander)

    def place_button(self, row: int, column: int) -> None:
        """
        Places ManaButton into grid-type frame.
        :param row: Row number
        :param column: Column number
        :return: None. Just places the button into the grid.
        """
        self.button.grid(row=row, column=column)


class PowerButton:
    """
    The class to create a deck power option radiobutton to select deck power level.

    Attributes:
         location(Frame): Tkinter frame to hold all radiobuttons.
         text(str): Text to denote radiobutton.
         value(str): Text to pass into variable.
         variable(StringVar): Tkinter variable to store current selection status.
         button(Radiobutton): ttk selectable button.

    """

    def __init__(self, location: Frame, text: str, value: str, variable: StringVar):
        """
        Initializes PowerButton with frame, text, status value, status variable, and button itself.
        :param location: Tkinter frame to hold all radiobuttons.
        :param text: Button name to be displayed.
        :param value: Value to pass to status variable.
        :param variable: Tkinter variable to store current button status.
        """
        self.location = location
        self.text = text
        self.value = value
        self.variable = variable  # All buttons with the same variable are tied together.
        self.button = ttk.Radiobutton(master=self.location, text=self.text, value=self.value, variable=self.variable)

    def place_button(self, row: int, column: int, sticky: str) -> None:
        """
        Places the button into grid-type frame.
        :param row: Row number.
        :param column: Column number.
        :param sticky: Alignment to frame side.
        :return: None. Just places the button into the grid.
        """
        self.button.grid(row=row, column=column, sticky=sticky)


class OptionButton:
    """
    The class to create the checkbutton to show/hide utility lands.

    Attributes:
        location: Tkinter frame to hold the button.
        button_toggle: Tkinter variable to store current check status.
        text: Text to display near the checkbox.
        button: ttk checkbutton.
    """

    def __init__(self, location: Frame, text: str):
        """
        Initializes OptionButton with frame, check store variable, displayed text, and button itself.
        :param location: Tkinter frame to store the button.
        :param text: Text to display as button name.
        """
        self.location = location
        self.button_toggle = IntVar()
        self.button_toggle.set(1)  # Initial value (Utility lands will be shown)
        self.text = text
        self.button = ttk.Checkbutton(master=self.location, text=self.text, variable=self.button_toggle)

    def place_button(self, row: int, column: int, sticky: str) -> None:
        """
        Places the button into grid-type frame.
        :param row: Row number.
        :param column: Column number.
        :param sticky: Alignment to frame side.
        :return: None. Just places the button into the grid.
        """
        self.button.grid(row=row, column=column, sticky=sticky, padx=(20, 0))


class ActionButton:
    """
    The class to create a button that starts the core function of the application when pressed.

    Attributes:
        location(Frame): Tkinter frame to hold the button.
        button(Button): Tkinter button that starts the function when pressed.
    """

    # Can't initialize with exact values because command function is dynamic.
    def __init__(
        self, location: Frame, colors: list, power: StringVar, utility: OptionButton, cursor, text_area: Text
    ):
        bold_font = font.Font(family="Arial", size=14, weight="bold")
        self.location = location
        self.button = tk.Button(
            self.location,
            text="SHOW LANDS",
            width=20,
            font=bold_font,
            command=lambda: self.show_lands(colors, power, utility, cursor, text_area),
        )

    @staticmethod
    def show_lands(colors: list, power: StringVar, utility: OptionButton, cursor, text_area: Text) -> None:
        """
        Forms a SQLite query, executes it to retrieve a list of lands, processes the list and updates the output widget.
        Triggers when the main button is pressed.
        :param colors: List of colors from Commander class instance attribute.
        :param power: Power option value from radiobutton status variable.
        :param utility: Show/hide utility lands status from checkbutton.
        :param cursor: sqlite3 object to interact with the database.
        :param text_area: Tkinter Text widget to display the selected lands.
        :return: None. Updates the widget.
        """
        query = cl.form_query(colors, power.get(), utility.button_toggle.get())
        lands = cl.select_lands(query, cursor)
        output_text = cl.process_lands(lands)
        text_area.replace("1.0", END, output_text)

    #       print(output_text)

    def place_button(self):
        """
        Places the button into the root container.
        :return: None. Just places the button into the container.
        """
        self.button.pack()


class ExportButton:
    """
    The class to create a button that gets the text from the Text widget,
    saves it to the user PC as *.txt, and opens the file.

    Attributes:
    location(Frame): Tkinter frame to hold the button.
    button(Button): Tkinter button with a command to save the lands into a txt file.
    """

    def __init__(self, location, text_widget):
        """
        Initializes the Button with the frame, and button itself.
        :param location: Tkinter frame to hold the button.
        :param text_widget: Tkinter Text widget from where the text is retrieved.
        """
        self.location = location
        self.button = tk.Button(
            master=self.location, text="Download as *.txt", command=lambda: fs.save_and_open_text(text_widget)
        )

    def place_button(self, pady: int, anchor) -> None:
        """
        Places the button into the root container.
        :param pady: Distance from edge.
        :param anchor: Alignment to side.
        :return: None. Just places the button into the container.
        """
        self.button.pack(pady=pady, anchor=anchor)
