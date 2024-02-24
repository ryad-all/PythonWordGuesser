import os
import sys
import random
from StringDatabase import *
from Game import *



class Guess:
    def __init__(self, wrd, mode):
        self.welcome_message = "+++\n+++ The Great Guessing Game\n+++\n\n"
        self.failure_word = "@@@\n@@@ FEEDBACK: bad guess\n@@@\n\n"
        self.success_word = "@@@\n@@@ FEEDBACK: great guess\n@@@\n\n"
        self.current_guess = ["-", "-", "-", "-"]
        self.options_message = "g = guess, t = tell me, l for a letter, and q to quit"
        self.options = ["g", "t", "l", "q"]
        self.selected_option = None
        self.guessed_letters = []
        self.word = wrd
        self.guessed_words = []
        self.test_mode = mode
        self.games = []
        
    def clear_screen(self):
        if os.name == 'nt':  # WINDOWS
            os.system('cls')
        else:  # UNIX
            os.system('clear')
        return

    def menu_option(self, flag):
        print(self.welcome_message)
        if (self.test_mode):
            print(f'Current word: {self.word}')
        print("Current Guess: " + "".join(self.current_guess))
        print("Letters guessed: " + " ".join(self.guessed_letters))

        print("\n" + self.options_message)
 
        a = input("\nEnter Option: ")
        flag = True
        if a in self.options:
            self.selected_option = a
        else:
            some = True
            while(some):
                x = input("Invalid option. Please re-enter: ")
                if x in self.options:
                    some = False
                    self.selected_option = x
                    break
                
        if self.selected_option == "g":
            self.handle_word()
        elif self.selected_option == "t":
            self.handle_tell_me()
        elif self.selected_option == "l":
            self.handle_letter()
        elif self.selected_option == "q":
            flag = self.handle_quit(flag)    
        
        return flag
    
    
    def handle_word(self):
        player_guess = input("Enter your guess: ")
        player_guess = player_guess.lower()
        if player_guess == self.word and player_guess not in self.guessed_words:
            print("\n" + self.success_word)
            self.save_game_guess()
            self.handle_word_found() 
        elif player_guess in self.guessed_words:
            print("\n@@@\n@@@ FEEDBACK: you already have tried that word\n@@@\n\n")
        elif len(player_guess) > 4:
            print(f'\n@@@\n@@@ FEEDBACK: "{player_guess}" is not a four letter word, try again\n@@@\n\n')
            self.press_any_key()
            self.clear_screen()
            return
        else:
            print(self.failure_word)
            self.guessed_words.append(player_guess) 
        self.press_any_key()
        return
    
    def handle_letter(self):
        guessed_letter = input("Enter a letter: ")
        guessed_letter = guessed_letter.lower()
        if len(guessed_letter) > 1:
            print(f'\n@@@\n@@@ FEEDBACK: "{guessed_letter}" is not a letter, try again\n@@@\n\n')
            self.press_any_key()
            self.clear_screen()
            return
        if guessed_letter in self.guessed_letters:
            print(f'\n@@@\n@@@ FEEDBACK: you already tried letter {guessed_letter}\n@@@\n\n')
            self.press_any_key()
            self.clear_screen()
            return
        self.guessed_letters.append(guessed_letter)
        dup_counter = 0
        for i, letter in enumerate(self.word):
            if guessed_letter == letter:
                self.current_guess[i] = guessed_letter
                dup_counter += 1
        if dup_counter > 0:
            print(f'\n@@@\n@@@ FEEDBACK: you found {dup_counter} letter(s)!\n@@@\n\n')
        else:
            print(f'\n@@@\n@@@ FEEDBACK: no match for your letter\n@@@\n\n')
        if "".join(self.current_guess) == self.word:
            self.save_game_letter_guess()
            self.handle_word_found()
        self.press_any_key()
        self.clear_screen()
        return
    
    def handle_quit(self, flag):
        self.clear_screen()
        self.print_games()
        flag = False
        return flag
    
    def handle_tell_me(self):
        print(f'\n@@@\n@@@ FEEDBACK: the word was {self.word}\n@@@\n\n')
        self.save_game_tell()
        self.handle_word_found()
        self.press_any_key()
        return

    def press_any_key(self):
        input("Press any key to continue...")
        self.clear_screen()
        return
        
    def handle_word_found(self):
        db = StringDatabase()
        db.load_list()
        self.word = db.generate_word()
        self.current_guess = ["-", "-", "-", "-"]
        self.guessed_letters = []
        self.guessed_words = []
        return
    
    
    def save_game_letter_guess(self):
        game = Game()
        #missed _letters
        missed = 0
        for letter in self.guessed_letters:
            if letter not in self.current_guess:
                missed += 1
        game.missed_letters = missed
        
        #status
        game.status = "Success" 
        
        # bad guess
        game.bad_guesses = len(self.guessed_words)
        
        #game word save
        game.game_word = self.word
        
        score_cal = 0
        for i, letter in enumerate(self.word):
            score_cal += letter_frequencies[letter]
        game.score = score_cal
        if missed > 0:
            game.score /= missed
            (game.score)
        if game.bad_guesses > 0:
            game.score *= (1-(game.bad_guesses*0.1))     

        self.games.append(game)        
        return 
        
        
    def save_game_guess(self):
        game = Game()
        
        #missed _letters
        missed = 0
        for letter in self.guessed_letters:
            if letter not in self.current_guess:
                missed += 1
        game.missed_letters = missed
        
        #status
        game.status = "Success" 
        
        # bad guess
        game.bad_guesses = len(self.guessed_words)
        
        #game word save
        game.game_word = self.word
        
        #score calculation
        score_cal = 0
        for i, letter in enumerate(self.word):
            if letter != self.current_guess[i]:
                score_cal += letter_frequencies[letter]
        game.score = score_cal  
        
        if missed > 0:
            game.score /= missed
            (game.score)
        if game.bad_guesses > 0:
            game.score *= (1-(game.bad_guesses*0.1))     

        self.games.append(game)        

        return 
    
    
    def save_game_tell(self):
        game = Game()
        
        #missed _letters
        missed = 0
        for letter in self.guessed_letters:
            if letter not in self.current_guess:
                missed += 1
        game.missed_letters = missed
        
        #status
        game.status = "Gave Up" 
        
        #game word save
        game.game_word = self.word
        
        # bad guess
        game.bad_guesses = len(self.guessed_words)
        
        #score calculation
        score_cal = 0
        for i, letter in enumerate(self.word):
            if letter != self.current_guess[i]:
                score_cal += letter_frequencies[letter]
        game.score = -score_cal  
        self.games.append(game)
        return 

        
        
    def print_games(self):
        
        game_table = [[i + 1, game.game_word, game.status, game.bad_guesses, game.missed_letters, game.score] for i, game in enumerate(self.games)]
        headers = ["Game", "Word", "Status", "Bad Guesses", "Missed Letters", "Score"]

        print("{:<10} {:<10} {:<15} {:<15} {:<15} {:<10}".format(headers[0], headers[1], headers[2], headers[3], headers[4], headers[5]))
        print("-" * 75)
        final_score = 0
        for row in game_table:
            print("{:<10} {:<10} {:<15} {:<15} {:<15} {:<10}".format(row[0], row[1], row[2], row[3], row[4], round(row[5],2)))
            final_score += row[5]
        print(f'\nFinal Score: {round(final_score,2)}\n')
            
        return
                
