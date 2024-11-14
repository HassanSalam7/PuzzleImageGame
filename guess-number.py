import random

def number_guessing_game():
    print("Think of a number between 1 and 100, and I'll try to guess it!")
    low = 1
    high = 100
    attempts = 0
    
    while True:
        # The AI guesses the midpoint of the current range
        guess = (low + high) // 2
        attempts += 1
        print(f"My guess is {guess}. Is it too high (H), too low (L), or correct (C)?")
        
        # Getting feedback from the player
        feedback = input("Enter H, L, or C: ").upper()
        
        if feedback == 'C':
            print(f"I guessed it! Your number is {guess}. It took me {attempts} attempts.")
            break
        elif feedback == 'H':
            high = guess - 1  # Reduce the range by setting a new high limit
        elif feedback == 'L':
            low = guess + 1   # Reduce the range by setting a new low limit
        else:
            print("Invalid input. Please enter 'H', 'L', or 'C'.")
    
    print("Thanks for playing!")

# Run the game
number_guessing_game()
