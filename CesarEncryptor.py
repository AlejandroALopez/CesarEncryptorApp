import string
import sys 


def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    
    in_file = open(file_name, 'r')    
    line = in_file.readline()
    word_list = line.split()
    
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    
    return word_list


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the loaded word list.
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

WORDLIST_FILENAME = 'words.txt'

class Message(object):

    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
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
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
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
        abc = string.ascii_lowercase
        abc2 = string.ascii_uppercase
        self.shift = shift
        self.aDict = {}

        for e in range (0,26):
          try:
           self.aDict[abc[e]] = abc[e+self.shift]

          except IndexError:
           self.aDict[abc[e]] = abc[e-(26-self.shift)]

        for e in range (0,26):
          try:
           self.aDict[abc2[e]] = abc2[e+self.shift]

          except IndexError:
           self.aDict[abc2[e]] = abc2[e-(26-self.shift)]
     
        return self.aDict

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
        self.encryptedMessage = ""
        abc = string.ascii_lowercase
        abc2 = string.ascii_uppercase
        self.shift = shift
        self.aDict = {}

        for e in range (0,26):
          try:
           self.aDict[abc[e]] = abc[e+self.shift]

          except IndexError:
           self.aDict[abc[e]] = abc[e-(26-self.shift)]

        for e in range (0,26):
          try:
           self.aDict[abc2[e]] = abc2[e+self.shift]

          except IndexError:
           self.aDict[abc2[e]] = abc2[e-(26-self.shift)]     
           
        for e in self.message_text:
            try:
               self.encryptedMessage += self.aDict[e]
               
            except KeyError:
                self.encryptedMessage += e
        
        return self.encryptedMessage

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
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self,shift)
        self.message_text_encrypted = Message.apply_shift(self,shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift


    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encrypting_dict = Message.build_shift_dict(self,shift)
        self.message_text_encrypted = Message.apply_shift(self,shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self, displayAll):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        counter = 0
        counter2 = 0
        s = 0
        bestIndex = 1
        while s < 26:
           decoded = Message.apply_shift(self, 26-s)
           if displayAll == "yes":
               print("Index: ",s,", Message: ",decoded)
           decodedList = decoded.split(" ")
           for e in decodedList:
              if e in self.valid_words:
                  counter2 += 1
           if counter2 > counter:
                  counter = counter2
                  bestIndex = 26-s
           s += 1
        return (26-bestIndex,Message.apply_shift(self, bestIndex))
   
#User Interface#         

print("Welcome to the Cesar Encryptor and Decipher App!")
print("------------------------------------------------")
print("With this program you can encrypt messages in Cesar Encryption using a personalized Cesar Index, or decipher Cesar encrypted messages encrypted in any Index. Below are some important clarifications:")
print("")
print("1. The Cesar Encryption consists in changing every letter in a message based on their index in the alphabet, increasing the index position of the letter to get another letter.")
print("")
print("2. This needs a Cesar Index, which increases the index of every letter by a specific amount. This index may be from 0 to 25. The index 26 may be equal to index 0.")
print("")
print("3. For example: With index 1, A becomes B, C becomes D, and so on. With index 3, A becomes D and C becomes F.")
print("")
print("4. If a letter increases its index passing the index of Z (26), it goes back to the beginning. For example, with Index 1, Z becomes A")
print("")


election = "n"
while election != "e" or "d":
   election = input("Press 'e' to encrypt a message, 'd' to decipher an encrypted message, or 'q' to quit: ")

   if election == "e":
     inputMessageEncrypt = str(input("Write the message you want to encrypt: "))
     inputIndexEncrypt = int(input("Now write the Cesar Index you want: "))

     plaintext = PlaintextMessage(inputMessageEncrypt, inputIndexEncrypt)
     print("Message: ",inputMessageEncrypt, ", Cesar Index: ",inputIndexEncrypt)
     print('Encrypted message:', plaintext.get_message_text_encrypted())

   if election == "d":
     inputMessageDecipher = str(input("Write the message you want to decipher: "))

     ciphertext = CiphertextMessage(inputMessageDecipher)
     print("Decoded message: ", ciphertext.decrypt_message(""))
     print("------------------------------------------------")
     agreement = "x"
     while agreement != "y" or "n": 
        agreement = input("Do you agree with this answer?: Press 'y' for Yes or 'n' for No: ")
        if agreement == "y":
            print("Great!")
            print("------------------------------------------------")
            break
        if agreement == "n":
            print("Then review the following deciphers with different Cesar Indexes:")
            ciphertext.decrypt_message("yes")
            print("------------------------------------------------")
            break

   if election == "q":
      print("------------------------------------------------")
      sys.exit("Thanks for using the Cesar Encryptor and Decipher App!")
   
   print("------------------------------------------------")
   election = "n"




