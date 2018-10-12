
class Game:
  """Game engine class"""

  def to_move(s):
    #returns the player to move next given the state s
    print('called to_move(s)')

  def terminal_test(s):
    #checks if state s is terminal
    print('called terminal_test(s)')

  def utility(s, p):
    #returns payoff of state s if terminal or evaluation with respect to player
    print('called utility(s, p)')

  def actions(s):
    #returns list of valid moves at state s
    print('called actions(s)')

  def result(s, a):
    #returns the sucessor game state after playing move a at state s
    print('called result(s, a)')

  def load_board(s):
    #loads board from file stream s. returns corresponding state
    print('called load_board(s)')


  def __init__(self):
    print('nothing')
