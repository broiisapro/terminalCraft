import os
import json
from datetime import datetime, date
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static, DataTable
from textual.containers import VerticalScroll

# Define the path to store habits in the /data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get terminalCraft directory
DATA_DIR = os.path.join(BASE_DIR, "data")
HABITS_FILE = os.path.join(DATA_DIR, "habits.json")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_habits():
    if not os.path.exists(HABITS_FILE):
        return {"last_reset": str(date.today()), "habits": []}
    with open(HABITS_FILE, "r") as file:
        data = json.load(file)

    if data["last_reset"] != str(date.today()):
        for habit in data["habits"]:
            habit["completed"] = False
        data["last_reset"] = str(date.today())
        save_habits(data)

    return data

def save_habits(data):
    with open(HABITS_FILE, "w") as file:
        json.dump(data, file, indent=4)

class HabitTrackerApp(App):
    def __init__(self):
        super().__init__()
        self.data = load_habits()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Habit Tracker", classes="title")
        yield Input(placeholder="Enter habit name", id="habit-input")
        yield Button("Add Habit", id="add")
        yield Button("Mark as Completed", id="complete")
        yield Button("Delete Habit", id="delete")
        yield Button("Quit", id="quit")
        yield DataTable(id="habit-table")
        yield Footer()

    def on_mount(self):
        self.load_habits_into_table(True)

    def load_habits_into_table(self, first):
        table = self.query_one("#habit-table", DataTable)
        table.clear()
        if first:
            table.add_columns("#", "Habit", "Completed")
        for i, habit in enumerate(self.data["habits"], 1):
            status = "✔" if habit["completed"] else "✘"
            table.add_row(str(i), habit["name"], status)

    def on_button_pressed(self, event: Button.Pressed):
        habit_input = self.query_one("#habit-input", Input)
        table = self.query_one("#habit-table", DataTable)

        if event.button.id == "add":
            if habit_input.value.strip():
                self.data["habits"].append({"name": habit_input.value, "completed": False})
                save_habits(self.data)
                habit_input.value = ""
                self.load_habits_into_table(False)

        elif event.button.id == "complete":
            if table.cursor_row is not None and 0 <= table.cursor_row < len(self.data["habits"]):
                self.data["habits"][table.cursor_row]["completed"] = True
                save_habits(self.data)
                self.load_habits_into_table(False)

        elif event.button.id == "delete":
            if table.cursor_row is not None and 0 <= table.cursor_row < len(self.data["habits"]):
                self.data["habits"].pop(table.cursor_row)
                save_habits(self.data)
                self.load_habits_into_table(False)

        elif event.button.id == "quit":
            self.exit()

if __name__ == "__main__":
    HabitTrackerApp().run()
