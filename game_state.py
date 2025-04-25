class GameState:
    def __init__(self, loader):
        self.loader = loader
        self.current_room = loader.rooms["entrance_hall"]
        self.inventory = []
        self.health = 100

    def move_to_room(self, direction):
        if direction in self.current_room.exits:
            next_room_id = self.current_room.exits[direction]
            self.current_room = self.loader.rooms[next_room_id]
            return True
        return False