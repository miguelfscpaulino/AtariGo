import sys

class State():
    """docstring for class State"""

    def __init__(self, mat, player, filled, dim):
        self.mat = mat
        self.player = player
        self.filled = filled
        self.dim = dim

    def closedCheck(self, f):
        c1 = True
        c2 = True
        c3 = True
        c4 = True


        print('f:')
        print(f)
        #coord = ind2coord(f[1], self.dim)

        if (f[1] - self.dim) >= 0:
            l = [item for item in self.filled if item[1] == (f[1] - self.dim)]
            print('l: ')
            print(l)
            if not l or (f[0] == l[0][0]):
                c1 = False

        if (f[1] + self.dim) < self.dim*self.dim:
            l = [item for item in self.filled if item[1] == (f[1] + self.dim)]
            print('l: ')
            print(l)
            if not l or (f[0] == l[0][0]):
                c2 = False

        if (f[1] % self.dim) != 0:
            l = [item for item in self.filled if item[1] == (f[1] - 1)]
            print('l: ')
            print(l)
            if not l or (f[0] == l[0][0]):
                c3 = False

        if ((f[1] + 1) % self.dim) != 0:
            l = [item for item in self.filled if item[1] == (f[1] + 1)]
            print('l: ')
            print(l)
            if not l or (f[0] == l[0][0]):
                c4 = False

        print('c1: ' + str(c1) + ', c2: ' + str(c2) + ', c3: ' + str(c3) + ', c4: ' + str(c4))
        if c1 and c2 and c3 and c4:
            return 1
        else:
            return -1

    def getMat(self):
        return self.mat

    def getPlayer(self):
        return self.player

    def getFilled(self):
        return self.filled

    def getDim(self):
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
        terminal = False
        auxFilled = self.state.getFilled()
        auxMat = self.state.getMat()
        dim = self.state.getDim()

        for i in auxFilled:
            check = self.state.closedCheck(i)
            print('check: ' + str(check))
            if check == 1:
                terminal = True
                break

        return terminal

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

        l = file.readline().split(' ')
        print(l)
        player = int(l[1])
        size = int(l[0])
        aux = []

        mat = [[0 for x in range(int(l[0]))] for y in range(int(l[0]))]

        for i in range(size):
            l = list(file.readline())
            for h in range(size):
                mat[i][h] = int(l[h])
                if int(l[h]) != 0:
                    aux.append((int(l[h]), coord2ind(h, i, size)))

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

def coord2ind(x, y, s):
    return x + s*y

def ind2coord(i, s):
    return (int(i / s), i % s)

# Main function
if __name__ == '__main__':

    g = Game()

    try:
        s = g.load_board(sys.argv[1])
    except IndexError:
        print('Error: Filename not provided or invalid open/read')
        sys.exit()

    s.printState()
    print(g.terminal_test(s))
