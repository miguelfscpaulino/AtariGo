import sys
import copy

infinity = float('inf')


class State():
    """docstring for class State"""
    # class state has the following atributes
    def __init__(self, mat, player, filled, dim, groups1, groups2, zeros1, zeros2, terminalflag=False, drawflag= False):
        self.mat = mat              # game matrix
        self.player = player        # current player 
        self.filled = filled        # list of positions occupied in the board in a certain state
        self.dim = dim              # dimension of the board(9x9 -> dim = 9)
        self.drawflag = drawflag       # Flag that is 1 if state is a draw, 0 else
        self.terminalflag = terminalflag   # Flag that is 1 if state is a terminal, 0 else
        self.groups1 = groups1      # List of lists of player 1 in which is list is a group(string) and has the positions of said group
        self.groups2 = groups2      # List of lists of player 2 in which is list is a group(string) and has the positions of said group
        self.zeros1 = zeros1        # List of lists of player 1 in which is list is the liberties of a group in groups1 list and has the positions of said liberties
        self.zeros2 = zeros2        # List of lists of player 2 in which is list is the liberties of a group in groups2 list and has the positions of said liberties


    def surronding_zeros(self, pos, dim, filled):
    	#Function that checks if a certain position has zeros(liberties) around itself and returns a list with thoose positions.
    	#If there aren't any zeros, returns an empty list.

        zeros = []

        if (pos - dim) >= 0: #Checks if the position above exists and is a zero
            for item in filled:
                if item[1] == (pos-dim):
                    break
                elif item[1] > (pos-dim):
                    zeros.append(pos-dim)
                    break

        if (pos + dim) < dim*dim: #Checks if the position bellow exists and is a zero
            for item in filled:
                if item[1] == (pos+dim):
                    break
                elif item[1] > (pos+dim) or item == filled[-1]:
                    zeros.append(pos+dim)
                    break

        if (pos % dim) != 0: #Checks if the position to the left exists and is a zero
            for item in filled:
                if item[1] == pos-1:
                    break
                elif item[1] > pos-1:
                    zeros.append(pos-1)
                    break

        if ((pos+1) % dim) != 0: #Checks if the position to the right exists and is a zero
            for item in filled:
                if item[1] == (pos+1):
                    break
                elif item[1] > (pos+1) or item == filled[-1]:
                    zeros.append(pos+1)
                    break

        return zeros


    
        # Group of self explanatory functions(getters and setters)
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

    def getTerminalFlag(self):
        return self.terminalflag

    def getGroups1(self):
        return self.groups1

    def getGroups2(self):
        return self.groups2

    def getZeros1(self):
        return self.zeros1

    def getZeros2(self):
        return self.zeros2

    def setDrawFlag(self, flag):
        self.drawflag = flag

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


