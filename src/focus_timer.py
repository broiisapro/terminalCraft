# imports
import os
from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static
from textual.containers import VerticalScroll, Container

# the app
class TimerApp(App):
    # timer defaults
    def __init__(self):
        super().__init__()
        self.timer = None
        self.remaining_time = 0
        self.running = False

    # buttons and stuff
    def compose(self) -> ComposeResult:
        yield Static("Timer App", classes="title")
        yield Input(placeholder="Enter time in minutes", id="time-input")
        yield Static("00:00", id="timer-display")
        yield Button("Start", id="start")
        yield Button("Pause", id="pause")
        yield Button("Reset", id="reset")

    def format_time(self) -> str:
        minutes, seconds = divmod(self.remaining_time, 60)
        return f"{minutes:02}:{seconds:02}"

    def update_display(self):
        self.query_one("#timer-display", Static).update(self.format_time())

    # checking if a button is pressed
    def on_button_pressed(self, event: Button.Pressed):

        # if the start button is pressed start the timer
        if event.button.id == "start":
            self.start_timer()

        # if the pause button is pressed, pause
        elif event.button.id == "pause":
            self.pause_timer()

        # reset if the reset button is pressed
        elif event.button.id == "reset":
            self.reset_timer()

    # start the timer
    def start_timer(self):
        if not self.running:
            input_widget = self.query_one("#time-input", Input)
            try:
                self.remaining_time = int(input_widget.value) * 60
            except ValueError:
                self.notify("Invalid input! Enter a number.", title="Error")
                return
            self.running = True
            self.timer = self.set_interval(1, self.tick)
            self.update_display()

    # pause the timer
    def pause_timer(self):
        if self.running and self.timer:
            self.running = False
            self.timer.stop()

    # reset the timer
    def reset_timer(self):
        if self.timer:
            self.timer.stop()
        self.running = False
        self.remaining_time = 0
        self.update_display()

    # decrease time by one until it is done then say time is up
    def tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_display()
        else:
            self.timer.stop()
            self.running = False
            self.notify("Time's up!", title="Timer Done")

if __name__ == "__main__":
    TimerApp().run()
