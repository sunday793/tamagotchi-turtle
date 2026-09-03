import flet as ft
import asyncio
from game import MyTurtie, GameController
from ui.components import StatusBar

class MainWindow(ft.SafeArea):
    """Main UI window for the Tamagotchi game."""

    W = 170
    H = 90
    
    def __init__(self):
        """Initialize the main window with game logic."""
        super().__init__()
        self.turtie = MyTurtie()
        self.controller = GameController(self.turtie)
    
    async def build_ui(self, page: ft.Page):
        """Build the user interface."""
        page.title = "Черепашка Куть-Куть 🐢"
        page.window.width = 350
        page.window.height = 500
        
        await page.window.wait_until_ready_to_show()
        await page.window.center()
        
        page.padding = 0
        
        
        img_turtie_happy = ft.Image(src="turtie_happy.png", opacity=1.0)
        img_smiling = ft.Image(src="turtie_smiling.png", opacity=0.0)
        img_jumping = ft.Image(src="turtie_jumping.png", opacity=0.0)
        img_eating = ft.Image(src="eating.png", width=self.W, height=self.H, opacity=0.0)
        img_sad = ft.Image(src="turtie_sad.png", width=self.W, height=self.H, opacity=0.0)
        img_love = ft.Image(src="love.png", width=self.W, height=self.H, opacity=0.0)
        img_love_2 = ft.Image(src="love_2.png", width=self.W, height=self.H, opacity=0.0)
        img_love_3 = ft.Image(src="love_3.png", width=self.W, height=self.H, opacity=0.0)
        
        img_list = [img_turtie_happy, img_smiling, img_jumping, img_sad, img_eating, img_love, img_love_2, img_love_3]
        
        turtie_img_stack = ft.Stack(
            controls=[
                img_love_3,
                img_love_2, 
                img_love,
                img_sad,
                img_eating,
                img_jumping,
                img_smiling,
                img_turtie_happy
            ],
            width=self.W,
            height=self.H,
            tooltip=None
        )
                
        satiety_bar = StatusBar(value = self.turtie.satiety / self.turtie.MAX_SATIETY,
                                    color = ft.Colors.PINK_100,
                                    height = 15,
                                    width = 150
        )
        
        health_bar = StatusBar(value = self.turtie.health / self.turtie.MAX_HEALTH,
                                    color = ft.Colors.YELLOW_100,
                                    height = 15,
                                    width = 150
        )
        
        def show_img(target_img):
            """Show only the target image, hide all others."""
            for img in img_list:
                img.opacity = 1.0 if img==target_img else 0.0
        
        async def click_btn_feed():
            """Handle feeding action."""
            if self.turtie.satiety == self.turtie.MAX_SATIETY:
                return

            await self.controller.feed()
            satiety_bar.value = self.turtie.satiety / self.turtie.MAX_SATIETY
            
            show_img(img_smiling)
            page.update() 
            await asyncio.sleep(2)
            
            show_img(img_turtie_happy if self.turtie.satiety > 3 else img_sad)
            page.update()
        
        async def tap_img_salad(e):
            """Handle click on salad."""
            if self.turtie.satiety == self.turtie.MAX_SATIETY:
                salad_clickable.disabled = True
                page.update()
            else:    
                img_salad.scale = 2.0
                page.update()
                
                await asyncio.sleep(0.15)
                
                img_salad.scale = 1.6
                page.update()
                page.run_task(click_btn_feed)
            
        async def start_washing(e: ft.DragTargetEvent):
            """Handle start of washing."""
            await self.controller.wash()
            health_bar.value = self.turtie.health / self.turtie.MAX_HEALTH
            show_img(img_jumping)
            page.update()
                
        async def finish_washing(e: ft.DragTargetLeaveEvent):
            """Handle end of washing."""
            show_img(img_turtie_happy if self.turtie.satiety > 3 else img_sad)
            page.update()
                
        async def drop_sponge(e: ft.DragTargetEvent):
            """Handle sponge drop."""
            show_img(img_turtie_happy)
            page.update()
                
        turtie_with_interaction = ft.DragTarget(
            content=turtie_img_stack,
            group="turtie_cleaning",
            on_move=start_washing,
            on_leave=finish_washing,
            on_accept=drop_sponge
        )
        
        img_sponge = ft.Image(
            src="sponge.png",
            width=20,
            height=20,
            scale=1.6,
            tooltip="помой Куть-Куть!"
        )
        
        sponge_draggable = ft.Draggable(
            content=img_sponge,
            group="turtie_cleaning",
            content_feedback= ft.Container(
                content=img_sponge,
                opacity=1.0
            ),
            content_when_dragging=ft.Container(
                content=img_sponge,
                opacity=0.0
            )
        )
    
        img_salad = ft.Image(
            src="salad_2.png",
            width=20,
            height=20,
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            scale=1.6,
            tooltip="покорми Куть-Куть!"
        )
        
        salad_clickable = ft.GestureDetector(
            content=img_salad,
            on_tap=tap_img_salad
        )
        
        async def live_timer():
            """Update UI after each game tick."""
            satiety_bar.value = self.turtie.satiety / self.turtie.MAX_SATIETY
            health_bar.value = self.turtie.health / self.turtie.MAX_HEALTH
                
            if self.turtie.satiety <= 3 or self.turtie.health <= 6:
                show_img(img_sad)
                        
            if self.turtie.satiety == 0:
                turtie_img_stack.tooltip = "Куть-Куть хочет кушать 🥬"
            elif self.turtie.health == 0:
                turtie_img_stack.tooltip = "Куть-Куть заболела 🥺"
            else:
                turtie_img_stack.tooltip = None
        
            page.update()
                            
        ui_content = ft.Column(
            controls=[
                turtie_with_interaction,
                ft.Row(
                    controls = [
                        ft.Column(
                            controls = [
                                ft.Text("Сытость черепашки", color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
                                satiety_bar
                            ]
                        ),
                        ft.Column(
                            controls = [
                                ft.Text("Здоровье черепашки", color=ft.Colors.BLACK),
                                health_bar
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(height=10),
                ft.Row(
                    controls =[
                        salad_clickable,
                        ft.Container(width=20),
                        sponge_draggable
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER   
        )
        
        game_card = ft.Container(
            content=ui_content,
            width=350,
            height=500,
            image=ft.DecorationImage(src="back.png"),
            alignment=ft.Alignment.CENTER,
            padding=ft.Padding(bottom=40)
        )
        
        background_container = ft.Container(
            content=game_card,
            expand=True,
            bgcolor=ft.Colors.WHITE,
            alignment=ft.Alignment.CENTER,
        )
        
        page.add(background_container)
        page.run_task(self.controller.run_game_loop, live_timer)