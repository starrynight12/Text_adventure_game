from game_loader import GameLoader
from game_state import GameState

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