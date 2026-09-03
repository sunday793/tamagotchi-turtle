class MyTurtie():
    """Game logic for the turtie"""

    MAX_HEALTH = 20
    MAX_SATIETY = 10
    
    def __init__(self):
        self.is_sleeping = False
        self.is_healthy = True
        self.is_full = True
        self.is_being_washed = False
        self.health = self.MAX_HEALTH
        self.satiety = self.MAX_SATIETY
        
    def feed(self) -> bool:
        """Feed the turtie. Returns True if successful."""
        if self.satiety < self.MAX_SATIETY and not self.is_sleeping:
            self.satiety += 1
            if not self.is_full and self.satiety == self.MAX_SATIETY:
                self.is_full = True
            return True
        return False
            
    def decrease_satiety(self) -> None:
        """Decrease satiety over time."""
        if self.satiety > 0:
            self.satiety -= 1
        if self.satiety == 0:
            self.is_full = False
            
    def wash(self) -> bool:
        """Wash the turtie. Returns True if successful."""
        if self.health < self.MAX_HEALTH and not self.is_sleeping:
            self.health += 1
            if not self.is_healthy and self.health == self.MAX_HEALTH:
                self.is_healthy = True
            return True
        return False
    
    def decrease_health(self) -> None:
        """Decrease health over time."""
        if self.health > 0:
            self.health -= 1
        if self.health == 0:
            self.is_healthy = False
    
    def apply_time_offline(self, minutes: int) -> None:
        """Apply offline time penalties."""
        hunger = int(minutes / 60)
        self.satiety = max(0, self.satiety - hunger)
        sick = int(minutes / 60)
        self.health = max(0, self.health - sick)
        
        if self.satiety == 0:
            self.is_full = False
        if self.health == 0:
            self.is_healthy = False