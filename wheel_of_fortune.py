import random

def spin_wheel():
    """
    Returns integer values representing the multiplier that's applied to a PLAYERs score,
    depending on the number of characters they guessed correctly.
    """
    choices = ([0] * 25 +
               [1] * 50 +
               [2] * 13 +
               [3] * 6 +
               [5] * 5 +
               [8] * 1)
    return random.choice(choices)

class Board(object):
    """
    BOARD that has a list of all phrases PLAYERs guess from. A BOARD informs PLAYERs whether their guesses were correct or not.
    """

    phrases =  ['SOMETIMES THE HEART SEES WHAT IS INVISIBLE TO THE EYE.',
                'NEVER GRADUATE!',
                "IF YOU DON'T BUILD YOUR DREAM, SOMEONE ELSE WILL HIRE YOU TO HELP THEM BUILD THEIRS.",
                'DO NOT DWELL IN THE PAST, DO NOT DREAM OF THE FUTURE, CONCENTRATE THE MIND ON THE PRESENT MOMENT.']

    def __init__(self):
        """
        A new BOARD will randomly select a phrase to start GAME.
        """
        self.correct_phrase = random.choice(self.phrases)
        self.current_phrase = self.mask_phrase()
        self.all_guesses = set()

    def __str__(self):
        s = ("""Here is what the board looks like so far: %s\nHere are all the guesses so far: %s"""
                % (self.current_phrase, str(self.all_guesses)))
        return s

    def mask_phrase(self):
        """
        Returns a STRING masked_phrase with the same length as self.correct_phrase but with all alphabetic characters converted to *

        Note: This method is only used when a BOARD object is initially set up.
        """
        return "".join('*' if c.isalpha() else c for c in self.correct_phrase)

    def is_guess_correct(self, guess):
        """
        STRING -> (INT, BOOLEAN)
        Returns the number of characters guessed correctly and whether the game is over

        Changes to state:   BOARD object's current_phrase (STRING), BOARD object's all_guesses (SET)

        There are 5 possible scenarios after making a guess:
        1) You make an invalid guess (an empty guess or a guess that's already been made).  Return (-1, False)
        2) You make a valid single letter guess.  The game still has unsolved pieces.  Return ( > 0 , False)
        3) You make a valid single letter guess.  The game doesn't have any remaining unsolved pieces.  Return ( > 0, True)
        4) You make a valid single letter guess, but there are no pieces with that guess.  Return (0, False)
        5) You make a valid multiple letter guess (solve), but you solved incorrectly.  Return (0, False)
            * Notice that (4) and (5) return identical results.
        6) You make a valid multiple letter guess (solve), and you solved correctly.  Return (0, True)
        """

        num_found = 0
        game_over = False
        u_guess = guess.upper()

        # Scenario 1 - The game continues and the player guesses again.
        if len(u_guess) == 0 or u_guess in self.all_guesses:
            print "Please guess again. You didn't provide a guess or your guess has already been made."
            num_found = -1 # need to guess again
            return (num_found, game_over)
        # Scenario 2, 3, and 4
        elif len(u_guess) == 1:
            self.all_guesses.add(u_guess)
            for (index, letter) in enumerate(self.correct_phrase):
                if u_guess == letter:
                    # Scenario 2 - The game still has unsolved pieces.  The player updates his score, the game continues, and the player goes again.
                    num_found += 1
                    self.current_phrase = self.current_phrase[:index] + u_guess + self.current_phrase[index + 1:]
            # Check if the game is over
            if self.current_phrase == self.correct_phrase:
                # Scenario 3 - The game doesn't have any remaining unsolved pieces.  The player updates his score, and the game ends.
                game_over = True
            # Scenario 4 - The game still has unsolved pieces.  The player updates his score (which is 0), the game continues, and the next player goes.
            return (num_found, game_over) # num_found will be between 0 and some positive number
        else:
            # Scenario 5 and 6
            self.all_guesses.add(u_guess)
            if u_guess == self.correct_phrase:
                # Scenario 6 - The player solves correctly.  The player updates his score (which is 0), and the game ends.
                game_over = True
                self.current_phrase = self.correct_phrase
            # Scenario 5 - The player solves incorrectly.  The player updates his score (which is 0), the game continues, and the next player goes.
            return (num_found, game_over)

    @classmethod
    def add_phrase(cls, phrase):
        """
        Input:                 a STRING phrase which can be in any case
        Output:             a LIST of all the uppercased phrases all BOARDs share
        Changes to state:    BOARD class' phrase (LIST)
        Note: Only add a phrase if the phrase doesn't already exist in the list.
        """
        if phrase.lower() in (i.lower() for i in cls.phrases):
            print "Phrase already exists."
            return cls.phrases
        cls.phrases.append(phrase.upper())
        return cls.phrases
    # add_phrase = classmethod(add_phrase) # The @classmethod is syntactic sugar for this function call.

