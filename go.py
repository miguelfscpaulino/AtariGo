import sys

class state():
	"""docstring for state"""
	def __init__(self,mat,player,filled,dim):
		self.mat = mat
		self.player = player
		self.filled = filled
		self.dim = dim

	def getMat():
		return self.mat

	def getPlayer():
		return self.player
	
	def getFilled():
		return self.filled	

	def getDim():
		return self.dim

	def printState(self):
		print(self.player)
		print(self.mat)
		print(self.filled)

class game():
	"""docstring for state"""
	def __init__(self,arg):
		
		self.state = self.load_board(arg)

	def printState(self):
		self.state.printState()

	def to_move(self,s):
		#returns the player to move next, given the state "s"
		return s.player
		
	def terminal_test(self,s):
		#checks if state "s" is terminal
		auxFilled = self.state.getFilled()
		auxMat = self.state.getMat()
		size = self.state.getDim()

		# for i in auxFilled

		# 	if i[1]-1 >= 0:
		# 		if auxMat[i[1]-1][]
				


		# 	if (i[1]-1 or i[2]-1)< 0 or (i[1]+1 or i[2]+1) > (size-1)
		# 		continue



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



	#TODO make the actual game!!!???
		


	def load_board(self,s):
		#loads board from file stream "s". returns corresponding state
		
		file = open(s, "r")
		l=list(file.readline())
		player= int(l[2])
		size = int(l[0])
		aux = []

		mat = [[0 for x in range(int(l[0]))] for y in range(int(l[0]))] 
	
		for i in range(size):
			l=list(file.readline())
			for h in range(size):
				mat[i][h] = int(l[h])
				if int(l[h])!= 0:
					aux.append((int(l[h]),h+ size*i + 1))
					print('h: ' + str(h) + ' i: ' + str(i))

		return state(mat,player,aux,size)

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
	g.printState()
		#g.printstate()	
	#except Exception as e:
		#print("Please insert file name")

	
		

