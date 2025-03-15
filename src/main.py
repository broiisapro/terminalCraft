from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static

class HomeScreen(Container):
    def compose(self) -> ComposeResult:
        yield Static("Welcome to Life! Choose an option", classes="title")
        yield Button("Focus Timer", id="focus_timer")
        yield Button("Habit Tracker", id="habit_tracker")
        yield Button("Task Manager", id="task_manager")
        yield Button("Quit", id="quit")

class Life(App):
    CSS_PATH = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield HomeScreen()
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "focus_timer":
                self.notify("Focus Tiemr Selected! (Coming Soon!)")
            case "habit_tracker":
                self.notify("Habit Tracker Selected! (Coming Soon!)")
            case "task_manager":
                self.notify("Task Manager Selected! (Coming Soon!)")
            case "quit":
                self.exit()

if __name__ == "__main__":
    app = Life()
    app.run()