class Player(object):
    """
    PLAYER who can interact with a BOARD within the context of a GAME.
    """

    def __init__(self, name, total_games_played = 0, total_games_won = 0, total_winnings = 0):
        self.name = name
        self.total_games_played = total_games_played
        self.total_games_won = total_games_won
        self.total_winnings = total_winnings
        self.current_game = {"score": 0, "num_guesses": 0, "num_correct_guesses": 0}
        self.total_num_guesses = self.current_game["num_guesses"]
        self.total_num_correct_guesses = self.current_game["num_correct_guesses"]

    @classmethod
    def player_from_raw_input(cls):
        p = cls(raw_input("Please enter your name: "))
        print "Welcome to Wheel of Fortune, %s" % p.name
        return p

    def __str__(self):
        return ("My name is %s. I have guessed %s total times and got %s guesses correctly"
                "in the %s games I played. My win-loss record is: %s Wins and %s Losses."
                "My total winnings is %s." % (self.name, self.total_num_guesses,
                    self.total_num_correct_guesses,self.total_games_played, self.total_games_won,
                    self.total_games_played - self.total_games_won, self.total_winnings))

    def make_proxy_for_current_game(att):
        def getter(self):
            return self.current_game[att]
        def setter(self, value):
            self.current_game[att] = value
        return property(getter, setter)

    for att in ['num_correct_guesses', 'score', 'num_guesses']:
        prop = make_proxy_for_current_game(att)
        locals().update({'current_game_' + att: prop})

    del make_proxy_for_current_game


