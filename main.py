# adventure_game.py
import json
import re

# Valid verbs and their synonyms
VERBS = {
    "go": ["move", "walk", "head", "travel", "enter", "proceed", "advance"],
    "take": ["grab", "pick", "steal", "collect", "acquire"],
    "use": ["utilize", "employ", "apply", "operate" "open", "unlock", "activate", "light", "cut"],
    "inspect": ["read", "look", "examine", "see", "view", "observe", "glance"],
    "quit": ["terminate", "abandon"],
    "run": ["exit", "leave", "stop", "end", "run", "flee", "es"],
    "help": ["assist", "aid", "guide", "support", "advise"],
    "inventory": ["items", "pack", "belongings", "gear", "stuff"]
}

# Valid directions and nouns
DIRECTIONS = ["north", "south", "east", "west", "up", "down"]
NOUNS = ["key", "torch", "door", "scroll", "urn", "statue", "mirror"]


def parse_input(user_input):
    pattern = r'^\s*(\w+)(?:\s+(?:the\s+)?(\w+))?\s*$'
    match = re.match(pattern, user_input.strip().lower())
    if not match:
        return None, None
    verb, noun = match.groups()
    return verb, noun


def normalize_verb(verb):
    for base_verb, synonyms in VERBS.items():
        if verb in synonyms or verb == base_verb:
            return base_verb
    return None


def parse_command(user_input):
    verb, noun = parse_input(user_input)
    if not verb:
        return None, None
    base_verb = normalize_verb(verb)
    if not base_verb:
        return None, None
    if base_verb == "go" and noun in DIRECTIONS:
        return "go", noun
    if noun and noun in NOUNS:
        return base_verb, noun
    return base_verb, None


class Game:
    def __init__(self, data):
        self.rooms = {int(k): v for k, v in data['rooms'].items()}
        self.inventory = data['starting_inventory']
        self.health = data['health']
        self.achievements = []
        self.current_room = 0
        self.collected_items = []

    def display_inventory(self):
        print("\nYour Inventory:")
        for item, info in self.inventory.items():
            print(f"- {item}: {info['description']}")

    def enter_room(self, room_id):
        room = self.rooms.get(room_id)
        if not room:
            print("That room doesn't exist.")
            return
        print(f"\n--- Room {room_id}: {room['name']} ---")
        print(room['description'])
        if room['critical_item'] and room['critical_item'] not in self.collected_items:
            print(f"You found a critical item: {room['critical_item']}!")
            self.collected_items.append(room['critical_item'])

    def handle_command(self, verb, noun):
        if verb in ["quit"]:
            print("Thanks for playing!")
            exit()
        if verb == "inventory":
            self.display_inventory()

        room = self.rooms[self.current_room]
        interactions = room.get("interactions", [])

        for action in interactions:
            if action["command"] == verb:
                print(f"\n{action['result']}")

                if action.get("game_over"):
                    print("\nGame Over.")
                    exit()

                if "next_room" in action:
                    self.current_room = action["next_room"]

                return  

        if verb == "help":
            print("\nYou can try commands like:")
            print("- go [direction/next]")
            print("- take [item]")
            print("- use [item]")
            print("- inspect [item]")
            print("- inventory")
            print("- quit")
        else:
            print("That command isn't recognized.")

    def check_game_end(self):
        if self.current_room == 6:
            required = [
                "Bronze Key", "Obsidian Mirror", "Golden Ankh",
                "Scales of Ma’at", "Sacred Flame"
            ]
            if all(item in self.collected_items for item in required):
                print("\nYou place the Key, Mirror, Ankh, Scales, and Flame into the slots.")
                print("The scarab’s wings unfold, and sunlight reveals the exit.")
                print("Achievement Unlocked: Heir of Djoser")
                self.achievements.append("Heir of Djoser")
            else:
                print("\nThe Golden Scarab glows red. A sandstorm engulfs you, and the pyramid collapses.")
                print("Game Over.")
            exit()

    def run(self):
        while True:
            self.enter_room(self.current_room)
            self.display_inventory()
            user_input = input("\n> ")
            verb, noun = parse_command(user_input)
            if not verb:
                print("I don't understand that.")
                continue
            self.handle_command(verb, noun)
            self.check_game_end()


def load_game(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return Game(data)


if __name__ == "__main__":
    game = load_game('game_data.json')
    game.run()
