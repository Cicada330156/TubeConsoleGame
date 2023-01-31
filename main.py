


print("Welcome to the game")
print("Enter a 'from -> to' command to move marbles and 'show' to show the state of the game")

# Components : tubes, game manager, command interpreter


# The forms of the commands:
# "Source -> Sink" : for example, "1 -> 2"
# Show, which shows the state of the game


# The look we want for the output of the state of the game
# | |   | |
# |R|   | |
# |B|   | |
# |G|   |R|
# |-|   |-|


class Tube:
    pass


class GameManager:
    
    def do_something(self):
        print("The game has started!")


class Command:
    
    def __init__(self, command_name, arguments = []):
        self.command_name = command_name
        self.arguments = arguments
    
    def __str__(self):
        return "Name: " + self.command_name + ", Arguments: " + str(self.arguments)

def interpret_input(user_input):
    '''This method will take the user input provided and output a indicator of the next action the game manager should take (string).'''
    result = None
    
    if user_input.lower().strip() == "show":
        result = Command("Show")
        
    elif "->" in user_input:
        
        # Try to get the to and from locations:
        arrow_index = user_input.index("->")
        
        lhs = user_input[:arrow_index]
        lhs = lhs.strip()
        
        rhs = user_input[arrow_index + len("->"):]
        rhs = rhs.strip()
        
        # Check to see if the inputs will cast to ints
        if lhs.isnumeric() and rhs.isnumeric():
            lhs_int = int(lhs)
            rhs_int = int(rhs)
            result = Command("Move", [lhs_int, rhs_int])
        else:
            result = Command("Invalid")
        
    else:
        result = Command("Invalid")
        
    return result
    

game_manager = GameManager()
game_manager.do_something()

user_input = input("Input something: ")
command_result = interpret_input(user_input)
print(command_result)