class Game(object):
    """ Each instance of GAME keeps track of the BOARD and all the PLAYERs involved in the GAME.  """
    def __init__(self, num_players):
        self.num_turns = 0
        self.num_players = num_players
        self.players = [Player.player_from_raw_input() for _ in range(num_players)]
        random.shuffle(self.players)
        self.board = Board()

        print "This is the order of the game: "
        for j in self.players:
            print j.name
        self.current_player = self.players[0]
        self.is_game_over = False

    def __str__(self):
        s = ("Here's a description of a game so far:\n** Game **\nThere are %s players."
             "We are on turn %s, and here's a description of the current player:\n%s\n\n**"
             "Players **\n%s\n\n** Board **\n%s" %
             (self.num_players, self.num_turns, self.current_player, self.players, self.board))
        return s

    def advance_player(self):
        """
        Advance the player and inrement self.num_turns

        Note:  This method should only be called when Scenario 4 or 5 occurs.
        """
        self.num_turns += 1
        self.current_player = self.players[self.num_turns % self.num_players]
        return self.current_player

    def prompt_guess(self):
        guess = raw_input("Please enter a guess: ")
        # Basic Validation: Is there a way to just make sure there are no numbers? Regex?

        # if not guess.isalpha():
        #     print "Please enter either a single alphabetic letter or an alphabetic phrase."
        #     return self.prompt_guess()
        # else:
        #     return guess
        return guess

    def start_game(self):
        """
        Changes to state:   GAME (num_turns, board, players, current_player, is_game_over)
                            PLAYER (total_games_played, total_games_won, total_winnings, current_game, total_num_guesses, total_num_correct_guesses,)
                            BOARD (current_phrase, all_guesses)

        Note:  This method should only be run at the end of the __init__ method.  This method establishes the game loop and will keep on
        looping until the is_game_over counter is set to TRUE.  This can only happen if scenario 3 or 6 occurs.

        This method has 2 layers of checks:
        1) First, it checks if the current_player's WHEEL spin passes.
                If it passes, then execution proceeds to the second layer.
                If it doesn't pass, then it becomes the next player's turn.
        2) Assuming the current_player makes it to this layer, execution will depend on how the PLAYER guesses:
                Execution here will depend entirely on the results of calling BOARD.is_guess_correct().
                There are 5 possible outcomes defined for BOARD.is_guess_correct().
        """
        # Initially, the game will not be over
        while not self.is_game_over:
            # Current player makes a guess, which means I need to update the current game's num_guesses
            print self.board

            score = 0

            print self.current_player.name + ", it's your turn and here's your current score: %s" % self.current_player.current_game_score
            raw_input("Press enter to see what you spin!")
            spin = spin_wheel()
            print "You rolled a %s." % spin

            if spin == 0:
                # Increment number of guesses; don't update score; get next player
                print "Sorry, rolling a %s means it's the next player's turn." % spin
                self.current_player.current_game_num_guesses += 1
                # print self.current_player()
                self.advance_player()
                # print self.current_player()
                # self.is_game_over = True
            else:
                # You successfully spun the wheel
                player_guess = self.prompt_guess()
                # Submit guess to board
                (num_found, game_over) = self.board.is_guess_correct(player_guess)
                # Scenario 1
                if num_found == -1:
                    # Don't update number of guesses
                    continue
                # Scenario 2
                elif num_found > 0 and not game_over:
                    self.current_player.current_game_num_guesses += 1
                    self.current_player.current_game_num_correct_guesses += 1
                    score = num_found * spin
                    self.current_player.current_game_score += score
                    print self.current_player.name + ", you guessed the letter %s and there are %s on the board! Since you guessed correctly, it's your turn again!" % (player_guess, num_found)
                # Scenario 3
                elif num_found > 0 and game_over:
                    self.current_player.inc_current_game_num_guesses()
                    self.current_player.current_game_num_correct_guesses += 1
                    score = num_found * spin
                    self.current_player.current_game_score += score
                    self.is_game_over = game_over
                    print self.current_player.name + ", you guessed the letter %s and there are %s on the board! Since you guessed the last letter on the board, you just won!" % (player_guess, num_found)
                # Scenario 6
                elif num_found == 0 and game_over:
                    self.current_player.current_game_num_guesses += 1
                    self.current_player.current_game_num_correct_guesses += 1
                    self.is_game_over = game_over
                    print self.current_player.name + ", you just solved the board with the guess %s! Congrats!" % player_guess
                # Scenario 4 or 5
                else:
                    self.current_player.current_game_num_guesses += 1
                    print self.current_player.name + ", sorry but your guess wasn't correct.  It's the next player's turn now!"
                    self.advance_player()
        # The game is now over.  Need to update game scores for all players.
        print "The game took %s turns." % self.num_turns() + 1
        for p in self.players:
            p.inc_total_games_played()
            p.total_num_guesses += p.current_game_num_guesses
            p.total_num_correct_guesses += p.current_game_num_correct_guesses
            # The game ends with the current player being the winner
            if p == self.current_player:
                p.inc_total_games_won()
                p.total_winnings += p.current_game_score
            print p

if __name__ == '__main__':
    print
    print "WELCOME TO WHEEL OF FORTUNE!"
    print "----------------------"
    game = Game(2)
    game.start_game()
