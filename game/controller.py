import asyncio

class GameController:
    """Controls the game loop and async events."""

    TICK_TIMEOUT = 10.0
    HEALTH_DECREASE_TICKS = 3

    def __init__(self, turtie):
        self.turtie = turtie
        self.feed_event = asyncio.Event()
        self.wash_event = asyncio.Event()
        self.tick_count = 0

    async def feed(self) -> bool:
        """Handle feeding action."""
        if self.turtie.feed():
            self.feed_event.set()
            return True
        return False

    async def wash(self) -> bool:
        """Handle washing action."""
        if self.turtie.wash():
            self.wash_event.set()
            return True
        return False

    async def run_game_loop(self, on_update) -> bool:
        """Main game loop that runs until turtie is healthy."""
        while self.turtie.is_healthy:
            try:
                await asyncio.wait_for(
                    asyncio.gather(
                        self.feed_event.wait(),
                        self.wash_event.wait(),
                        return_exceptions=True
                    ),
                    timeout=self.TICK_TIMEOUT
                )
                self.feed_event.clear()
                self.wash_event.clear()
            except asyncio.TimeoutError:
                self.tick_count += 1
                self.turtie.decrease_satiety()

                if self.tick_count >= self.HEALTH_DECREASE_TICKS:
                    self.turtie.decrease_health()
                    self.tick_count = 0

                on_update()