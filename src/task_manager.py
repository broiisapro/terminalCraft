import json
import os
from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Button, Input, Static
from textual.containers import VerticalScroll

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

class TaskManagerApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Task Manager", classes="title")
        yield Input(placeholder="Enter task...")
        yield Input(placeholder="Enter due date (YYYY-MM-DD)...", id="due_input")
        yield Button("Add Task", id="add_button")
        yield Button("Complete Task", id="complete_button")
        yield Button("Delete Task", id="delete_button")
        yield DataTable(id="task_table")
        yield Footer()

    def on_mount(self):
        self.load_tasks_into_table()

    def load_tasks_into_table(self):
        table = self.query_one("#task_table", DataTable)
        table.clear()
        table.add_columns("#", "Task", "Status", "Due Date")
        tasks = load_tasks()
        for i, task in enumerate(tasks, 1):
            status = "✔" if task["completed"] else "✘"
            due = task.get("due", "N/A")
            table.add_row(str(i), task["task"], status, due)

    def on_button_pressed(self, event: Button.Pressed):
        task_input = self.query_one(Input)
        due_input = self.query_one("#due_input", Input)
        table = self.query_one("#task_table", DataTable)
        tasks = load_tasks()

        if event.button.id == "add_button":
            if task_input.value.strip():
                tasks.append({"task": task_input.value, "completed": False, "added": str(datetime.now()), "due": due_input.value.strip() or "N/A"})
                save_tasks(tasks)
                task_input.value = ""
                due_input.value = ""
                self.load_tasks_into_table()
        elif event.button.id == "complete_button":
            if table.cursor_row is not None and 0 <= table.cursor_row < len(tasks):
                tasks[table.cursor_row]["completed"] = True
                save_tasks(tasks)
                self.load_tasks_into_table()
        elif event.button.id == "delete_button":
            if table.cursor_row is not None and 0 <= table.cursor_row < len(tasks):
                tasks.pop(table.cursor_row)
                save_tasks(tasks)
                self.load_tasks_into_table()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()
