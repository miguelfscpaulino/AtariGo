


class state():
	"""docstring for state"""
	def __init__(self, arg):
		super(state, self).__init__()
		self.table = table
		self.player = player
		
class game():
		

	def to_move(s):
		pass
		
	def terminal_test(s):#-1:loss 1:win 0:draw
		pass

	def utility(s,p):
		pass
	def actions(s):
		pass

	def result(s,a):
		pass


	def load_board(s):

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
	import sys

	g= game() 
	g.load_board(sys.argv[1])