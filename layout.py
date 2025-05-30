"""
This module contains functions to create and place GUI elements such as application window, frames, labels.
"""

from tkinter import *
from tkinter import ttk
from tkinter import font
from commander import *


def create_layout() -> Tk:
    """
    Creates the main application window
    :return: tkinter GUI window
    """
    layout = Tk()
    layout.title("EDH Landbase Creator")  # Headline
    layout.geometry("600x900")  # Window size
    layout.iconphoto(True, PhotoImage(file="Images/MTGicon.png"))  # Headline icon
    return layout


def greet() -> Label:
    """
    Creates a greeting/version message to be placed  in the upper part of the window
    :return: tkinter label with text
    """
    greeting = Label(text="*** This is a MVP version of the application ***")
    return greeting


def create_mana_frame() -> Frame:
    """
    Creates and configures a grid-type frame to hold mana buttons
    :return: ttk grid-type frame with five columns
    """
    mana_frame = ttk.Frame(relief=RAISED, padding=[10, 10])
    mana_frame.columnconfigure(0, weight=1)
    mana_frame.columnconfigure(1, weight=1)
    mana_frame.columnconfigure(2, weight=1)
    mana_frame.columnconfigure(3, weight=1)
    mana_frame.columnconfigure(4, weight=1)
    return mana_frame


def create_options_frame() -> Frame:
    """
    Creates and configures a grid-type frame to hold Budget and Utility buttons
    :return: ttk grid-type frame with three columns
    """
    options_frame = ttk.Frame(width=400)
    options_frame.columnconfigure(0, weight=1)
    options_frame.columnconfigure(1, weight=1)
    options_frame.columnconfigure(2, weight=1)
    return options_frame


def create_action_frame() -> Frame:
    """
    Creates a standard frame to hold the SHOW LANDS button
    :return: ttk default button
    """
    action_frame = ttk.Frame()  # Raised button relief available in ttk only
    return action_frame


def create_text_frame() -> Frame:
    """
    Creates and configures a grid-type frame to hold Text widget and scrollbar
    :return: ttk grid-type frame with two columns
    """
    text_frame = ttk.Frame(width=350, height=450)
    text_frame.columnconfigure(0, weight=1)
    text_frame.rowconfigure(0, weight=1)
    text_frame.pack_propagate(False)
    return text_frame


def select_colors(location: Frame) -> Label:
    """
    Creates a user prompt to be placed in the mana frame
    :param location: mana_frame
    :return: tkinter label with text
    """
    intro = Label(
        location,
        text="PLEASE SELECT THE COLORS OF YOUR COMMANDER",
        font=font.Font(family="Arial", size=14, weight="bold"),
    )
    return intro


class DeckLabel:
    """
    DeckLabel is a class to display dynamic deck label representing a color combination name.

    Attributes:
        location (tk.frame): Tkinter frame where the label will be placed.
        initial text (str): The initial text to display on the label.
        button_outro (tk.StringVar): Tkinter variable that holds the deck label text to be displayed.
        label (tk.Label): Tkinter Label widget that displays the text.
    """

    def __init__(self, location: Frame, initial_text: str):
        """
        Initializes the DeckLabel with a given frame location and given text.
        :param location: Tkinter frame where the label will be placed.
        :param initial_text: The initial text to display on the label.
        """
        self.location = location
        self.button_outro = StringVar()
        self.button_outro.set(initial_text)
        label_font = font.Font(family="Arial", size=14, weight="bold")  # Font for Label available in ttk only
        self.label = Label(location, textvariable=self.button_outro, font=label_font)
        self.label.grid(row=2, column=0, columnspan=5)

    def update(self, commander: Commander) -> None:
        """
        Updates the text label with the current color combination name after any mana button action.
        :param commander: Commander class instance that contains the color combination attribute.
        :return: None. Updates the widget text.
        """
        self.button_outro.set(f"*** {commander.combination} ***")
