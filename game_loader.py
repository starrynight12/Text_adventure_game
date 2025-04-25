import json
from game_objects import Room, Item

class GameLoader:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.game_data = json.load(f)
        
        self.rooms = {}
        self.items = {}
        
        self._load_items()
        self._load_rooms()

    def _load_items(self):
        for item_id, data in self.game_data["items"].items():
            self.items[item_id] = Item(
                id=item_id,
                name=data["name"],
                description=data["description"],
                takeable=data.get("takeable", False)
            )

    def _load_rooms(self):
        for room_id, data in self.game_data["rooms"].items():
            self.rooms[room_id] = Room(
                id=room_id,
                name=data["name"],
                description=data["description"],
                exits=data["exits"],
                items=[self.items[item_id] for item_id in data["items"]],
                actions=data.get("actions", {})
            )