import flet as ft
import asyncio
import time
# import database

class MyTurtie():
    
    def __init__(self):
        self.is_sleeping = False
        self.is_healthy = True
        self.is_full = True
        self.is_being_washed = False
        self.health = 20 # max of the health
        self.satiety = 10 # max of satiety
        
    def feed(self):
        if self.satiety < 10 and not self.is_sleeping:
            self.satiety += 1
        if not self.is_full and self.satiety == 10:
            self.is_full = True
            
    def decrease_satiety(self):
        if self.satiety > 0:
            self.satiety -= 1
        if self.satiety == 0:
            self.is_full = False
            
    def wash(self):
        if self.health < 20 and not self.is_sleeping:
            self.health += 1
        if not self.is_healthy and self.health == 20:
            self.is_healthy = True
    
    def decrease_health(self):
        if self.health > 0:
            self.health -= 1
        if self.health == 0:
            self.is_healthy = False
    
    def apply_time_offline(self, minutes: int):
        hunger = int(minutes / 60)
        self.satiety = max(0, self.satiety - hunger)
        sick = int(minutes / 60)
        self.health = max(0, self.health - sick)
        
        if self.satiety == 0:
            self.is_full = False
        if self.health == 0:
            self.is_healthy = False
        
        
class MainWindow(ft.SafeArea):
    
    def __init__(self):
        super().__init__
        self.turtie = MyTurtie()
    
    async def build_ui(self, page: ft.Page):
        page.title = "Черепашка Куть-Куть 🐢"
        page.window.width = 350
        page.window.height = 500
        
        await page.window.wait_until_ready_to_show()
        await page.window.center()
        
        page.padding = 0
        
        W = 170
        H = 90
        
        img_turtie_happy = ft.Image(src="turtie_happy.png", opacity=1.0)
        # img_happy = ft.Image(src="happy.png", width=W, height=H, opacity=0.0)
        img_smiling = ft.Image(src="turtie_smiling.png", opacity=0.0)
        img_jumping = ft.Image(src="turtie_jumping.png", opacity=0.0)
        img_eating = ft.Image(src="eating.png", width=W, height=H, opacity=0.0)
        img_sad = ft.Image(src="turtie_sad.png", width=W, height=H, opacity=0.0)
        img_love = ft.Image(src="love.png", width=W, height=H, opacity=0.0)
        img_love_2 = ft.Image(src="love_2.png", width=W, height=H, opacity=0.0)
        img_love_3 = ft.Image(src="love_3.png", width=W, height=H, opacity=0.0)
        
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
            width=W,
            height=H,
            tooltip=None
        )
                
        satiety_bar = ft.ProgressBar(value = self.turtie.satiety / 10,
                                    color = ft.Colors.PINK_100,
                                    height = 15,
                                    width = 150
        )
        
        health_bar = ft.ProgressBar(value = self.turtie.health / 20,
                                    color = ft.Colors.YELLOW_100,
                                    height = 15,
                                    width = 150
        )
        
        def show_img(target_img):
            for img in img_list:
                img.opacity = 1.0 if img==target_img else 0.0
        
        feed_event = asyncio.Event()
        wash_event = asyncio.Event()
        
        async def click_btn_feed():
            if self.turtie.satiety == 10:
                return
            
            self.turtie.feed()
            satiety_bar.value = self.turtie.satiety / 10
            
            feed_event.set()
            
            show_img(img_smiling)
            page.update() 
            await asyncio.sleep(2)
            
            # show_img(img_love)
            # page.update()
            # await asyncio.sleep(1)
            
            # show_img(img_love_2)
            # page.update()
            # await asyncio.sleep(1)
            
            # show_img(img_love)
            # page.update()
            # await asyncio.sleep(1)
            
            show_img(img_turtie_happy if self.turtie.satiety > 3 else img_sad)
            page.update()
        
        async def tap_img_salad(e):
            if self.turtie.satiety == 10:
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
            if self.turtie.health < 20:
                self.turtie.wash()
                health_bar.value = self.turtie.health / 20
                wash_event.set()
            # if not self.turtie.is_being_washed:
            # self.turtie.is_being_washed = True
            show_img(img_jumping)
            page.update()
            # print("I'M JUMPING!!")
                
        async def finish_washing(e: ft.DragTargetLeaveEvent):
            # if self.turtie.is_being_washed:
                # self.turtie.is_being_washed = False
            show_img(img_turtie_happy if self.turtie.satiety > 3 else img_sad)
            page.update()
            # print("I'M SMILING!!")
                
        async def drop_sponge(e: ft.DragTargetEvent):
            # self.turtie.is_being_washed = True
            show_img(img_turtie_happy)
            page.update()
            # print("I'M DROPPING THE SPONGE!!")
                
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
            tick_count = 0
            while self.turtie.is_healthy:
                try:
                    await asyncio.wait_for(
                        asyncio.gather(feed_event.wait(), wash_event.wait(), return_exceptions=True),
                        timeout=10.0
                    )
                    feed_event.clear()
                    wash_event.clear()
                except asyncio.TimeoutError:
                    self.turtie.decrease_satiety()
                    satiety_bar.value = self.turtie.satiety / 10
                    
                    tick_count+=1
                    if tick_count >= 3:
                        self.turtie.decrease_health()
                        health_bar.value = self.turtie.health / 20
                        tick_count = 0
                
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
        page.run_task(live_timer)
            
        
        # time_opened = time.time()
        # time_closed = database.get_last_closed_time()
        # passed_minutes = (time_closed - time_opened) / 60
        # self.turtie.apply_time_offline(passed_minutes)
    