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
        self.terminalflag = False

    def closed_check(self, curr, checked=[]):
        """Checks if a position/group adjacent is closed. Returns True if yes"""

        # Checks top position
        if (curr[1] - self.dim) >= 0:

            # Checks if top was already checked
            up = [item for item in checked if item[0][1] == (curr[1]-self.dim)]
            if up:
                # Checks if top pos is free
                if up[0][0][0] == curr[0] and up[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if top is filled
                up = [item for item in self.filled if item[1] == (curr[1]-self.dim)]

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
            if down:
                # Checks if bottom pos is free
                if down[0][0][0] == curr[0] and down[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if bottom is filled
                down = [item for item in self.filled if item[1] == (curr[1]+self.dim)]

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
            if left:
                # Checks if left pos is free
                if left[0][0][0] == curr[0] and left[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if left is filled
                left = [item for item in self.filled if item[1] == (curr[1]-1)]

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
            if right:
                # Checks if right pos is free
                if right[0][0][0] == curr[0] and right[0][1] == False:
                    checked.append([curr, False])
                    return False
            else:
                # Checks if right is filled
                right = [item for item in self.filled if item[1] == (curr[1]+1)]

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

    def getTerminalFlag(self):
        return self.terminalflag

    def setTerminalFlag(self, flag):
        self.terminalflag = flag

    def setMat(self, m):
        self.mat = m

    def setPlayer(self, p):
        self.player = p

    def setFilled(self, f):
        self.filled = f

    def addFilled(self, f):
        self.filled.append(f)

    def removeFilled(self, f):
        self.filled.remove(f)

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
            if [item for item in checked_nodes if item[0] == i]:
                continue
            if s.closed_check(i, checked_nodes):
                s.setTerminalFlag(True)
                s.setDrawFlag(False)
                return True

        if not self.actions(s):
            s.setTerminalFlag(False)
            s.setDrawFlag(True)

        return False


    def utility(self, s, p):
        #returns payoff of state "s" if terminal or evaluation with respect to player

        if s.getDrawFlag():
                return 0

        if s.getTerminalFlag():
            if s.getPlayer() == p:
                return -1
            else:
                return 1


        dim = s.getDim()
        matP1 = [[0]*dim for i in range(dim)]
        matP2 = [[0]*dim for i in range(dim)]

       

        for i in s.getFilled():

        	coord = ind2coord(i[1],dim)

        	if i[0] == p:
        		matP1[coord[0]][coord[1]] += 1;
        	else:
        		matP2[coord[0]][coord[1]] -= 1;

        	u=False
        	d=False
        	l=False
        	r=False

        	if (i[1] - dim) >= 0:
        		u=True
        		if i[0] == p:
        			matP1[coord[0]-1][coord[1]] += 1;
        		else:
        			matP2[coord[0]-1][coord[1]] -= 1;

        	if (i[1] + dim) < dim*dim:
        		d=True
        		if i[0] == p:
        			matP1[coord[0]+1][coord[1]] += 1;
        		else:
        			matP2[coord[0]+1][coord[1]] -= 1;

        	if (i[1]%dim) != 0:
        		l=True
        		if i[0] == p:
        			matP1[coord[0]][coord[1]-1] += 1;
        		else:
        			matP2[coord[0]][coord[1]-1] -= 1;

        	if ((i[1]+1)%dim) != 0:
        		r=True
        		if i[0] == p:
        			matP1[coord[0]][coord[1]+1] += 1;
        		else:
        			matP2[coord[0]][coord[1]+1] -= 1;

        	if u and r:

        		if i[0] == p:
        			matP1[coord[0]-1][coord[1]+1] += 1;
        		else:
        			matP2[coord[0]-1][coord[1]+1] -= 1;

        	if u and l:

        		if i[0] == p:
        			matP1[coord[0]-1][coord[1]-1] += 1;
        		else:
        			matP2[coord[0]-1][coord[1]-1] -= 1;

        	if d and r:

        		if i[0] == p:
        			matP1[coord[0]+1][coord[1]+1] += 1;
        		else:
        			matP2[coord[0]+1][coord[1]+1] -= 1;

        	if d and l:

        		if i[0] == p:
        			matP1[coord[0]+1][coord[1]-1] += 1;
        		else:
        			matP2[coord[0]+1][coord[1]-1] -= 1;

        sumation = 0;

        for i in matP1:

        	sumation += sum(i)

        for i in matP2:

        	sumation += sum(i)


        aux = sumation/(dim*dim)
        #print("\n--------------------------------")
        #print("\naux:"+str(aux))
        f = open("logfile.txt","a")
        f.write("aux:" + str(aux) + "\n")
        f.close()
        return aux

    def actions(self, s):
        #returns list of valid moves at state "s"

        # act = []
        dim = s.getDim()
        player = s.getPlayer()
        if player == 1:
        	nextplayer = 2
        else:
        	nextplayer = 1 
        mat = s.getMat()
        filled = s.getFilled()

        aux = [(player, i+1, k+1) for i in range(dim) for k in range(dim) if mat[i][k] == 0]
        b = []

        for i in aux:
        	if s.closed_check((player, coord2ind(i[2]-1, i[1]-1, dim)), []):
        		if (i[1]-2) >= 0:
        			if mat[i[1]-2][i[2]-1] != player:
        				mat[i[1]-1][i[2]-1] = player
        				s.addFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        				if s.closed_check((nextplayer, coord2ind(i[2]-1, i[1]-2, dim)), []):
        					mat[i[1]-1][i[2]-1] = 0
        					s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        					continue
        				mat[i[1]-1][i[2]-1] = 0
        				s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        		if i[1] < dim:
        			if mat[i[1]][i[2]-1] != player:
        				mat[i[1]-1][i[2]-1] = player
        				s.addFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        				if s.closed_check((nextplayer, coord2ind(i[2]-1, i[1], dim)), []):
        					mat[i[1]-1][i[2]-1] = 0
        					s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        					continue
        				mat[i[1]-1][i[2]-1] = 0
        				s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        		if (i[2]-2) >= 0:
        			if mat[i[1]-1][i[2]-2] != player:
        				mat[i[1]-1][i[2]-1] = player
        				s.addFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        				if s.closed_check((nextplayer, coord2ind(i[2]-2, i[1]-1, dim)), []):
        					mat[i[1]-1][i[2]-1] = 0
        					s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        					continue
        				mat[i[1]-1][i[2]-1] = 0
        				s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        		if i[2] < dim:
        			if mat[i[1]-1][i[2]] != player:
        				mat[i[1]-1][i[2]-1] = player
        				s.addFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        				if s.closed_check((nextplayer, coord2ind(i[2], i[1]-2, dim)), []):
        					mat[i[1]-1][i[2]-1] = 0
        					s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))
        					continue
        				mat[i[1]-1][i[2]-1] = 0
        				s.removeFilled((player, coord2ind(i[2]-1, i[1]-1, dim)))

        		b.append(i)

        for k in b:
        	aux.remove(k)

        return aux


    def result(self, s, a):
        #returns the sucessor game state after playing move "a" at state "s"

        if a[0] == 1:
            # s.setPlayer(2)
            player = 2
        else:
            # s.setPlayer(1)
            player = 1

        mat = copy.deepcopy(s.getMat())
        filled = copy.deepcopy(s.getFilled())
        dim = s.getDim()

        mat[a[1]-1][a[2]-1] = a[0]
        filled.append((a[0], coord2ind(a[2]-1, a[1]-1, dim)))

        return State(mat, player, filled, dim)


    def load_board(self, s):
        #loads board from file stream "s". returns corresponding state

        l = s.readline().rstrip('\n').split(' ')
        player = int(l[1])
        size = int(l[0])

        # Reads file and creates list of lists of integers with the board
        l = [line.rstrip('\n') for line in s.readlines()]
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

# Converts 2-D coordinates of a matrix in a positive integer index
def coord2ind(x, y, s):
    return x + s*y

# Converts index of a matrix into 2-D coordinates
def ind2coord(i, s):
    return (int(i / s), i % s)

# Main function
if __name__ == '__main__':

    g = Game()
    f = open("logfile.txt","w")
    f.close()
    try:
        fileID = open(sys.argv[1], "r")
    except IndexError:
        print('Error: Filename not provided or invalid open/read')
        sys.exit()
    except IOError:
        print("Error: couldn't open board file")
        sys.exit()

    s = g.load_board(fileID)
    # s.printState()
    # move = (2,5,4)
    # s = g.result(s, move)
    # s.printState()
    # print('\n\nTerminal: ' + str(g.terminal_test(s)))
    # utilityresult = g.utility(s, 1)
    # print('\nutilityresult: ' + str(utilityresult))

    actions = g.actions(s)
    print(actions)

    # s.printState()
    # # print('\n\nTerminal: ' + str(g.terminal_test(s)))

    # # i = 1
    # # while i < 2:
    # #     actions = g.actions(s)
    # #     print('\n\nActions: ' + str(actions))
    # #     s = g.result(s, actions[int(len(actions)/2)])
    # #     s.printState()
    # #     i = i + 1
    # #
    # # print('\nutility: ' + str(g.utility(s, 1)))

    # player = s.getPlayer()
    # while True:
    #     move = alphabeta_cutoff_search(s, g)
    #     #print('\nmove: ' + str(move))
    #     s = g.result(s, move)
    #     #s.printState()
    #     #print('\n\n')
    #     if g.terminal_test(s):
    #         utilityresult = g.utility(s, player)
    #         print('\nutilityresult: ' + str(utilityresult))
    #         print('\nGAME ENDED: ' + str(utilityresult))
    #         s.printState()
    #         break
