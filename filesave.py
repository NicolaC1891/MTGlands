"""
Module contains functions to export the created land base to *.txt, then save and open it on the user PC.
"""

from tkinter import *
from tkinter import filedialog
import os
import platform
import subprocess


def save_and_open_text(text_widget: Text) -> None:
    """
    Retrieves the text from the Text widget, writes to txt file, asks to save, finally opens the txt file.
    :param text_widget: Tkinter Text widget to display selected lands.
    :return: None. User refuses from saving the file, or the saved file opens.
    """
    text_content = text_widget.get("1.0", END).rstrip()  # Getting text from the widget (str)

    # Open dialogue to save a file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save as"
    )

    # Saving cancelled by the user
    if not file_path:
        return

    # Writing text into file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_content)

    # Opening file in OS
    open_file(file_path)


def open_file(filepath) -> None:
    """
    Opens the file on the user PC depending on the OS.
    :param filepath: filedialog object (type?)
    :return: None. Opens the file on the user PC.
    """
    # Define OS and call the open command
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", filepath])
    else:
        subprocess.call(["xdg-open", filepath])  # Linux and others