class Game():
    """docstring for class Game"""

    def getState(self): #Returns the current state
        return self.state 

    def to_move(self, s):
        #returns the player to move next, given the state "s"
        return s.getPlayer()

    def terminal_test(self, s):
        #checks if state "s" is terminal

        zeros1 = s.getZeros1()
        zeros2 = s.getZeros2()

        for zeros in [zeros1, zeros2]: #If a certain group has no liberties, the state is terminal.
            for i in zeros:
                if len(i) == 0:
                    s.setTerminalFlag(True)
                    s.setDrawFlag(False)
                    return True

        if not self.actions(s): #Sets draw flag if it is a draw
            s.setTerminalFlag(False)
            s.setDrawFlag(True)

        return False


    def utility(self, s, p):
        #returns payoff of state "s" if terminal or evaluation with respect to player

        if s.getDrawFlag(): #If it's a draw, the utility is 0.
                return 0

        if s.getTerminalFlag(): # If the state is terminal , returns + or - 1 depending if the original player given by the original state won or not, respecitvely.
            if s.getPlayer() == p:
                return -1
            else:
                return 1

        if p ==1:               # Else, it's considered that the state that reduces the largest number of liberties of an opposing group is the better one.
            zeros= s.getZeros2()
        else:
            zeros= s.getZeros1()

        liberties = []

        for i in zeros:
            liberties.append(len(i))

        dim = s.getDim()

        return 1 - min(liberties)/(dim*dim); 


    def actions(self, s):
        #returns list of valid moves at state "s"

        dim = s.getDim() 
        player = s.getPlayer()
        if player == 1:                 #Choses what lists to evaluate depending on whose turn it is.
        	zerosCont = s.getZeros2()
        	zerosOwn = s.getZeros1()
        else:
        	zerosCont = s.getZeros1()
        	zerosOwn = s.getZeros2()

        mat = s.getMat()
        filled = s.getFilled()
        dim = s.getDim()

        aux = [(player, i+1, k+1) for i in range(dim) for k in range(dim) if mat[i][k] == 0] #initialy all zeros are possible moves in the board

        rmv = []
        for mov in aux:                                     # Cicle to remove suicidal moves, which envolves verifying if the move is a suicide to the 
        	continue_flag = False                           # specific piece, to the group it's going to belong to if played or if it's not a suicide because it captures
        	ind = coord2ind(mov[2]-1, mov[1]-1, dim)        # an oponent group.
        	if not s.surronding_zeros(ind, dim, filled):
        		for i in zerosCont:
        			if len(i) == 1 and i[0] == ind:
        				continue_flag = True
        				break
        		if continue_flag:
        			continue

        		for i in zerosOwn:
        			if ind in i:
        				if len(i) != 1:
        					continue_flag = True
        					break
        		if continue_flag:
        			continue
        		else:
        			rmv.append(mov)

        for k in rmv:
        	aux.remove(k)

        return aux


    def result(self, s, a):
        #returns the sucessor game state after playing move "a" at state "s"

        if a[0] == 1:                                   #if player is player 1..
            groups = copy.deepcopy(s.getGroups1())      #..player groups is groups2,..
            zeros = copy.deepcopy(s.getZeros1())        #..list of surounding zeros is palyer's 1 zeros
            zerosCont = copy.deepcopy(s.getZeros2())    #..and list of contrarie surounding zeros is palyer's 2 zeros
            player = 2
        else:                                           #same but for player 2
            groups = copy.deepcopy(s.getGroups2())      
            zeros = copy.deepcopy(s.getZeros2())
            zerosCont = copy.deepcopy(s.getZeros1())
            player = 1

        mat = s.getMat()
        filled = s.getFilled()
        dim = s.getDim()


        ind = coord2ind(a[2]-1, a[1]-1, dim)    #gets index of the new piece 

        mat = mat[:(a[1]-1)] + [mat[a[1]-1][:(a[2]-1)] + [a[0]] + mat[a[1]-1][a[2]:]] + mat[a[1]:]  #remakes the board with the new piece

        filled = filled + [(a[0], ind)]     #adds the piece's index to the "filled" list
        filled.sort(key=lambda x:x[1])      #sort "filled" list by the indexes

        UpGroup=[]                      #group to which the top piece (of the piece that was played) is associated
        DownGroup=[]                    #  "    "   "    "  down piece is associated
        LeftGroup=[]                    #  "    "   "    "  left piece is associated
        RightGroup=[]                   #  "    "   "    "  right piece is associated
        joinedUp=False                  # flag if a connection to the upper piece was made
        joinedDown=False                #  "    " "      "     "   "  down piece was made
        joinedLeft=False                #  "    " "      "     "   "  left piece was made
        joinedRight = False             #  "    " "      "     "   "  right piece was made


        if (ind - dim) >= 0 and mat[a[1]-2][a[2]-1] == a[0]:        #if the position above the new piece exists and has a piece of the same colour..
            for k in groups:                                        #..finds the group of that piece..
                if (ind - dim) in k:                            
                    k.append(ind)                                   #..connects the new piece with that group.
                    joinedUp=True
                    break


        if (ind + dim) < dim*dim and mat[a[1]][a[2]-1] == a[0]:     #if the position bellow the new piece exists and has a piece of the same colour..
            if joinedUp:                                            #..if a connection with the above piece was made..

                cntup_flag = True
                cntup = 0
                cntdown_flag = True
                cntdown = 0
                DownGroup = []
                UpGroup = []
                for k in groups:                                    #..search the group list.. 
                    if ind in k:
                        cntup_flag = False
                        UpGroup=k                                   #..finds the above piece's group..
                    if (ind+dim) in k:
                        cntdown_flag = False
                        DownGroup=k                                 #..finds the bellow piece's group..
                    if UpGroup and DownGroup:
                        break
                    if cntup_flag:
                        cntup += 1
                    if cntdown_flag:
                        cntdown += 1
                if UpGroup is not DownGroup:                        #..and if the groups are not the same..
                    for k in DownGroup:
                        UpGroup.append(k)                           #..connects the pieces of the bellow piece's group to the group of the above piece.
                    groups.remove(DownGroup)
                    for k in zeros[cntdown]:
                        zeros[cntup].append(k)                      #adds the bellow group's liberties to the above group's
                    zeros.remove(zeros[cntdown])                    #removes the liberties list of the down group
            else:                                                   #if a connection was not made with the above ..
                for k in groups:                                    #..search the group list..
                    if (ind+dim) in k:
                        k.append(ind)                               #..and connects to the bellow piece's group
                        joinedDown = True
                        break

        if (ind%dim) != 0 and mat[a[1]-1][a[2]-2] == a[0]:          #if the position to the left of the new piece exists and has a piece of the same colour..
            if joinedUp:                                            #..if a connection with the above piece was made..

                cntup_flag = True
                cntup = 0
                cntleft_flag = True
                cntleft = 0
                LeftGroup = []
                UpGroup = []
                for k in groups:                                    #..search the group list.. 
                    if ind in k:
                        cntup_flag = False
                        UpGroup=k                                   #..finds the above piece's group..
                    if (ind-1) in k:
                        cntleft_flag = False
                        LeftGroup=k                                 #..finds the left piece's group..
                    if UpGroup and LeftGroup:
                        break
                    if cntup_flag:
                        cntup += 1
                    if cntleft_flag:
                        cntleft += 1
                if UpGroup is not LeftGroup:                        #..and if the groups are not the same..
                    for k in LeftGroup:
                        UpGroup.append(k)                           #..connects the pieces of the left piece's group to the group of the above piece.
                    groups.remove(LeftGroup)
                    for k in zeros[cntleft]:
                        zeros[cntup].append(k)                      #adds the left group's liberties to the above group's
                    zeros.remove(zeros[cntleft])                    #removes the liberties list of the left group
            elif joinedDown:                                        #..if a connection with the above piece was not made but instead made with the bellow piece..

                cntdown_flag = True
                cntdown = 0
                cntleft_flag = True
                cntleft = 0
                DownGroup = []
                LeftGroup = []
                for k in groups:                                    #..search the group list.. 
                    if ind in k:
                        cntdown_flag = False
                        DownGroup=k                                 #..finds the bellow piece's group..
                    if (ind-1) in k:
                        cntleft_flag = False
                        LeftGroup=k                                 #..finds the left piece's group..
                    if DownGroup and LeftGroup:
                        break
                    if cntdown_flag:
                        cntdown += 1
                    if cntleft_flag:
                        cntleft += 1
                if DownGroup is not LeftGroup:                      #..and if the groups are not the same..
                    for k in LeftGroup:
                        DownGroup.append(k)                         #..connects the pieces of the left piece's group to the group of the bellow piece.
                    groups.remove(LeftGroup)
                    for k in zeros[cntleft]:
                        zeros[cntdown].append(k)                    #adds the left group's liberties to the bellow group's
                    zeros.remove(zeros[cntleft])                    #removes the liberties list of the left group
            else:                                                   #if a connection was not made with the above and bellow pieces..
                for k in groups:                                    #..search the group list..
                    if (ind-1) in k:
                        k.append(ind)                               #..and connects to the right piece's group
                        joinedLeft = True
                        break

        if (ind+1)%dim != 0 and mat[a[1]-1][a[2]] == a[0]:          #if the position on the right of the new piece exists and has a piece of the same colour..
            if joinedUp:                                            #..if a connection with the above piece was made..


                cntup_flag = True
                cntup = 0
                cntright_flag = True
                cntright = 0
                UpGroup = []
                RightGroup = []
                for k in groups:                                    #..search the group list.. 
                    if ind in k:
                        cntup_flag = False
                        UpGroup=k                                   #..finds the above piece's group..
                    if (ind+1) in k:
                        cntright_flag = False
                        RightGroup=k                                #..finds the right piece's group..
                    if UpGroup and RightGroup:
                        break
                    if cntup_flag:
                        cntup += 1
                    if cntright_flag:
                        cntright += 1
                if UpGroup is not RightGroup:                       #..and if the groups are not the same..
                    for k in RightGroup:   
                        UpGroup.append(k)                           ##..connects the pieces of the right piece's group to the group of the above piece.
                    groups.remove(RightGroup)
                    for k in zeros[cntright]:
                        zeros[cntup].append(k)                      #adds the right group's liberties to the above group's
                    zeros.remove(zeros[cntright])                   #removes the liberties list of the right group
            elif joinedDown:                                        #..if a connection with the above piece was not made but instead made with the bellow piece..

                cntdown_flag = True
                cntdown = 0
                cntright_flag = True
                cntright = 0
                DownGroup = []
                RightGroup = []
                for k in groups:                                    #..search the group list.. 
                    if ind in k:
                        cntdown_flag = False
                        DownGroup=k                                 #..finds the bellow piece's group..
                    if (ind+1) in k:
                        cntright_flag = False
                        RightGroup=k                                #..finds the right piece's group..
                    if DownGroup and RightGroup:
                        break
                    if cntdown_flag:
                        cntdown += 1
                    if cntright_flag:
                        cntright += 1
                if DownGroup is not RightGroup:                     #..and if the groups are not the same..
                    for k in RightGroup:
                        DownGroup.append(k)                         #..connects the pieces of the right piece's group to the group of the bellow piece.
                    groups.remove(RightGroup)
                    for k in zeros[cntright]:
                        zeros[cntdown].append(k)                    #adds the right group's liberties to the bellow group's
                    zeros.remove(zeros[cntright])                   #removes the liberties list of the right group
            elif joinedLeft:                                        #..if a connection was not made with the above and bellow pieces but was made with the left piece..

                cntleft_flag = True
                cntleft = 0
                cntright_flag = True
                cntright = 0
                LeftGroup = []
                RightGroup = []
                for k in groups:                                    #..search the group list.. 
                    if ind in k:
                        cntleft_flag = False
                        LeftGroup=k                                 #..finds the left piece's group..
                    if (ind+1) in k:
                        cntright_flag = False
                        RightGroup=k                                #..finds the right piece's group..
                    if LeftGroup and RightGroup:                    
                        break
                    if cntleft_flag:
                        cntleft += 1
                    if cntright_flag:
                        cntright += 1
                if LeftGroup is not RightGroup:                     #..and if the groups are not the same..
                    for k in RightGroup:
                        LeftGroup.append(k)                         #..connects the pieces of the right piece's group to the group of the left piece..
                    groups.remove(RightGroup)
                    for k in zeros[cntright]:
                        zeros[cntleft].append(k)                    #adds the right group's liberties to the left group's
                    zeros.remove(zeros[cntright])                   #removes the liberties list of the right group
            else:                                                   #if a connection was nor made with any other pieces..
                for k in groups:                                    #..search the group list..
                    if (ind+1) in k:
                        k.append(ind)                               #.. and connects with the right piece's group
                        joinedRight = True
                        break

        if not joinedUp and not joinedDown and not joinedLeft and not joinedRight:      #if the new piece has not been connected with any other piece..
            groups.append([ind])                                                        #.. creates a new group with the new piece..
            zeros.append(s.surronding_zeros(ind, dim, filled))                          #..and creates a new list of surrounding zeros associated with that group

        for i in range(len(zeros)):
            if ind in zeros[i]:
                for k in s.surronding_zeros(ind, dim, filled):
                    zeros[i].append(k)                              #adds the surrouding zeros of the new piece to the group of liberties where the new piece has benn added 
            zeros[i] = list(set(zeros[i]))
            if ind in zeros[i]:
                zeros[i].remove(ind)                                #removes the new piece board's index from all the liberties lists where "ind" was a liberty of the player's groups 

        for i in range(len(zerosCont)):                             ##removes the new piece board's index from all the liberties lists where "ind" was a liberty of the next player's groups 
            if ind in zerosCont[i]:
                zerosCont[i].remove(ind)

        if a[0] == 1:
            groups1 = groups
            zeros1 = zeros
            groups2 = s.getGroups2()
            zeros2 = zerosCont
        else:
            groups1 = s.getGroups1()
            zeros1 = zerosCont
            groups2 = groups
            zeros2 = zeros

        return State(mat, player, filled, dim, groups1, groups2, zeros1, zeros2)


    def load_board(self, s):
        #loads board from file stream "s". returns corresponding state

        l = s.readline().rstrip('\n').split(' ')
        player = int(l[1])
        dim = int(l[0])

        # Reads file and creates list of lists of integers with the board
        l = [line.rstrip('\n') for line in s.readlines()]
        mat = [list(map(int, list(i))) for i in l]
        # List of tuples with filled positions of the board
        aux = [(mat[x][y], coord2ind(y, x, dim)) for x in range(dim) for y in range(dim) if mat[x][y] != 0]

        groups1=[]
        zeros1=[]
        groups2=[]
        zeros2=[]

        for i in aux: # Fills the two lists of existing groups and corresponding liberties

            if i[0] == 1:
                groups = groups1
            else:
                groups = groups2

            joined=False
            coord = ind2coord(i[1],dim)

            if (i[1] - dim) >= 0 and mat[coord[0]-1][coord[1]] == i[0]: #Connects to any same color piece above it, if it exists.
                for k in groups:
                    if (i[1] - dim) in k:
                        k.append(i[1])
                        joined=True
                        break

            if (i[1]%dim) != 0 and mat[coord[0]][coord[1]-1] == i[0]: #Connects to any same color piece to the left, if it exists.
                if joined:
                    UpGroup=[]
                    LeftGroup=[]
                    for k in groups:
                        if (i[1]) in k:
                            UpGroup=k
                        if (i[1]-1) in k:
                            LeftGroup=k
                        if UpGroup and LeftGroup:
                            break
                    if UpGroup is not LeftGroup:
                        for k in LeftGroup:
                            UpGroup.append(k)
                        groups.remove(LeftGroup)
                else:
                    for k in groups:
                        if (i[1]-1) in k:
                            k.append(i[1])
                            joined = True
                            break

            if not joined:
                groups.append([i[1]])



        for (groups, zeros) in [(groups1, zeros1),(groups2, zeros2)]: #Defning the liberties of each group by verifying the zeros next to it.

            cnt=0
            for k in groups:
                zeros.append([])
                for i in k:
                    coord = ind2coord(i,dim)
                    if (i - dim) >= 0 and mat[coord[0]-1][coord[1]]==0 and (i-dim) not in zeros[cnt]:
                        zeros[cnt].append(i-dim)

                    if (i + dim) < dim*dim and mat[coord[0]+1][coord[1]]==0 and (i+dim) not in zeros[cnt]:
                        zeros[cnt].append(i+dim)

                    if (i%dim) != 0 and mat[coord[0]][coord[1]-1]==0 and (i-1) not in zeros[cnt]:
                        zeros[cnt].append(i-1)

                    if ((i+1)%dim) != 0 and mat[coord[0]][coord[1]+1]==0 and (i+1) not in zeros[cnt]:
                        zeros[cnt].append(i+1)
                cnt += 1

        auxState= State(mat, player, aux, dim, groups1, groups2, zeros1, zeros2)
        self.terminal_test(auxState)
        auxState.printState()


        self.state = State(mat, player, aux, dim, groups1, groups2, zeros1, zeros2, auxState.getTerminalFlag(), auxState.getDrawFlag())
        return self.state


