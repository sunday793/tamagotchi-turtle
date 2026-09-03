import flet as ft

class StatusBar(ft.ProgressBar):
    """Progress bar for displaying tirtie stats."""

    def __init__(self, value: float, color: str, height:int = 15, width: int = 150):
        super().__init__(
            value=value,
            color=color,
            height=height,
            width=width
        )