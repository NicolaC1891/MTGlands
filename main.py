"""
This application is a land selection tool to build land bases for EDH decks.
"""

import sqlite3

from buttons import *
from commander import *
import layout as lay

# Connecting to SQL
connection = sqlite3.connect("MTG_landbase.db")
cursor = connection.cursor()  # Cursor object (specific for sqlite3) for interaction with the database

# 1. CREATING COMMANDER
commander = Commander()  # Class to operate with color combination

# 2. CREATING GUI
root = lay.create_layout()

# 2.1. Placing greeting message
greeting = lay.greet()
greeting.pack()

# 3. PLACING FRAMES FOR ALL GUI ELEMENTS
mana_frame = lay.create_mana_frame()
options_frame = lay.create_options_frame()
action_frame = lay.create_action_frame()
text_frame = lay.create_text_frame()
mana_frame.pack(anchor=N, expand=True, fill=X, pady=(20, 0))
options_frame.pack(pady=(10, 0))
action_frame.pack(anchor=N, expand=True, fill=X, pady=(20, 0))
text_frame.pack(pady=10)

# 3.1. Placing colors selection message and deck label
selection_message = lay.select_colors(mana_frame)
selection_message.grid(row=0, column=0, columnspan=5)
deck_label = lay.DeckLabel(mana_frame, f"*** {commander.combination} ***")

# 3.2. Placing mana buttons

# 3.2.1. Loading mana images for on and off toggle
white_on, white_off = PhotoImage(file="Images/white_on.png"), PhotoImage(file="Images/white_off.png")
ultra_on, ultra_off = PhotoImage(file="Images/ultra_on.png"), PhotoImage(file="Images/ultra_off.png")
black_on, black_off = PhotoImage(file="Images/black_on.png"), PhotoImage(file="Images/black_off.png")
red_on, red_off = PhotoImage(file="Images/red_on.png"), PhotoImage(file="Images/red_off.png")
green_on, green_off = PhotoImage(file="Images/green_on.png"), PhotoImage(file="Images/green_off.png")

# 3.2.2. Creating mana buttons
white_button = ManaButton(mana_frame, white_on, white_off, "W", commander, deck_label)
ultra_button = ManaButton(mana_frame, ultra_on, ultra_off, "U", commander, deck_label)
black_button = ManaButton(mana_frame, black_on, black_off, "B", commander, deck_label)
red_button = ManaButton(mana_frame, red_on, red_off, "R", commander, deck_label)
green_button = ManaButton(mana_frame, green_on, green_off, "G", commander, deck_label)

# 3.2.3. Placing mana buttons
white_button.place_button(1, 0)
ultra_button.place_button(1, 1)
black_button.place_button(1, 2)
red_button.place_button(1, 3)
green_button.place_button(1, 4)

# 3.3. Placing options buttons

# 3.3.1. Creating radio buttons for power level selection
power = StringVar(value="Collector")  # This is a status line, not displayed but used to store current value
starter_btn = PowerButton(options_frame, "Starter", "Starter", power)
collector_btn = PowerButton(options_frame, "Collector", "Collector", power)
elite_btn = PowerButton(options_frame, "Elite", "Elite", power)

# 3.3.2. Placing radio buttons
starter_btn.place_button(row=0, column=0, sticky="nw")
collector_btn.place_button(row=1, column=0, sticky="nw")
elite_btn.place_button(row=2, column=0, sticky="nw")

# 3.3.3. Creating and placing checkbutton to show(default)/hide utility lands
utility_button = OptionButton(options_frame, "Show utility lands")
utility_button.place_button(row=1, column=2, sticky="e")

# 3.4. Creating and placing output text widget and scrollbar
text_widget = Text(text_frame, width=45, height=30)    # Size parameters are in symbols and lines
text_widget.grid(row=0, column=0, sticky="nsew")
y_scroll = ttk.Scrollbar(master=text_frame, orient="vertical", command=text_widget.yview)
y_scroll.grid(row=0, column=1, sticky=NS)
text_widget["yscrollcommand"] = y_scroll.set    # Tying s/bar to widget. S/bar position updates when text is scrolled.


# 3.5. Creating and placing button to save text widget contents as txt
export_button = ExportButton(root, text_widget)
export_button.place_button(pady=10, anchor="s")

# 3.6. Creating and placing action button (core functionality)
action_button = ActionButton(action_frame, commander.colors, power, utility_button, cursor, text_widget)
action_button.place_button()

# 4. STARTING THE WINDOW
root.mainloop()
