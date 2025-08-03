class Enemy:
    def __init__(self, enemy_type, health):
        self.enemy_type = enemy_type
        self.max_health = health
        self.health = health
        self.max_shield = 100
        self.shield = 100  # Starting shield
    
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
    
    def is_alive(self):
        """Check if enemy is alive"""
        return self.health > 0
    
    def get_health_percentage(self):
        """Get health as a percentage"""
        return self.health / self.max_health
    
    def get_shield_percentage(self):
        """Get shield as a percentage"""
        return self.shield / self.max_shield
    
    def get_display_name(self):
        """Get a display name for the enemy"""
        return f"Level {self.enemy_type}" 