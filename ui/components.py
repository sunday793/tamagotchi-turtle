import flet as ft

class StatusBar(ft.ProgressBar):
    """Progress bar for displaying tirtie stats."""

    def __init__(self, value: float, color: str, width: int = 150):
        super().__init__(
            value=value,
            color=color,
            height=15,
            width=width
        )