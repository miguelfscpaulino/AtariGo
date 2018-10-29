import sys

class State():
    """docstring for class State"""

    def __init__(self, mat, player, filled, dim):
        self.mat = mat
        self.player = player
        self.filled = filled
        self.dim = dim

    def closed_check(self, f, g=[]):
        """Checks if a position is closed. Recursively calls itself to check
        groups. Returns 1 if it's closed, -1 if it's open, 0 if need to
        check neighbours (group found)"""

        ferr = open('err.txt', 'a')

         # Surronding position flags
        c1 = True
        c2 = True
        c3 = True
        c4 = True

        print('f: ' + str(f) + ', g: ' + str(g))
        ferr.write('f: ' + str(f) + ', g: ' + str(g) + '\n')

        # If top position is occupied, checks if occupied with another player
        if (f[1] - self.dim) >= 0 and (not g or
            not [item for item in g if (item[0] == f[0] and item[1] == (f[1]-self.dim))]):

            l = [item for item in self.filled if item[1] == (f[1] - self.dim)]
            print('l: ' + str(l))
            ferr.write('l: ' + str(l) + '\n')
            if not l:
                return -1
                #c1 = False
            elif f[0] == l[0][0] and f not in g:
                g.append(f)
                print('CALLING RECURS')
                ferr.write('CALLING RECURS' + '\n')
                b = self.closed_check(l[0], g)
                while f in g:
                    g.remove(f)
                if b == -1:
                    c1 = False



        # If down position is occupied, checks if occupied with another player
        if (f[1] + self.dim) < self.dim*self.dim and (not g or
            not [item for item in g if (item[0] == f[0] and item[1] == (f[1]+self.dim))]):

            l = [item for item in self.filled if item[1] == (f[1] + self.dim)]
            print('l: ' + str(l))
            ferr.write('l: ' + str(l) + '\n')
            if not l:
                return -1
                #c2 = False
            elif f[0] == l[0][0] and f not in g:
                g.append(f)
                print('CALLING RECURS')
                ferr.write('CALLING RECURS' + '\n')
                b = self.closed_check(l[0], g)
                while f in g:
                    g.remove(f)
                if b == -1:
                    c2 = False


        # If left position is occupied, checks if occupied with another player
        if (f[1] % self.dim) != 0 and (not g or
            not [item for item in g if (item[0] == f[0] and item[1] == (f[1]-1))]):

            l = [item for item in self.filled if item[1] == (f[1] - 1)]
            print('l: ' + str(l))
            ferr.write('l: ' + str(l) + '\n')
            if not l:
                return -1
                #c3 = False
            elif f[0] == l[0][0] and f not in g:
                g.append(f)
                print('CALLING RECURS')
                ferr.write('CALLING RECURS' + '\n')
                b = self.closed_check(l[0], g)
                while f in g:
                    g.remove(f)
                if b == -1:
                    c3 = False


        # If right position is occupied, checks if occupied with another player
        if ((f[1] + 1) % self.dim) != 0 and (not g or
            not [item for item in g if (item[0] == f[0] and item[1] == (f[1]+1))]):

            l = [item for item in self.filled if item[1] == (f[1] + 1)]
            print('l: ' + str(l))
            ferr.write('l: ' + str(l) + '\n')
            if not l:
                return -1
                #c4 = False
            elif f[0] == l[0][0] and f not in g:
                g.append(f)
                print('CALLING RECURS')
                ferr.write('CALLING RECURS' + '\n')
                b = self.closed_check(l[0], g)
                while f in g:
                    g.remove(f)
                if b == -1:
                    c4 = False

        print('c1: ' + str(c1) + ', c2: ' + str(c2) + ', c3: ' + str(c3) + ', c4: ' + str(c4))
        ferr.write('c1: ' + str(c1) + ', c2: ' + str(c2) + ', c3: ' + str(c3) + ', c4: ' + str(c4) + '\n')
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
        ferr = open('err.txt', 'a')
        ferr.write('State::')
        ferr.write('\n')
        ferr.write('Player: ' + str(self.player))
        ferr.write('\n')
        ferr.write('Board: ')
        ferr.write('\n')
        ferr.write(str(self.mat))
        ferr.write('\n')
        ferr.write('Occupied positions: ')
        ferr.write('\n')
        ferr.write(str(self.filled))
        ferr.write('\n')
        ferr.close()


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

        # Checks if each filled position of the board is closed (no liberties)
        print('auxfilled ' + str(auxFilled))
        ferr = open('err.txt', 'a')
        ferr.write('auxfilled ' + str(auxFilled))
        ferr.write('\n')
        ferr.close()
        for i in auxFilled:
            print('i: ' + str(i))
            ferr = open('err.txt', 'a')
            ferr.write('i: ' + str(i))
            ferr.write('\n')
            ferr.close()
            check = self.state.closed_check(i)
            print('check: ' + str(check))
            ferr = open('err.txt', 'a')
            ferr.write('check: ' + str(check))
            ferr.write('\n')
            ferr.close()
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
        player = int(l[1])
        size = int(l[0])

        # Python way of creatig map and filled with 3 lines of code
        # Reads file and creates list of lists of integers with the board
        l = [line.rstrip('\n') for line in file.readlines()]
        mat = [list(map(int, list(i))) for i in l]
        # List of tuples with filled positions of the board
        aux = [(mat[x][y], coord2ind(y, x, size)) for x in range(size) for y in range(size) if mat[x][y] != 0]

        # "C" style way
#        mat = [[0 for x in range(int(l[0]))] for y in range(int(l[0]))]
#        for i in range(size):
#            l = list(file.readline())
#            for h in range(size):
#                mat[i][h] = int(l[h])
#                if int(l[h]) != 0:
#                    aux.append((int(l[h]), coord2ind(h, i, size)))

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

# Converts 2-D coordinates of a matrix in a positive integer index
def coord2ind(x, y, s):
    return x + s*y

# Converts index of a matrix into 2-D coordinates
def ind2coord(i, s):
    return (int(i / s), i % s)

# Main function
if __name__ == '__main__':

    ferr = open('err.txt', 'w')
    ferr.close()
    g = Game()

    try:
        s = g.load_board(sys.argv[1])
    except IndexError:
        print('Error: Filename not provided or invalid open/read')
        sys.exit()

    s.printState()
    test = g.terminal_test(s)
    print('\n\nTerminal: ' + str(test))
    ferr = open('err.txt', 'a')
    ferr.write('\n\nTerminal: ' + str(test))
    ferr.write('\n')
    ferr.close()
