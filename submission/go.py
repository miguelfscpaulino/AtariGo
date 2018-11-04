import sys
import copy
import bisect

infinity = float('inf')


class State():
    """docstring for class State"""

    def __init__(self, mat, player, filled, dim, groups1, groups2, zeros1, zeros2):
        self.mat = mat
        self.player = player
        self.filled = filled
        self.dim = dim
        self.drawflag = False
        self.terminalflag = False
        self.groups1 = groups1
        self.groups2 = groups2
        self.zeros1 = zeros1
        self.zeros2 = zeros2
        

    def surronding_zeros(self, pos, dim, filled):

        zeros = []

        if (pos - dim) >= 0:
            for item in filled:
                if item[1] == (pos-dim):
                    break
                elif item[1] > (pos-dim):
                    zeros.append(pos-dim)
                    break

        if (pos + dim) < dim*dim:
            for item in filled:
                if item[1] == (pos+dim):
                    break
                elif item[1] > (pos+dim) or item == filled[-1]:
                    zeros.append(pos+dim)
                    break

        if (pos % dim) != 0:
            for item in filled:
                if item[1] == pos-1:
                    break
                elif item[1] > pos-1:
                    zeros.append(pos-1)
                    break

        if ((pos+1) % dim) != 0:
            for item in filled:
                if item[1] == (pos+1):
                    break
                elif item[1] > (pos+1) or item == filled[-1]:
                    zeros.append(pos+1)
                    break

        return zeros


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

    def printState(self):
        print('State::')
        print('Player: ' + str(self.player))
        print('Board: ')
        print(self.mat)
        print('Occupied positions: ')
        print(self.filled)
        print('Groups1: ' + str(self.groups1))
        print('Zeros1: ' + str(self.zeros1))
        print('Groups2: ' + str(self.groups2))
        print('Zeros2: ' + str(self.zeros2))


