import random

password = "undecoded"

def function_guessing():
    function = functionSetter()
    printInfo(function)
    print(function)
    function_guess = 0
    for i in range(6, 0, -1):
        function_guess = int(input("Guess a number: "))
        if function_guess > function:
            print("Lower")
        elif function_guess < function:
            print("Higher")
        else:
            return True
        print("You have", i, "guesses left")

    return False


def decode():
    # Allows for 2 attemps in case the user mistypes 
    for j in range(2):
        guess = input("Guess the password: ")
        # TODO Remove this
        if guess == "":
            quit()

        if guess == password:
            print("CORRECT")
            break
        # Needs to make sure the user knows they have one more try or if they have just failed
        else:
            if j == 0:
                print("One more try!")
            else:
                print("FAIL")


def functionSetter():
    '''Returns the randomly generated number to act as the function'''
    # Needed to have 2 seperate random number generators for negative and positive numbers as it is not continuous
    # And also needed to randomly choose if the function is negative or positive
    negpos = random.randint(0, 1)
    if negpos:
        return random.randint(3, 23)
    else:
        return random.randint(-23, -3)


def encode(function):
    '''Returns a string that seems like a jumble of random letter'''
    # Creating a list with the corresponding place in the alphabet of each letter in the word
    nums_of_chars = []
    for char in password:
        num = ord(char) - 96
        nums_of_chars.append(num)

    # Creates a list, where each item is a letter in the now encoded word
    encoded_list = []
    for item in nums_of_chars:
        # This ensures that when going above 26, it goes back to 1 again
        # TODO Make sure this can also work when going into negative numbers
        num = (item + function) % 26
        if num == 0:
            num = 26
        encoded_list.append(chr(num + 96))

    # converts the list of the encoded word to a string
    encoded = ""
    for item in encoded_list:
        encoded += item

    return encoded


def printInfo(function):
    '''
    Information is printed, the word is also encoded here as each time the user fails to decode the word 
    it will change and be printed here
    '''
    print("Figure out the function to decode the password")
    encoded_word = encode(function)
    print("This is the encoded password: ", encoded_word)

def decoder_puzzle():
    '''
    Runs the decoding loop, currently allowing for an infinite amount of trys to guess the function
    '''
    correct = False
    while not correct:
        correct = function_guessing()

    decode()


