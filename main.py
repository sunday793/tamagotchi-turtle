import flet as ft
from app import MainWindow

if __name__ == "__main__":
    window = MainWindow()
    ft.run(window.build_ui, assets_dir = "assets", view=ft.AppView.FLET_APP_HIDDEN)
