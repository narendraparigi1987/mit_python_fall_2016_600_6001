# Problem Set 4B
# Name: <Narendra parigi>
# Collaborators:
# Time Spent: x:xx

import string
import copy

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        result = self.valid_words[:]
        return result

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        #assignments
        shift = shift
        dict_all_letters = {}
        dict_lower_letters = {}
        dict_upper_letters = {}
        
        #dictionary for all letters created
        for c in string.ascii_letters:
            dict_all_letters[c] = c
        
        #dictionary for lowercase letters created
        l=0
        for c in string.ascii_lowercase:
            l+=1
            dict_lower_letters[c] = l
        
        #dictionary for uppercase letters created
        u=0
        for c in string.ascii_uppercase:
            u+=1
            dict_upper_letters[c] = u
        
        #doing shift, copy dictionary
        result_dict_all_letters = dict_all_letters.copy()
        #loop all key, values from dict_all_letters
        for key,value in result_dict_all_letters.items():    
            #if key is lowercase
            if key in dict_lower_letters:
                #find index of shift alphabet
                if (dict_lower_letters[key]+shift)%26 ==0:
                    index = 26
                else:
                    index = (dict_lower_letters[key]+shift)%26
                #assign new value to based on shift
                dict_all_letters[key] = list(dict_lower_letters.keys())[list(dict_lower_letters.values()).index(index)]
            #if key is uppercase
            if key in dict_upper_letters:
                #find index of shift alphabet            
                if (dict_upper_letters[key]+shift)%26==0:
                    index = 26
                else:
                    index = (dict_upper_letters[key]+shift)%26
                #assign new value to based on shift
                dict_all_letters[key] = list(dict_upper_letters.keys())[list(dict_upper_letters.values()).index(index)]
        
        return dict_all_letters

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        #get message text for object
        string = self.get_message_text()
        #variable assignment
        shift = shift
        #build shift dic for a object
        dict_all_letters = self.build_shift_dict(shift)
        #result
        result = ''
        #loop through all chars in string 
        #and if char is alpha then shift
        #else display AS IS
        for c in string:
            if c.isalpha():
                result = result+dict_all_letters[c]
            else:
                result = result + c
        return result

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self,text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        copy_encryption_dict = self.encryption_dict[:]
        
        return copy_encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self,text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        #encrypted message
        encrypted_string = self.get_message_text()
        #list words
        valid_words = self.get_valid_words()
        i = 0
        result_dict = {}
        #loop from 0 to 26
        while i <= 26:
            counter = 0
            #decrypt message
            decrypt_message = self.apply_shift(i)
            #go through all words
            for word in decrypt_message.split(' '):
                #check for valid words
                if is_word(valid_words,word):
                    #count valid words
                    counter+=1
            result_dict[i] = counter
            i+=1
        #check which value of i is with maximum valid words
        result_tuple = max([(value,key) for key , value in list(result_dict.items())])
        #create a variable shift
        result_shift = result_tuple[1]
        #decrypt message
        decrypt_message = self.apply_shift(result_shift)
        #return shift and decrypt message
        return (result_shift,decrypt_message)

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    print ('________________________________________________')
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # #Example test case (CiphertextMessage)
    print ('________________________________________________')
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    print ('________________________________________________')
    plaintext_2 = PlaintextMessage('Good!!!', 5)
    print('Actual Output:', plaintext_2.get_message_text_encrypted())

    print ('________________________________________________')
    ciphertext_2 = CiphertextMessage('amhvwqoz')
    print('Actual Output:', ciphertext_2.decrypt_message())
    
    #calling funcation to get encrypted message
    story_string = get_story_string()
    print ('________________________________________________')
    ciphertext_3 = CiphertextMessage(story_string)
    print ('Actual Output:', ciphertext_3.decrypt_message())