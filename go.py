import sys

class state():
	"""docstring for state"""
	def __init__(self,mat,player):
		self.table = mat
		self.player = player

	def printstate():
		print(self.player)

class game():
	"""docstring for state"""
	def __init__(self,arg):
		self.state=self.load_board(arg)

	def printstate():
		self.state.printstate()

	def to_move(s):
		#returns the player to move next, given the state "s"
		return s.player
		
	def terminal_test(s):
		#checks if state "s" is terminal
		pass

	def utility(s,p):
 		#returns payoff of state "s" if terminal or evaluation with respect to player		
 		pass

	def actions(s):
 		#returns list of valid moves at state "s"		
 		pass

	def result(s,a):
		#returns the sucessor game state after playing move "a" at state "s"
		if a[0]==1:
			s.player=2
		else:
			s.player=1

		s.table[a[1]][a[2]]=a[0]

		pass


	def load_board(s):
		#loads board from file stream "s". returns corresponding state
		file = open(s, "r")
		l=list(file.readline())
		player= int(l[2])
		mat = [[0 for x in range(int(l[0]))] for y in range(int(l[0]))] 

		for i in range(int(l[0])):
			l=list(file.readline())
			for h in range(int(l[0])):
				mat[i][h] =l[h]
				pass
			pass	
			
		state=state(mat,player)

		return state

def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action






if __name__ == '__main__':


	#try:
		g= game(sys.argv[1])
		g.printstate()	
	#except Exception as e:
		#print("Please insert file name")

	
		

