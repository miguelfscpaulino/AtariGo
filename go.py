import sys
import copy

infinity = float('inf')


class State():
    """docstring for class State"""

    def __init__(self, mat, player, filled, dim):
        self.mat = mat
        self.player = player
        self.filled = filled
        self.dim = dim
        self.drawflag = False

    def closed_check(self, curr, checked=[]):
        """Checks if a position/group adjacent is closed. Returns True if yes"""

        print('\nStarting close_check:')
        print('curr: ' + str(curr))
        print('checked: ' + str(checked) + '\n')


        # Checks top position
        if (curr[1] - self.dim) >= 0:

            # Checks if top was already checked
            up = [item for item in checked if item[0][1] == (curr[1]-self.dim)]
            print('up: '+ str(up))
            if up:
                # Checks if top pos is free
                if up[0][0][0] == curr[0] and up[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if top is filled
                up = [item for item in self.filled if item[1] == (curr[1]-self.dim)]
                print('up: '+ str(up))

                if not up:     # Top pos is free
                    checked.append([curr, False])
                    return False
                else:           # Top is filled

                    # Checks if top position is filled with an equal piece
                    if up[0][0] == curr[0]:
                        i = [curr, True]
                        if i not in checked:
                            checked.append(i)
                        # Checks if group on top of current is closed
                        if not self.closed_check(up[0], checked):
                            while i in checked:
                                checked.remove(i)
                            checked.append([curr, False])
                            return False


        # Checks bottom position
        if (curr[1] + self.dim) < self.dim*self.dim:

            # Checks if bottom was already checked
            down = [item for item in checked if item[0][1] == (curr[1]+self.dim)]
            print('down: '+ str(down))
            if down:
                # Checks if bottom pos is free
                if down[0][0][0] == curr[0] and down[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if bottom is filled
                down = [item for item in self.filled if item[1] == (curr[1]+self.dim)]
                print('down: '+ str(down))

                if not down:    # Bottom pos is free
                    checked.append([curr, False])
                    return False
                else:           # Bottom pos is filled

                    # Checks if bottom position is filled with an equal piece
                    if down[0][0] == curr[0]:
                        i = [curr, True]
                        if i not in checked:
                            checked.append(i)
                        # Checks if group on bottom of current is closed
                        if not self.closed_check(down[0], checked):
                            while i in checked:
                                checked.remove(i)
                            checked.append([curr, False])
                            return False


        # Checks left position
        if (curr[1] % self.dim) != 0:

            # Checks if left was already checked
            left = [item for item in checked if item[0][1] == (curr[1]-1)]
            print('left: '+ str(left))
            if left:
                # Checks if left pos is free
                if left[0][0][0] == curr[0] and left[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if left is filled
                left = [item for item in self.filled if item[1] == (curr[1]-1)]
                print('left: '+ str(left))

                if not left:    # Left pos is free
                    checked.append([curr, False])
                    return False
                else:           # Left pos is filled

                    # Checks if left position is filled with an equal piece
                    if left[0][0] == curr[0]:
                        i = [curr, True]
                        if i not in checked:
                            checked.append(i)
                        # Checks if group on left of current is closed
                        if not self.closed_check(left[0], checked):
                            while i in checked:
                                checked.remove(i)
                            checked.append([curr, False])
                            return False


        # Checks right position
        if ((curr[1]+1) % self.dim) != 0:

            # Checks if right was already checked
            right = [item for item in checked if item[0][1] == (curr[1]+1)]
            print('right: '+ str(right))
            if right:
                # Checks if right pos is free
                if right[0][0][0] == curr[0] and right[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if right is filled
                right = [item for item in self.filled if item[1] == (curr[1]+1)]
                print('right: '+ str(right))

                if not right:   # Right pos is free
                    checked.append([curr, False])
                    return False
                else:           # Right pos is filled

                    # Checks if right position is filled with an equal piece
                    if right[0][0] == curr[0]:
                        i = [curr, True]
                        if i not in checked:
                            checked.append(i)
                        # Checks if group on right of current is closed
                        if not self.closed_check(right[0], checked):
                            while i in checked:
                                checked.remove(i)
                            checked.append([curr, False])
                            return False

        if [curr, True] not in checked:
            checked.append([curr, True])

        return True


    def getMat(self):
        return self.mat

    def getPlayer(self):
        return self.player

    def getFilled(self):
        return self.filled

    def getDim(self):
        return self.dim

    def getDrawFlag(self):
        return self.drawflag

    def setDrawFlag(self, flag):
        self.drawflag = flag

    def setMat(self, m):
        self.mat = m

    def setPlayer(self, p):
        self.player = p

    def setFilled(self, f):
        self.filled = f

    def setDim(self, d):
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

    def getState(self):
        return self.state

    def to_move(self, s):
        #returns the player to move next, given the state "s"
        return s.getPlayer()

    def terminal_test(self, s):
        #checks if state "s" is terminal

        # Checks if each filled position of the board is closed (no liberties)
        checked_nodes = []
        for i in s.getFilled():
            print('---------------------------------------')
            print('Current piece in terminal_test: ' + str(i))
            if [item for item in checked_nodes if item[0] == i]:
                print('Already checked this node/group. Continue to next')
                continue
            if s.closed_check(i, checked_nodes):
                print('\n\nFound terminal state!\nchecked: ' + str(checked_nodes))
                s.setDrawFlag(False)
                return True
            print('\nchecked: ' + str(checked_nodes))

        if not self.actions(s):
            print('\n\nFound terminal state! DRAW')
            s.setDrawFlag(True)
            return True

        return False


    def utility(self, s, p):
        #returns payoff of state "s" if terminal or evaluation with respect to player

        if self.terminal_test(s):

            if s.getDrawFlag():
                return 0

            if s.getPlayer() == p:
                return -1
            else:
                return 1

        return 0.2

    def actions(self, s):
        #returns list of valid moves at state "s"

        # act = []
        dim = s.getDim()
        player = s.getPlayer()
        mat = s.getMat()

        return [(player, i+1, k+1) for i in range(dim) for k in range(dim) if
                mat[i][k] == 0 and not s.closed_check((player, coord2ind(k, i, dim)), [])]

    def result(self, s, a):
        #returns the sucessor game state after playing move "a" at state "s"

        print('a: ' + str(a))
        if a[0] == 1:
            # s.setPlayer(2)
            player = 2
        else:
            # s.setPlayer(1)
            player = 1

        print('MATORIG antes: ' + str(s.getMat()))

        mat = copy.deepcopy(s.getMat())
        filled = copy.deepcopy(s.getFilled())
        dim = s.getDim()

        mat[a[1]-1][a[2]-1] = a[0]
        filled.append((a[0], coord2ind(a[2]-1, a[1]-1, dim)))

        print('MATORIG depois: ' + str(s.getMat()))
        return State(mat, player, filled, dim)


    def load_board(self, s):
        #loads board from file stream "s". returns corresponding state

        try:
            file = open(s, "r")
        except IOError:
            print("Error: couldn't open board file")
            sys.exit()

        l = file.readline().rstrip('\n').split(' ')
        player = int(l[1])
        size = int(l[0])

        # Reads file and creates list of lists of integers with the board
        l = [line.rstrip('\n') for line in file.readlines()]
        mat = [list(map(int, list(i))) for i in l]
        # List of tuples with filled positions of the board
        aux = [(mat[x][y], coord2ind(y, x, size)) for x in range(size) for y in range(size) if mat[x][y] != 0]

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

def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            state.printState()
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            state.printState()
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    print('ANTES DO primeiro for do alfabeta SEarch')
    for a in game.actions(state):
        print('CHAMA MIN VALUE')
        v = min_value(game.result(state, a), best_score, beta)
        state.printState()
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

    g = Game()

    try:
        s = g.load_board(sys.argv[1])
    except IndexError:
        print('Error: Filename not provided or invalid open/read')
        sys.exit()

    s.printState()
    # print('\n\nTerminal: ' + str(g.terminal_test(s)))

    # i = 1
    # while i < 2:
    #     actions = g.actions(s)
    #     print('\n\nActions: ' + str(actions))
    #     s = g.result(s, actions[int(len(actions)/2)])
    #     s.printState()
    #     i = i + 1
    #
    # print('\nutility: ' + str(g.utility(s, 1)))

    while True:
        player = s.getPlayer()
        move = alphabeta_cutoff_search(s, g)
        print('move: ' + str(move))
        s = g.result(s, move)
        s.printState()
        if g.terminal_test(s):
            print('\nGAME ENDED: ' + str(g.utility(s,player)))
            s.printState()
            break
