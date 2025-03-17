# imports, I honestly dont know what I need and am too scared to remove something
import json
import os
from datetime import datetime, date
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Button, Input, Static
from textual.containers import VerticalScroll
from textual.widgets import Label
from rich.table import Table
import calendar

# my version of a database because I dont want to learn a database
TASKS_FILE = "tasks.json"

# loading all of the tasks from the "database" because I still refuse to learn a database
def load_tasks():
    # if the file exists open it else create it
    if not os.path.exists(TASKS_FILE):
        return []
    # reading the file
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

# opening the file to write in it so that you can finish or add new tasks
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# creating a calendar view
def generate_calendar_view(year, month):
    cal = calendar.monthcalendar(year, month)
    table = Table(title=f"{calendar.month_name[month]} {year}")
    table.add_column("Mon")
    table.add_column("Tue")
    table.add_column("Wed")
    table.add_column("Thu")
    table.add_column("Fri")
    table.add_column("Sat")
    table.add_column("Sun")
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append("")
            else:
                row.append(str(day))
        table.add_row(*row)
    return table

# setting up all the buttons and input fields and tables
class TaskManagerApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        # title
        yield Static("Task Manager", classes="title")
        # input field for the task name
        yield Input(placeholder="Enter task...")
        # input field for the due date
        yield Input(placeholder="Enter due date (YYYY-MM-DD)...", id="due_input")
        # button for adding the task
        yield Button("Add Task", id="add_button")
        # button for marking a task as complete
        yield Button("Complete Task", id="complete_button")
        # button for deleting a task
        yield Button("Delete Task", id="delete_button")
        # button for previous month view
        yield Button("Previous Month", id="prev_month")
        # button for next month view
        yield Button("Next Month", id="next_month")
        # button for quitting the app
        yield Button("Quit", id="quit")
        # table for all the tasks
        yield DataTable(id="task_table")
        # calendar view
        yield Label("", id="calendar_view")
        yield Footer()

    # tbh i dont really know wat this does it was on a tutorial
    def on_mount(self):
        #setting up calendar
        self.current_year = datetime.today().year
        self.current_month = datetime.today().month
        # fixing the issue with the column headers showing up multiple times, this is the first time to it is true
        first = True
        self.load_tasks_into_table(first)
        self.update_calendar()

    #loading all the tasks and adding the checkmark and x for if it is completed or not
    def load_tasks_into_table(self, first):
        table = self.query_one("#task_table", DataTable)
        table.clear()
        # if it is the first time that it is running then it prints the column headers, if not then it skipps this.
        if first:
            # the column headers for the tasks. There are issues with this i think but i really could't be bothered to fix them as it does not crash i think. I want to make this the longest comment I have ever written and I think I have done it
            table.add_columns("#", "Task", "Status", "Due Date")
        tasks = load_tasks()
        # loop to get the stuff and add them to the table from the "database"
        for i, task in enumerate(tasks, 1):
            status = "✔" if task["completed"] else "✘"
            due = task.get("due", "N/A")
            table.add_row(str(i), task["task"], status, due)

    def update_calendar(self):
        calendar_table = generate_calendar_view(self.current_year, self.current_month)
        calendar_label = self.query_one("#calendar_view", Label)
        calendar_label.update(calendar_table)

    # checking if the button was pressed
    def on_button_pressed(self, event: Button.Pressed):
        task_input = self.query_one(Input)
        due_input = self.query_one("#due_input", Input)
        table = self.query_one("#task_table", DataTable)
        tasks = load_tasks()

        # if the add button was pressed then add the tasks
        if event.button.id == "add_button":
            if task_input.value.strip():
                tasks.append({"task": task_input.value, "completed": False, "added": str(datetime.now()), "due": due_input.value.strip() or "N/A"})
                save_tasks(tasks)
                task_input.value = ""
                due_input.value = ""
                # fixing the issue with the column headers showing up multiple times, this isnt the first and so it is false
                first = False
                self.load_tasks_into_table(first)

        # if the complete button is pressed then mark as complete
        elif event.button.id == "complete_button":
            if table.cursor_row is not None and 0 <= table.cursor_row < len(tasks):
                tasks[table.cursor_row]["completed"] = True
                save_tasks(tasks)
                # fixing the issue with the column headers showing up multiple times, this isnt the first and so it is false
                first = False
                self.load_tasks_into_table(first)

        # if the delete button is pressed then delete the task
        elif event.button.id == "delete_button":
            if table.cursor_row is not None and 0 <= table.cursor_row < len(tasks):
                tasks.pop(table.cursor_row)
                save_tasks(tasks)
                # fixing the issue with the column headers showing up multiple times, this isnt the first and so it is false
                first = False
                self.load_tasks_into_table(first)

        elif event.button.id == "prev_month":
            # changing the month
            if self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
            else:
                self.current_month -=1
            # regenerate the calendar view
            self.update_calendar()

        elif event.button.id == "next_month":
            # changing the month
            if self.current_month == 12:
                self.current_month = 2
                self.current_year += 1
            else:
                self.current_month += 1
            # regenerate the calendar view
            self.update_calendar()

        # if the quit button is pressed then exit
        elif event.button.id == "quit":
            self.exit()

# testing purposes because I dont want to integrate into main
if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()
