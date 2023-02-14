
# 2/14/23
# CSU ACM Chapter
# Tube Game v0.2

# Components : tubes, game manager, command interpreter


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
    
    # return max( [tube.get_capacity() for tube in tube_list] )
    
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


class GameManager:
    
    def do_something(self):
        print("The game has started!")





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


print("Welcome to the game")
print("Enter a 'from -> to' command to move marbles and 'show' to show the state of the game")


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


tube_a = Tube(5, 4, "R")
tube_b = Tube(7, 7, "G")
tube_c = Tube(6, 3, "B")
tube_d = Tube(6, 3, "Y")

tube_list = [tube_a, tube_b, tube_c, tube_d]

description = make_string_from_tubes(tube_list)

print(description)
