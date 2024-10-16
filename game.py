#!/usr/bin/python3

from decoder import *
from gameparser import *
from items import *
from map import rooms
from player import *
import lightswitches


def check_complete(room):
    if room == rooms["Reception"]:
        if len(room["items"]) >= 6:
            print("YOU HAVE COMPLETED THE GAME, CONGRATULATIONS!!!")
            return True
    return False


def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:
    """
    items_string = ""
    for item in items:
        items_string = items_string + item["name"] + ", "
        # items_string = (
        #     items_string + item["name"] + " (" + str(item["mass"]) + "g)" + ", "
        # )

    items_string = items_string[:-2]
    return items_string


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:
    """
    items_list = room["items"]
    items_string = list_of_items(items_list)
    if items_string == "":
        pass
    else:
        print("There is " + items_string + " here.")
        print("")


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:
    """
    items_string = list_of_items(inventory)

    if items_string == "":
        print("You have nothing")
    else:
        print("You have " + items_string + ".")
        # print(
        #     "Your inventory's weight is "
        #     + str(inventory_weight)
        #     + "g out of "
        #     + str(inventory_max_weight)
        #     + "g."
        # )
    print("")


def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:
    """
    # Display room name
    print()
    print(room["name"].upper())
    print()
    # Display room description
    print(room["description"])
    print()
    # Displays items in the room
    print_room_items(room)


def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:
    """
    return rooms[exits[direction]]["name"]


def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.
    """
    print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."

    For example, the menu of actions available at the Reception may look like this:

    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to MJ and Simon's room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?
    """

    print("You can:")
    # Iterate over available exits
    for direction in exits:
        # Print the exit name and where it leads to
        print_exit(direction, exit_leads_to(exits, direction))

    # Iterate over all items in the room
    for item in room_items:
        # Print the item id and the item name with formatting
        print("TAKE " + item["id"].upper() + " to take " + item["name"] + ".")

    # Iterate over all items in the player's inventory
    for item in inv_items:
        print("DROP " + item["id"].upper() + " to drop your " + item["id"] + ".")

    if puzzle_check():
        print("ATTEMPT", current_room["puzzle"], "Puzzle")

    print("What do you want to do?")


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:
    """
    return chosen_exit in exits


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room
    if direction in current_room["exits"]:
        current_room = move(current_room["exits"], direction)
    else:
        print("You cannot go there.")


def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """
    global inventory_weight
    # loops through the items in the room so they can be checked against
    for item in current_room["items"]:
        if item_id == item["id"]:
            inventory_weight += item["mass"]
            if inventory_weight > inventory_max_weight:
                inventory_weight -= item["mass"]
                print("You cannot take that, it is too heavy")
                return None
            # adds the item to the inventory and removes it from the room
            inventory.append(item)
            current_room["items"].remove(item)
            # inventory_weight
            return None

    print("You cannot take that")


def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    global inventory_weight

    for item in inventory:
        if item_id == item["id"]:
            inventory_weight -= item["mass"]
            # adds the item to the room and removes it from the inventory
            inventory.remove(item)
            current_room["items"].append(item)

            return None

    print("You cannot drop that")

def execute_puzzle():
    if current_room["puzzle"] == "Decoder":
        decoder_puzzle()
    elif current_room["puzzle"] == "Lights":
        

def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.
    """

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")
    
    elif command[0] == "attempt":
        if len(command) > 1:
            execute_puzzle()

    else:
        print("This makes no sense.")

def puzzle_check():
    if "puzzle_complete" in current_room:
        return True

def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.
    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")
    if user_input == "":
        quit()
    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:
    """

    # Next room to go to
    return rooms[exits[direction]]


# This is the entry point of our program
def main():
    print(
        "YOUR TASK IS TO FIND ALL OF THE ITEMS AND BRING THEM BACK TO RECEPTION. GOOD LUCK!"
    )
    complete = False
    # Main game loop
    while not complete:
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)
        #puzzle_check(current_room)
        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)
        complete = check_complete(current_room)


# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    main()
