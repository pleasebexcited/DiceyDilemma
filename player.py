class Player:
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = max_health
        self.gold = 0  # Starting gold
        self.max_shield = 100
        self.shield = 100  # Starting shield
        
        # Power-up inventory (6 slots)
        self.power_ups = [None] * 6  # None = empty slot
    
    def take_damage(self, damage):
        """Take damage, shield absorbs first, then health"""
        remaining_damage = damage
        
        # Shield absorbs damage first
        if self.shield > 0:
            if self.shield >= remaining_damage:
                self.shield -= remaining_damage
                remaining_damage = 0
            else:
                remaining_damage -= self.shield
                self.shield = 0
        
        # Any remaining damage goes to health
        if remaining_damage > 0:
            self.health = max(0, self.health - remaining_damage)
    
    def heal(self, amount):
        """Heal the player up to max health"""
        self.health = min(self.max_health, self.health + amount)
    
    def refill_shield(self):
        """Refill shield to maximum"""
        self.shield = self.max_shield
    
    def is_alive(self):
        """Check if player is alive"""
        return self.health > 0
    
    def get_health_percentage(self):
        """Get health as a percentage"""
        return self.health / self.max_health
    
    def get_shield_percentage(self):
        """Get shield as a percentage"""
        return self.shield / self.max_shield
    
    def earn_gold(self, amount):
        """Earn gold based on score"""
        self.gold += amount
    
    def spend_gold(self, amount):
        """Spend gold (returns True if successful, False if insufficient)"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def get_gold(self):
        """Get current gold amount"""
        return self.gold
    
    def add_power_up(self, power_up):
        """Add a power-up to the first available slot"""
        for i in range(len(self.power_ups)):
            if self.power_ups[i] is None:
                self.power_ups[i] = power_up
                return True
        return False  # No empty slots
    
    def get_power_ups(self):
        """Get all power-ups in inventory"""
        return [p for p in self.power_ups if p is not None]
    
    def has_power_up(self, power_up_name):
        """Check if player has a specific power-up"""
        return any(p and p["name"] == power_up_name for p in self.power_ups)
    
    def get_power_up_count(self, power_up_name):
        """Get count of a specific power-up"""
        return sum(1 for p in self.power_ups if p and p["name"] == power_up_name) 