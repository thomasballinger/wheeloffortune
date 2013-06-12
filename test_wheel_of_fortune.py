from wheel_of_fortune import Board, spin_wheel, Player, Game

def get_test_board():
    b = Board()
    b.phrases = ['EE, AEAO! EE.', "AA'E AOE? OO AE! EO?", 'E. E. E.']
    return b

def test_player():
    # 1) Create a new Player and get initial stats
    print "PLAYER RELATED"
    print "----------------------"
    p1 = Player("Willson")
    assert p1.name == "Willson"
    assert p1.total_games_played == 0
    assert p1.total_games_won == 0
    assert p1.total_winnings == 0
    assert str(p1) == 'My name is Willson. I have guessed 0 total times and got 0 guesses correctlyin the 0 games I played. My win-loss record is: 0 Wins and 0 Losses.My total winnings is 0.'
    # 2) Update player name
    p1.name = "Mock"
    assert p1.name == "Mock"
    # 3) Assume player won and get 500 incremental_winnings
    p1.total_winnings += 500
    assert p1.total_winnings == 500
    # 4) Print updated player
    assert str(p1) == 'My name is Mock. I have guessed 0 total times and got 0 guesses correctlyin the 0 games I played. My win-loss record is: 0 Wins and 0 Losses.My total winnings is 500.'
    # 5) Create 2 more players
    p2 = Player("Ed")
    p3 = Player("Dennis")
    print p2
    print p3
    print

test_player()

# Board Class
#1) Create a new Board and get the current phrase and the masked phrase
print "BOARD RELATED"
print "----------------------"
board = Board()
print "Initial setup.  The correct phrase is: ", board.correct_phrase
print "Initial setup. ", board
# 2) Get phrases as a class method
print "----------------------"
print "Initial setup.  List of all the phrases: ", Board.phrases
# 3) Add a phrase that exists already
print "----------------------"
print "Adding a phrase that already exists."
print Board.add_phrase("AA'E AOE? OO AE! EO?")
# 4) Add a phrase that exists already, but in a different case
print "----------------------"
print "Adding a phrase that already exists, but in a different case."
print Board.add_phrase("aA'e aOe? Oo aE! eO?")
# 4) Add a phrase that doesn't exist yet
print "----------------------"
print "Adding a phrase that doesn't exist yet."
print Board.add_phrase("You only live once")
# 5) Scenario 1
print "----------------------"
print "Making guesses.  Scenario 1 - make an empty guess."
print board.is_guess_correct("")
print board
# 6) Scenario 2
print "----------------------"
print "Making guesses.  Scenario 2 - make a valid single letter guess, but the game continues because there are remaining pieces." 
print board.is_guess_correct("e")
print board
# 7) Scenario 1
print "----------------------"
print "Making guesses.  Scenario 1 - make a repeat guess."
print board.is_guess_correct("e")
print board
# 8) Scenario 4
print "----------------------"
print "Making guesses.  Scenario 4 - make a valid single letter guess, but nothing matches.  The game continues with remaining pieces."
print board.is_guess_correct("z")
print board
# 9) Scenario 3
print "----------------------"
print "Making guesses.  Scenario 3 - make a valid single letter guess, but the game is over because there are no more pieces to solve."
print "First, guess 'a'"
print board.is_guess_correct("a")
print "Next, guess 'o'"
print board.is_guess_correct("o")
print board
# 10) Scenario 5
print "----------------------"
print "Making guesses.  Scenario 5 - making an incorrect solve.  The game continues."
print board.is_guess_correct("never graduate!")
print board
# 11) Scenario 6
print "----------------------"
print "Making guesses.  Scenario 6 - making a correct solve.  The game ends."
print board.is_guess_correct("EE, AEAO! EE.")
print board

#Wheel Class
# 1) Create a new Wheel
print
print "WHEEL RELATED"
print "----------------------"
# 2) Generate a random spin
print spin_wheel()

#Game Class
print
print "WELCOME TO WHEEL OF FORTUNE!"
print "----------------------"
# 1) Create a game and print out the board and players
# game = Game(2)
# print game
# print "Is game over? ", game.is_game_over
# game.start_game()
# print "This is the game board: "
# print game.board
# for p in game.players:
#     print p
# # 2) Call other get functions
# print "----------------------"
# print "Number of turns so far: %s" % game.num_turns
# print "Number of players: %s" % game.num_players
# print "Current player is: %s" % game.current_player

# for i in range(0, 20):
#     print game.advance_player
