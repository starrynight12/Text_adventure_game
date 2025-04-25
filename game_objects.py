import json
from dataclasses import dataclass

@dataclass
class GameObject:
    id: str
    name: str
    description: str

class Room(GameObject):
    def __init__(self, id, name, description, exits, items, actions):
        super().__init__(id, name, description)
        self.exits = exits
        self.items = items
        self.actions = actions

class Item(GameObject):
    def __init__(self, id, name, description, takeable):
        super().__init__(id, name, description)
        self.takeable = takeable
