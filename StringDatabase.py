import random


class StringDatabase:
    def __init__(self):
        self.word_list = None
        self.file_path = "four_letters.txt"

    def load_list(self):
        with open(self.file_path, "r") as file:
            self.word_list = [word.strip() for line in file for word in line.split()]
        return

    def generate_word(self):
        random_index = random.randint(0, len(self.word_list) - 1)
        return self.word_list[random_index]
#print(len(word_list))
#print(word_list)
