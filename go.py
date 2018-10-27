import sys

class State():
    """docstring for class State"""

    def __init__(self, mat, player, filled, dim):
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

    def setMat(m):
        self.mat = m

    def setPlayer(p):
        self.player = p

    def setFilled(f):
        self.filled = f

    def setDim(d):
        self.dim = d

    def printState(self):
        print('State::')
        print('Player: ' + str(self.player))
        print('Board: ')
        print(self.mat)
        print('Occupied positions: ')
        print(self.filled)


class Game():
    """docstring for class Game"""

    #def __init__(self, arg):
    #    self.state = self.load_board(arg)

    def getState(self):
        return self.state

    def to_move(self, s):
        #returns the player to move next, given the state "s"
        return s.getPlayer()

    def terminal_test(self, s):
        #checks if state "s" is terminal
        auxFilled = self.state.getFilled()
        auxMat = self.state.getMat()
        dim = self.state.getDim()

        # for i in auxFilled
            # 	if i[1]-1 >= 0:
            # 		if auxMat[i[1]-1][]
            # 	if (i[1]-1 or i[2]-1)< 0 or (i[1]+1 or i[2]+1) > (size-1)
            # 		continue

    def utility(s, p):
        #returns payoff of state "s" if terminal or evaluation with respect to player
        pass

    def actions(s):
        #returns list of valid moves at state "s"
        pass

    def result(s, a):
        #returns the sucessor game state after playing move "a" at state "s"
        if a[0] == 1:
            s.setPlayer(2)
        else:
            s.setPlayer(1)

        print('printing player inside result')
        print(s.player)

        s.table[a[1]][a[2]] = a[0]

        #TODO make the actual game!!!???

    def load_board(self, s):
        #loads board from file stream "s". returns corresponding state

        try:
            file = open(s, "r")
        except IOError:
            print("Error: couldn't open board file")
            sys.exit()

        l = list(file.readline())
        player = int(l[2])
        size = int(l[0])
        aux = []

        mat = [[0 for x in range(int(l[0]))] for y in range(int(l[0]))]

        for i in range(size):
            l = list(file.readline())
            for h in range(size):
                mat[i][h] = int(l[h])
                if int(l[h]) != 0:
                    aux.append((int(l[h]),h+ size*i + 1))

        self.state = State(mat, player, aux, size)
        return self.state

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


# Main function
if __name__ == '__main__':

    g = Game()

    try:
        s = g.load_board(sys.argv[1])
    except IndexError:
        print('Error: Please insert file name in args')
        sys.exit()
