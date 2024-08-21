# 3/14/23
# CSU ACM Chapter
# Tube Game v1.0

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
        
    def get_variety_count(self):
        '''Gets the number of types of marbles in the tube.'''
        marble_set = set(self._stack)
        return len(marble_set)
    
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
            removed_marble = self._stack.pop()
        
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


class ansicolors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m' # orange on some systems
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'


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
                result += "|"
                if tube.get_marble_color(working_height) == "R":
                    result += ansicolors.RED
                if tube.get_marble_color(working_height) == "G":
                    result += ansicolors.GREEN
                if tube.get_marble_color(working_height) == "B":
                    result += ansicolors.BLUE
                if tube.get_marble_color(working_height) == "Y":
                    result += ansicolors.YELLOW
                if tube.get_marble_color(working_height) == "P":
                    result += ansicolors.MAGENTA 
                result += tube.get_marble_color(working_height) + "\033[0m|"
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

# Challenge: add a "new game" command

# The list a default colors when creating a simple game (call start_simple_game)
list_of_color = ["R", "G", "B", "Y", "P", "O"]

# The number of moves performed during the shuffle during a new game
random_iterations = 1000

class GameManager:
    
    def __init__(self):
        print("Welcome to the game!")
        self.is_playing = True
        self.tubes = []
        self.score = 0
        self.start_simple_game(3)
        
    def start_simple_game(self, number_of_tubes):
        tube_parameters = []
        maximum_tubes_count = len(list_of_color)
        
        for tube_index in range(min(number_of_tubes, maximum_tubes_count)):
            tube_parameters.append( (6, 4, list_of_color[tube_index]) )
            
        self.start_new_game(tube_parameters)
    
    # tube_parameters is a list of objects of the following form (tube capacity, initial marble count, color string)
    def start_new_game(self, tube_parameters, initial_score=10):
    
        # Inform the user started a game
        print("The game has started!")
        
        self.is_playing = True
        self.tubes = []
        self.score = initial_score
        
        # Populate the tubes list with new tubes
        for tube_characteristics in tube_parameters:
            tube_capacity = tube_characteristics[0]
            initial_marble_count = tube_characteristics[1]
            color_string = tube_characteristics[2]
            
            # Create a new tube and add it
            new_tube = Tube(tube_capacity, initial_marble_count, color_string)
            self.tubes.append(new_tube)
            
        # Shuffle the contents of the tube
        self.shuffle_tubes()
    
    def check_if_won(self):
        
        each_tube_has_unique = True
        
        # Check if each tube has at max 1 kind of marble in it
        for tube in self.tubes:
            if tube.get_variety_count() > 1:
                each_tube_has_unique = False
                break
        
        # Check if the player has won (congratulate if so)
        if each_tube_has_unique:
            print("You have won! Good job!")
            self.is_playing = False
        
        return each_tube_has_unique
        
    
    def decrease_score(self, amount=1):
        if self.is_playing:
            self.score = max(0, self.score - amount)
            
            if self.score <= 0:
                print("You have lost! You can still keeping playing the level, though.")
                
                # If you want the game to restart, you can use the following:
                # self.start_simple_game(3)
    
    def shuffle_tubes(self, shuffle_iterations=random_iterations):
        
        last_tube_index = len(self.tubes) - 1
        for _ in range(shuffle_iterations):
            from_index = random.randint(0, last_tube_index)
            to_index = random.randint(0, last_tube_index)
            self.move_marble(from_index, to_index)
            
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
        
    # NOTE: this uses the user-entered indices (off by one)
    # This attempts to move a marble
    def player_requests_move(self, from_index, to_index):
        
        can_move = True
        out_of_range = False
        last_tube_index = len(self.tubes)
        
        if not self.is_playing:
            print("You already won.")
            can_move = False
        
        if from_index not in range(1, last_tube_index+1):
            print(f"The first index ({from_index}) is not valid!")
            can_move = False
            out_of_range = True
                
        if to_index not in range(1, last_tube_index+1):
            print(f"The second index ({to_index}) is not valid!")
            can_move = False
            out_of_range = True
        
        if from_index == to_index:
            print(f"The indices (both {from_index}) must be different!")
            can_move = False
        
        if can_move:
            did_move = self.move_marble(from_index - 1, to_index - 1)
            if did_move:
                self.check_if_won()
                self.decrease_score()
            else:
                print("You cannot do that!")
        elif out_of_range:
            print(f"The valid range is from 1 to {last_tube_index}.")
    
    def start_game(self):
        
        print("Enter a 'from -> to' command to move marbles and 'show' to show the state of the game")
        
        is_executing = True
        
        while is_executing:
            # Game loop:
            
            user_input = input("Enter your command: ")
            command = interpret_input(user_input)
            
            # Determine the command and execute the appropriate action
            if command.command_name == "Quit":
                is_executing = False
            elif command.command_name == "Show":
                self.decrease_score()
                print(make_string_from_tubes(self.tubes))
                print(f"Your score is {self.score}")
            elif command.command_name == "Move":
                from_index = command.arguments[0]
                to_index = command.arguments[1]
                self.player_requests_move(from_index, to_index)
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