# def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
#     """Search game to determine best action; use alpha-beta pruning.
#     This version cuts off search and uses an evaluation function."""

#     player = game.to_move(state)

#     # Functions used by alphabeta
#     def max_value(state, alpha, beta, depth):
#         if cutoff_test(state, depth):
#             return eval_fn(state)
#         v = -infinity
#         for a in game.actions(state):
#             v = max(v, min_value(game.result(state, a),
#                                  alpha, beta, depth + 1))
#             if v >= beta:
#                 return v
#             alpha = max(alpha, v)
#         return v

#     def min_value(state, alpha, beta, depth):
#         if cutoff_test(state, depth):
#             return eval_fn(state)
#         v = infinity
#         for a in game.actions(state):
#             v = min(v, max_value(game.result(state, a),
#                                  alpha, beta, depth + 1))
#             if v <= alpha:
#                 return v
#             beta = min(beta, v)
#         return v

#     # Body of alphabeta_cutoff_search starts here:
#     # The default test cuts off at depth d or at a terminal state
#     cutoff_test = (cutoff_test or
#                    (lambda state, depth: depth > d or
#                     game.terminal_test(state)))
#     eval_fn = eval_fn or (lambda state: game.utility(state, player))
#     best_score = -infinity
#     beta = infinity
#     best_action = None
#     for a in game.actions(state):
#         v = min_value(game.result(state, a), best_score, beta, 1)
#         if v > best_score:
#             best_score = v
#             best_action = a
#     return best_action

# Converts 2-D coordinates of a matrix in a positive integer index
def coord2ind(x, y, s):
    return x + s*y

# Converts index of a matrix into 2-D coordinates
def ind2coord(i, s):
    return (int(i / s), i % s)

# Main function
# if __name__ == '__main__':

#     g = Game()
#     f = open("logfile.txt","w")
#     f.close()
#     try:
#         fileID = open(sys.argv[1], "r")
#     except IndexError:
#         print('Error: Filename not provided or invalid open/read')
#         sys.exit()
#     except IOError:
#         print("Error: couldn't open board file")
#         sys.exit()

#     s = g.load_board(fileID)
#     s.printState()

    # actions = g.actions(s)
    # print('actions: ' + str(actions))

    # print('\n\nTerminal: ' + str(g.terminal_test(s)))

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
    # print('move: ' + str(alphabeta_cutoff_search(s, g)))
