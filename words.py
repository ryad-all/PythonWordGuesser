import random
import sys
from Guess import *
from StringDatabase import *



db = StringDatabase()
db.load_list()
word = db.generate_word()
if (len(sys.argv) > 1 and sys.argv[1] == "test"):
    guess = Guess(word, True)
else:
    guess = Guess(word, False)
flag = True

while(flag):
    flag = guess.menu_option(flag)
    