class Game():
    """docstring for class Game"""

    def getState(self):
        return self.state

    def to_move(self, s):
        #returns the player to move next, given the state "s"
        return s.getPlayer()

    def terminal_test(self, s):
        #checks if state "s" is terminal

        zeros1 = s.getZeros1()
        zeros2 = s.getZeros2()

        for zeros in [zeros1, zeros2]:
            for i in zeros:
                if len(i) == 0:
                    s.setTerminalFlag(True)
                    s.setDrawFlag(False)
                    return True


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
        
        if p ==1:
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
            groups = copy.deepcopy(s.getGroups1())
            zeros = copy.deepcopy(s.getZeros1())
            zerosCont = copy.deepcopy(s.getZeros2())
            player = 2
        else:
            groups = copy.deepcopy(s.getGroups2())
            zeros = copy.deepcopy(s.getZeros2())
            zerosCont = copy.deepcopy(s.getZeros1())
            player = 1

        mat = copy.deepcopy(s.getMat())
        filled = copy.deepcopy(s.getFilled())
        dim = s.getDim()
        

        ind = coord2ind(a[2]-1, a[1]-1, dim)

        mat[a[1]-1][a[2]-1] = a[0]
        filled.append((a[0], ind))
        filled.sort(key=lambda x:x[1])

        UpGroup=[]
        DownGroup=[]
        LeftGroup=[]
        RightGroup=[]
        joinedUp=False
        joinedDown=False
        joinedLeft=False
        joinedRight = False


        if (ind - dim) >= 0 and mat[a[1]-2][a[2]-1] == a[0]:
            for k in groups:
                if (ind - dim) in k:
                    k.append(ind)
                    joinedUp=True
                    break


        if (ind + dim) < dim*dim and mat[a[1]][a[2]-1] == a[0]:
            if joinedUp:

                cntup_flag = True
                cntup = 0
                cntdown_flag = True
                cntdown = 0
                DownGroup = []
                UpGroup = []
                for k in groups:
                    if ind in k:
                        cntup_flag = False
                        UpGroup=k
                    if (ind+dim) in k:
                        cntdown_flag = False
                        DownGroup=k
                    if UpGroup and DownGroup:
                        break
                    if cntup_flag:
                        cntup += 1
                    if cntdown_flag:
                        cntdown += 1
                if UpGroup is not DownGroup:
                    for k in DownGroup:
                        UpGroup.append(k)
                    groups.remove(DownGroup)
                    for k in zeros[cntdown]:
                        zeros[cntup].append(k)
                    zeros.remove(zeros[cntdown])
            else:
                for k in groups:
                    if (ind+dim) in k:
                        k.append(ind)
                        joinedDown = True
                        break

        if (ind%dim) != 0 and mat[a[1]-1][a[2]-2] == a[0]:
            if joinedUp:

                cntup_flag = True
                cntup = 0
                cntleft_flag = True
                cntleft = 0
                LeftGroup = []
                UpGroup = []
                for k in groups:
                    if ind in k:
                        cntup_flag = False
                        UpGroup=k
                    if (ind-1) in k:
                        cntleft_flag = False
                        LeftGroup=k
                    if UpGroup and LeftGroup:
                        break
                    if cntup_flag:
                        cntup += 1
                    if cntleft_flag:
                        cntleft += 1
                if UpGroup is not LeftGroup:
                    for k in LeftGroup:
                        UpGroup.append(k)
                    groups.remove(LeftGroup)
                    for k in zeros[cntleft]:
                        zeros[cntup].append(k)
                    zeros.remove(zeros[cntleft])
            elif joinedDown:

                cntdown_flag = True
                cntdown = 0
                cntleft_flag = True
                cntleft = 0
                DownGroup = []
                LeftGroup = []
                for k in groups:
                    if ind in k:
                        cntdown_flag = False
                        DownGroup=k
                    if (ind-1) in k:
                        cntleft_flag = False
                        LeftGroup=k
                    if DownGroup and LeftGroup:
                        break
                    if cntdown_flag:
                        cntdown += 1
                    if cntleft_flag:
                        cntleft += 1
                if DownGroup is not LeftGroup:
                    for k in LeftGroup:
                        DownGroup.append(k)
                    groups.remove(LeftGroup)
                    for k in zeros[cntleft]:
                        zeros[cntdown].append(k)
                    zeros.remove(zeros[cntleft])
            else:
                for k in groups:
                    if (ind-1) in k:
                        k.append(ind)
                        joinedLeft = True
                        break

        if (ind+1)%dim != 0 and mat[a[1]-1][a[2]] == a[0]:
            if joinedUp:

                cntup_flag = True
                cntup = 0
                cntright_flag = True
                cntright = 0
                UpGroup = []
                RightGroup = []
                for k in groups:
                    if ind in k:
                        cntup_flag = False
                        UpGroup=k
                    if (ind+1) in k:
                        cntright_flag = False
                        RightGroup=k
                    if UpGroup and RightGroup:
                        break
                    if cntup_flag:
                        cntup += 1
                    if cntright_flag:
                        cntright += 1
                if UpGroup is not RightGroup:
                    for k in RightGroup:
                        UpGroup.append(k)
                    groups.remove(RightGroup)
                    for k in zeros[cntright]:
                        zeros[cntup].append(k)
                    zeros.remove(zeros[cntright])
            elif joinedDown:

                cntdown_flag = True
                cntdown = 0
                cntright_flag = True
                cntright = 0
                DownGroup = []
                RightGroup = []
                for k in groups:
                    if ind in k:
                        cntdown_flag = False
                        DownGroup=k
                    if (ind+1) in k:
                        cntright_flag = False
                        RightGroup=k
                    if DownGroup and RightGroup:
                        break
                    if cntdown_flag:
                        cntdown += 1
                    if cntright_flag:
                        cntright += 1
                if DownGroup is not RightGroup:
                    for k in RightGroup:
                        DownGroup.append(k)
                    groups.remove(RightGroup)
                    for k in zeros[cntright]:
                        zeros[cntdown].append(k)
                    zeros.remove(zeros[cntright])
            elif joinedLeft:

                cntleft_flag = True
                cntleft = 0
                cntright_flag = True
                cntright = 0
                LeftGroup = []
                RightGroup = []
                for k in groups:
                    if ind in k:
                        cntleft_flag = False
                        LeftGroup=k
                    if (ind+1) in k:
                        cntright_flag = False
                        RightGroup=k
                    if LeftGroup and RightGroup:
                        break
                    if cntleft_flag:
                        cntleft += 1
                    if cntright_flag:
                        cntright += 1
                if LeftGroup is not RightGroup:
                    for k in RightGroup:
                        LeftGroup.append(k)
                    groups.remove(RightGroup)
                    for k in zeros[cntright]:
                        zeros[cntleft].append(k)
                    zeros.remove(zeros[cntright])
            else:
                for k in groups:
                    if (ind+1) in k:
                        k.append(ind)
                        joinedRight = True
                        break

        if not joinedUp and not joinedDown and not joinedLeft and not joinedRight:
            groups.append([ind])
            zeros.append(s.surronding_zeros(ind, dim, filled))

        for i in range(len(zeros)):
            if ind in zeros[i]:
                for k in s.surronding_zeros(ind, dim, filled):
                    zeros[i].append(k)
            zeros[i] = list(set(zeros[i]))
            if ind in zeros[i]:
                zeros[i].remove(ind)
        
        for i in range(len(zerosCont)):
            if ind in zerosCont[i]:
                zerosCont[i].remove(ind)

        #for zeros in [zeros1, zeros2]:
        #    for i in zeros:
        #        while ind in i:
        #            i.remove(ind)

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

        for i in aux:
            
            if i[0] == 1:
                groups = groups1
            else:
                groups = groups2

            joined=False
            coord = ind2coord(i[1],dim)

            if (i[1] - dim) >= 0 and mat[coord[0]-1][coord[1]] == i[0]:
                for k in groups:
                    if (i[1] - dim) in k:
                        k.append(i[1])
                        joined=True
                        break

            if (i[1]%dim) != 0 and mat[coord[0]][coord[1]-1] == i[0]:
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


        
        for (groups, zeros) in [(groups1, zeros1),(groups2, zeros2)]:
            
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

        self.state = State(mat, player, aux, dim, groups1, groups2, zeros1, zeros2)
        return self.state

# Converts 2-D coordinates of a matrix in a positive integer index
def coord2ind(x, y, s):
    return x + s*y

# Converts index of a matrix into 2-D coordinates
def ind2coord(i, s):
    return (int(i / s), i % s)