from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static
from textual import css

from src.focus_timer import TimerApp
from src.habit_tracker import HabitTrackerApp
from src.task_manager import TaskManagerApp

class MainContainer(Vertical):
    CSS = """
    Vertical{
        background: $surface;
        color: $text;
        padding: 1;
        height: 100%;
    }

    .title {
        content-align: center middle;
        height: 3;
        text-style: bold;
        color: $accent;
        text-align: center;
        padding: 1;
    }

    Button {
        width: 100%;
        margin: 1;
        height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Welcome to Life! Choose an option", classes="title")
        yield Button("Focus Timer", id="focus_timer")
        yield Button("Habit Tracker", id="habit_tracker")
        yield Button("Task Manager", id="task_manager")
        yield Button("Quit", id="quit")

class TimerScreen(Screen):
    def __init__(self):
        super().__init__()
        self.timer_app = TimerApp()

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.timer_app
        yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.app.pop_screen()

class HabitTrackerScreen(Screen):
    def __init__(self):
        super().__init__()
        self.habit_tracker_app = HabitTrackerApp()

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.habit_tracker_app
        yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.app.pop_screen()

class TaskManagerScreen(Screen):
    def __init__(self):
        super().__init__()
        self.task_manager_app = TaskManagerApp()

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.task_manager_app
        yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.app.pop_screen()

class Life(App):
    CSS = """
    App {
        background: $surface;
        color: $text;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield MainContainer()
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "focus_timer":
                self.push_screen(TimerScreen())
            case "habit_tracker":
                self.push_screen(HabitTrackerScreen())
            case "task_manager":
                self.push_screen(TaskManagerScreen())
            case "quit":
                self.exit()

if __name__ == "__main__":
    app = Life()
    app.run()
