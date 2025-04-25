from game_loader import GameLoader
from game_state import GameState
import re


# Valid verbs and their synonyms
VERBS = {
    "go": ["move", "walk", "head", "travel"],
    "take": ["grab", "pick", "steal"],
    "use": ["unlock", "open", "light", "cut"],
    "inspect": ["read", "look", "examine"],
    "quit": ["exit", "leave"]
}

# Valid directions and nouns
DIRECTIONS = ["north", "south", "east", "west", "up", "down"]
NOUNS = ["key", "torch", "door", "scroll", "urn", "statue", "mirror"]

# parser
def parse_input(user_input):
    # Normalize input and match verb + noun
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
    
    # Normalize verb (e.g., "unlock" → "use")
    base_verb = normalize_verb(verb)
    if not base_verb:
        return None, None
    
    # Check if direction (e.g., "go north")
    if base_verb == "go" and noun in DIRECTIONS:
        return "go", noun
    
    # Check if valid noun (e.g., "use key")
    if noun and noun in NOUNS:
        return base_verb, noun
    
    return base_verb, None


def main():
    loader = GameLoader("game_data.json")
    game = GameState(loader)
    
    print(f"You are in {game.current_room.name}")
    print(game.current_room.description)
    
    while True:
        command = input("> ")
        verb, noun = parse_command(command)  # From Step 2
        
        
        if verb == "quit":
            break
        elif verb == "go":
            if game.move_to_room(noun):
                print(f"Moved to {game.current_room.name}")
            else:
                print("You can't go that way.")
        
        elif verb == "take":
            item = next((i for i in game.current_room.items if i.id == noun), None)
            if item and item.takeable:
                game.inventory.append(item)
                game.current_room.items.remove(item)
                print(f"You took the {item.name}")
        else:
            print("I don't understand that.")