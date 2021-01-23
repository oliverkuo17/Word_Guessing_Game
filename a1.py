from a1_support import *

# Fill these in with your details
__author__ = "{{Yi-chi Kuo}} ({{45257908}})"
__email__ = "yichi.kuo@uqconnect.edu.au"
__date__ = "04092020"


# Write your code here (i.e. functions)
def select_word_at_random(word_select):
    """
    Returns a string randomly selected from
    WORDS FIXED.txt or WORDS ARBITRARY.txt
    based on the difficulty selected

    Parameters:
        word_select (str): The difficulty selected

    Returns:
        word (str): The word selected to be guessed
    """

    if word_select in ('FIXED', 'ARBITRARY'):
        word = load_words(word_select)[random_index(load_words(word_select))]
        return word

    return None

def create_guess_line(guess_no, word_length):
    """
    Returns the string representing the display
    corresponding to the guess number.

    Parameters:
        guess_no (int): The number of the guess
        word_length (int): The length of the word

    Returns:
        guess_line (str): The string that shows information of the guess
    """

    # mark reprensents which part of the word is being guessed
    # "-" means the letter is not being guessed
    # "*" means the letter is being guessed
    # Append the list in accordance with the word_length
    mark = []
    mark += ["-"] * word_length

    # Get the range of the subword to be guessed
    # from GUESS_INDEX_TUPLE depends on word_length and guess_no
    # then replace "-" with "*" in mark list
    for idx in range(
        GUESS_INDEX_TUPLE[word_length - 6][guess_no - 1][0]-1,
        GUESS_INDEX_TUPLE[word_length - 6][guess_no - 1][1]
        ):
        mark[idx + 1] = "*"

    # Create the guess line based on guess_no, word_length and mark
    # Loop through the the range of word_length to append the guess_line
    guess_line = f"Guess {guess_no}" + WALL_VERTICAL
    for num in range(word_length):
        guess_line += f" {mark[num]} " + WALL_VERTICAL

    return guess_line

def compute_value_for_guess(word, start_index, end_index, guess):
    """
    Compute the score for each guess based on the rules.
    Each vowel guessed in the correct position gets 14 points.
    Each consonant guessed in the correct position gets 12 points.
    Each letter guessed correctly but in the wrong position gets 5 points.

    Parameters:
        word (str): The word selected to be guessed
        start_index (int): Start index to decide the substring to be guessed
        end_index (int): End index to decide the substring to be guessed
        guess (str): The guess made by players

    Returns:
        score (int): The points obtained from the guess
    """

    score = 0

    # Use for loop to get the index of each letter being guessed
    for idx in range(start_index, end_index+1):

        # Each letter guessed
        guess_letter = guess[idx - start_index]

        # Check if the letter guessed is correct
        # and in the same position of the word
        if guess_letter == word[idx]:

            # Vowel guessed in the correct position
            if guess_letter in VOWELS:
                score += 14

            # Consonant guessed in the correct position
            elif guess_letter in CONSONANTS:
                score += 12

        # Letter guessed correctly but in the wrong position
        elif guess_letter in word[start_index: end_index+1]:
            score += 5

        else:
            score += 0

    return score


def display_guess_matrix(guess_no, word_length, scores):
    """
    Displays the progress of the game.

    Parameters:
        guess_no (str): An integer representing how many guesses has made
        word_length (int): The length of the word
        scores (tuple<int>): A tuple containing all previous scores

    Prints:
        (str): The progress of the game
    """

    # Create the top line of the matrix
    # Append the top line based on the word_length
    matrix_top = (" "*7 + WALL_VERTICAL)
    for num in range(1, word_length + 1):
        matrix_top += f" {num} " + WALL_VERTICAL

    # Create breaking line
    breaking_line = (WALL_HORIZONTAL*(33 + (word_length - 6)*4))

    print(matrix_top)
    print(breaking_line)

    # line variable is used to identify whether the guess is answered or not
    # Points should be printed only if the guess has been answered
    line = 1
    while line < guess_no:
        print(create_guess_line(line, word_length) + f"   {scores[line-1]} Points")
        print(breaking_line)
        line += 1

    print(create_guess_line(line, word_length))
    print(breaking_line)

def main():
    """
    Handles top-level interaction with user.
    """
    # Write the code for your main function here
    # Greeting and promt user to enter the action
    print(WELCOME)
    action = input(INPUT_ACTION)

    # Checking the validity of the action
    while action not in ("s","h","q"):
        print(INVALID)
        action = input(INPUT_ACTION)

    # Commence the game if "s" or "h" are entered
    if action in ("s", "h"):
        if action == "h":
            print(HELP)

        # Promt users to select the difficulty
        word_select = ""
        while word_select not in ("FIXED", "ARBITRARY"):
            word_select = input("""Do you want a 'FIXED' or 'ARBITRARY' length word?: """)

        # Select the word to be guessed based on the word_select
        word = select_word_at_random(word_select)

        print("Now try and guess the word, step by step!!")

        word_length = len(word) # Length of the word being guessed
        guess_no = 1 # Guess number
        scores = () # Tuple used to store the score from each guess

        # Guessing procedure
        while guess_no < word_length:
            guess = ""
            # The range of which part of the word being guessed
            start_index = GUESS_INDEX_TUPLE[word_length - 6][guess_no - 1][0]
            end_index = GUESS_INDEX_TUPLE[word_length - 6][guess_no - 1][1]

            # Display the matrix for user
            # Information includes which part of the word is being guessed,
            # word length, scores from prior guessing
            display_guess_matrix(guess_no, word_length, scores)

            # If the length of guess does not meet the expectation
            # Promt user to guess again
            while len(guess) != end_index - start_index + 1:
                guess = input(f"Now enter Guess {guess_no}: ")

            # Calculate the score from the guess and store it into scores
            score = compute_value_for_guess(word, start_index, end_index, guess)
            scores += (score,)
            guess_no += 1

        # Final guess
        if guess_no == word_length:
            display_guess_matrix(guess_no, word_length, scores)
            final_guess = input("Now enter your final guess. i.e. guess the whole word: ")

            if final_guess == word:
                print("You have guessed the word correctly. Congratulations.")

            else:
                print(f'Your guess was wrong. The correct word was "{word}"')

    # End the game if "q" is entered
    elif action == "q":
        return None

if __name__ == "__main__":
    main()
