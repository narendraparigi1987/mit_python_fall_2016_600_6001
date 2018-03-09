# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    result = True
    for letter in secret_word:
      if letter not in letters_guessed:
        result = False
    return result

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_dic = {}
    for i in range(len(secret_word)):
      secret_dic[i] = '_'
    
    for letter in letters_guessed:
      for j in range(len(secret_word)):
        if letter == secret_word[j]:
          secret_dic[j] = letter
    return "".join(secret_dic.values())

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase
    for c in letters_guessed:
      if c in available_letters:
        available_letters = available_letters.replace(c,'')

    return available_letters

def create_guess_set(guess,guess_set,iter,w_iter,secret_word,check):
  if guess not in guess_set:
    guess_set.add(guess)
  else:
    if w_iter < 3:
      w_iter+=1
      print 'Oops! That is already a guessed letter. You have %s warnings left:%s'%(3-w_iter,get_guessed_word(secret_word,guess_set))
      check = False
    else:
      iter+=1
      print 'Oops! That is already a guessed letter. You have %s warnings left so you lose one guess:%s'%(0,get_guessed_word(secret_word,guess_set))
      check = False  
  return (guess_set,iter,w_iter,check)

def check_valid_alpha(guess_set,iter,w_iter,secret_word,check):
  if w_iter < 3:
    w_iter+=1
    print 'Oops! That is not a valid letter. You have %s warnings left:%s'%(3-w_iter,get_guessed_word(secret_word,guess_set))
    check = False
  else:
    iter+=1
    print 'Oops! That is not a valid letter. You have %s warnings left so you lose one guess:%s'%(0,get_guessed_word(secret_word,guess_set))
    check = False
  return (iter,w_iter,check)

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print 'Welcome to hangman!!!'
    print 'I am thinking of a word that is {} letters long.'.format(len(secret_word))
    #variable assignments
    guess_set = set([])
    iter = 0
    w_iter = 0
    #looping with 6 chances, incase of correct guess user is not penalized, incase of incorrect guess user is penalized
    while iter < 6:
      print '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _'
      print 'You have {} guesses left'.format(6-iter)
      print 'You have {} warnings left'.format(3-w_iter)
      #user input
      print 'Available letters: {}'.format(get_available_letters(guess_set))
      guess = raw_input('Please guess a letter: ')
      guess = guess.lower()
      check = True
      vowels = ['a','e','i','o','u'] 
      #checking if input is alphabet or not
      if guess.isalpha():
      #creating set based on user input, handling already guessed letters
        (guess_set,iter,w_iter,check) = create_guess_set(guess,guess_set,iter,w_iter,secret_word,check)
        #checking word based on guessed letters matches with secret_word
        if guess in secret_word and check == True:
          print 'Good guess {}'.format(get_guessed_word(secret_word,guess_set))
          if is_word_guessed(secret_word,guess_set):
            total_score = (6-iter) * len(set(secret_word))
            print 'Congrats, Game is complete!!! with score {}'.format(total_score)
            break
        elif check == True:
          print 'Oops! That letter is not in my word: {}'.format(get_guessed_word(secret_word,guess_set))
          if guess in vowels:
            iter+=2
          else:
            iter+=1
      else:
        #Handling invalid scenarios
        (iter,w_iter,check) = check_valid_alpha(guess_set,iter,w_iter,secret_word,check)
    
    #check for failed scenario
    if iter >= 6:
        print 'Sorry, you ran out of guesses. The word was {}'.format(secret_word)
    
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    if len(my_word) == len(other_word):
      result = True
      for i in range(len(my_word)):
        if (my_word[i] != other_word[i] and my_word[i] != '_') or (my_word[i] == '_' and other_word[i] in my_word):
          result = False
    else:
      result = False
    
    return result



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    result = ''
    for word in wordlist:
      if match_with_gaps(my_word,word):
        result = result+' '+word
    if result == '':
      result = 'No matches found!!!'
    else:
      result = result
  
    return result

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print 'Welcome to hangman!!!'
    print 'I am thinking of a word that is {} letters long.'.format(len(secret_word))
    #variable assignments
    guess_set = set([])
    iter = 0
    w_iter = 0
    #looping with 6 chances, incase of correct guess user is not penalized, incase of incorrect guess user is penalized
    while iter < 6:
      print '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _'
      print 'You have {} guesses left'.format(6-iter)
      print 'You have {} warnings left'.format(3-w_iter)
      #user input
      print 'Available letters: {}'.format(get_available_letters(guess_set))
      guess = raw_input('Please guess a letter: ')
      check = True
      vowels = ['a','e','i','o','u'] 
      #checking if input is alphabet or not
      if guess != '*':
        guess = guess.lower()
        if guess.isalpha():
      #creating set based on user input, handling already guessed letters
          (guess_set,iter,w_iter,check) = create_guess_set(guess,guess_set,iter,w_iter,secret_word,check)
        #checking word based on guessed letters matches with secret_word
          if guess in secret_word and check == True:
            print 'Good guess {}'.format(get_guessed_word(secret_word,guess_set))
            if is_word_guessed(secret_word,guess_set):
              total_score = (6-iter) * len(set(secret_word))
              print 'Congrats, Game is complete!!! with score {}'.format(total_score)
              break
          elif check == True:
            print 'Oops! That letter is not in my word: {}'.format(get_guessed_word(secret_word,guess_set))
            if guess in vowels:
              iter+=2
            else:
              iter+=1
        else:
        #Handling invalid scenarios
          (iter,w_iter,check) = check_valid_alpha(guess_set,iter,w_iter,secret_word,check)
      elif guess == '*':
        print show_possible_matches(get_guessed_word(secret_word,guess_set).strip())
    #check for failed scenario
    if iter >= 6:
        print 'Sorry, you ran out of guesses. The word was {}'.format(secret_word)

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # pass
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)
###############
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
    #hangman_with_hints('tact')