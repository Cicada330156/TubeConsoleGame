# 2/21/23
# CSU ACM Chapter
# Tube Game v0.3

# Components : tubes, game manager, command interpreter

import random

# The forms of the commands:
# "Source -> Sink" : for example, "1 -> 2"
# Show, which shows the state of the game


# The look we want for the output of the state of the game
# | |   | |
# |G|   |B|
# |G|   |B|
# |G|   |B|
# |-|   |-|



# ----------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------  Tubes ------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

class Tube:
    
    def __init__(self, capacity, initial_marble_count, marble_description):
        
        self._stack = []
        self._capacity = capacity
        
        for _ in range(initial_marble_count):
            self.add_marble(marble_description)
    
    def get_capacity(self):
        '''Getter for the capacity of the tube.'''
        return self._capacity
    
    def add_marble(self, marble_description):
        '''Attempt to add a marble to the top of the tube. If there is no room, the marble is not added.
        This method return the success of the addition.'''
        
        did_add = False
        
        if len(self._stack) < self._capacity:
            self._stack.append(marble_description)
            did_add = True
        
        return did_add
        
    def remove_marble(self):
        '''This method remove the top marble from the tube and returns it. If the tube is empty, return None.'''
        
        removed_marble = None
        
        if len(self._stack) != 0:
            remove_marble = self._stack.pop()
        
        return removed_marble
        
    
    def get_marble_color(self, position):
        '''Return the marble/color description at the passed position (starting at 0). If the position contains no marbles, then return a single space (" ").'''
        
        result = " "
        
        if len(self._stack) > position:
            result = self._stack[position]
        
        return result



# ----------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------  Printing ------------------------------------------------ #
# ----------------------------------------------------------------------------------------------------------- #


def get_highest_capacity(tube_list):
    
    # return max(tube.get_capacity() for tube in tube_list)
    
    running_highest = 0
    
    for tube in tube_list:
        capacity = tube.get_capacity()
        if capacity > running_highest:
            running_highest = capacity
    
    return running_highest
    
    
    

def make_string_from_tubes(tube_list):
    result = ""
    
    tallest_height = get_highest_capacity(tube_list)
    working_height = tallest_height - 1
    
    while working_height >= 0:
        
        for tube in tube_list:
            
            if tube.get_capacity() - 1 >= working_height:
                # Put in the tube's edges and the marble inside (if any)
                result += "|" + tube.get_marble_color(working_height) + "|"
            else:
                # Print a few spaces
                result += "   "
                
            # Add the spacing between the tubes
            result += "   "
                
            
        result += "\n"
        
        working_height -= 1
    
    # Add the bottoms of the tubes
    for _ in range(len(tube_list)):
        result += "|-|   "
    
    return result




# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------- Game Manager ---------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

# Create a method for creating new games
#   1. Create the tubes
#   2. Randomize the marble within the tubes
#   3. Randomize the tubes
# Add a loop that reads input, parses that input for commands
# In the loop, we want to process those commands
# Add a system for tracking points
# Create some method for detecting if the player has won
# Add a check to see if the player has lost (ran out of points)
# Maybe add a new game command


list_of_color = ["R", "G", "B", "Y", "P", "O"]
random_iterations = 200

class GameManager:
    
    def __init__(self):
        print("Welcome to the game!")
        self.is_playing = True
        self.tubes = []
        self.start_simple_game(3)
        
    def start_simple_game(self, number_of_tubes):
        tube_parameters = []
        maximum_tubes_count = len(list_of_color)
        
        for tube_index in range(min(number_of_tubes, maximum_tubes_count)):
            tube_parameters.append( (6, 4, list_of_color[tube_index]) )
            
        self.start_new_game(tube_parameters)
    
    # tube_parameters is a list of objects of the following form (tube capacity, initial marble count, color string)
    def start_new_game(self, tube_parameters):
    
        # Inform the user started a game
        print("The game has started!")
        
        self.is_playing = True
        self.tubes = []
        
        # Populate the tubes list with new tubes
        for tube_characteristics in tube_parameters:
            tube_capacity = tube_characteristics[0]
            initial_marble_count = tube_characteristics[1]
            color_string = tube_characteristics[2]
            
            # Create a new tube and add it
            new_tube = Tube(tube_capacity, initial_marble_count, color_string)
            self.tubes.append(new_tube)
            
        last_tube_index = len(tube_parameters) - 1
        for _ in range(random_iterations):
            self.move_marble(random.randint(0, last_tube_index), random.randint(0, last_tube_index))
            
    def move_marble(self, from_tube_index, to_tube_index):
    
        did_move = False
        
        from_tube = self.tubes[from_tube_index]
        from_marble = from_tube.remove_marble()
        
        # Check if there was a marble in the tube
        if from_marble is not None:
            to_tube = self.tubes[to_tube_index]
            did_add = to_tube.add_marble(from_marble)
            
            # If the to_tube cannot take the marble, we add it back to the original tube
            if did_add:
                did_move = True
            else:
                from_tube.add_marble(from_marble)
                
        return did_move
        
    
    def start_game(self):
        
        print("Welcome to the game")
        print("Enter a 'from -> to' command to move marbles and 'show' to show the state of the game")
        
        is_executing = True
        
        while is_executing:
            # Game loop:
            
            user_input = input("Enter your command: ")
            command = interpret_input(user_input)
            
            if command.command_name == "Quit":
                is_executing = False
            elif command.command_name == "Show":
                print(make_string_from_tubes(self.tubes))
            elif command.command_name == "Invalid":
                print("Sorry, but that is not a valid command.")
            else:
                pass
        
        print("Thank you for playing!")





# ----------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Commands ------------------------------------------------ #
# ----------------------------------------------------------------------------------------------------------- #



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
        
    elif user_input.lower().strip() == "quit":
        result = Command("Quit")
        
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
    



# ----------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- Gameplay ------------------------------------------------ #
# ----------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.start_game()

# ----------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------  Testing ------------------------------------------------ #
# ----------------------------------------------------------------------------------------------------------- #




#game_manager = GameManager()
#game_manager.do_something()

#user_input = input("Input something: ")
#command_result = interpret_input(user_input)
#print(command_result)



#def check_tube_contents(tube):
#    print("-")
#    for index in range(tube.get_capacity()-1, -1, -1):
#
#        print(tube.get_marble_color(index))
#    print("-")


#test_tube = Tube(5, 3, "R")
#test_tube.add_marble("B")
#test_tube.add_marble("Y")
#test_tube.remove_marble()
#test_tube.add_marble("G")

#check_tube_contents(test_tube)


#tube_a = Tube(5, 4, "R")
#tube_b = Tube(7, 7, "G")
#tube_c = Tube(6, 3, "B")
#tube_d = Tube(6, 3, "Y")
#
#tube_list = [tube_a, tube_b, tube_c, tube_d]
#
#description = make_string_from_tubes(tube_list)
#
#print(description)
