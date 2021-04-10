'''
Created on Apr 10, 2021

@author: ERICSCHELL
'''
class Pawn:
    def __init__(self, color, x, y):
        self.color = color
        self.alive = True
        self.x = x
        self.y = y
        if self.color == 'w':
            self.symbol = 'P'
        else:
            self.symbol = 'p'
    
    def taken(self):
        self.alive = False
        
    def move(self, x, y):
        self.x = x
        self.y = y
        
class Rook:
    def __init__(self, color, x, y):
        self.color = color
        self.alive = True
        self.x = x
        self.y = y
        if self.color == 'w':
            self.symbol = 'R'
        else:
            self.symbol = 'r'
    
    def taken(self):
        self.alive = False
        
    def move(self, x, y):
        self.x = x
        self.y = y
        
class Knight:
    def __init__(self, color, x, y):
        self.color = color
        self.alive = True
        self.x = x
        self.y = y
        if self.color == 'w':
            self.symbol = 'N'
        else:
            self.symbol = 'n'
    
    def taken(self):
        self.alive = False
        
    def move(self, x, y):
        self.x = x
        self.y = y  
        
class Bishop:
    def __init__(self, color, x, y):
        self.color = color
        self.alive = True
        self.x = x
        self.y = y
        if self.color == 'w':
            self.symbol = 'B'
        else:
            self.symbol = 'b'
    
    def taken(self):
        self.alive = False
        
    def move(self, x, y):
        self.x = x
        self.y = y  
        
class Queen:
    def __init__(self, color, x, y):
        self.color = color
        self.alive = True
        self.x = x
        self.y = y
        if self.color == 'w':
            self.symbol = 'Q'
        else:
            self.symbol = 'q'
    
    def taken(self):
        self.alive = False
        
    def move(self, x, y):
        self.x = x
        self.y = y  
        
class King:
    def __init__(self, color, x, y):
        self.color = color
        self.alive = True
        self.x = x
        self.y = y
        if self.color == 'w':
            self.symbol = 'K'
        else:
            self.symbol = 'k'
    
    def taken(self):
        self.alive = False
        
    def move(self, x, y):
        self.x = x
        self.y = y
        
class Board:
    def __init__(self):
        self.P1 = Pawn('w', 'a', 2)
        self.P2 = Pawn('w', 'b', 2)
        self.P3 = Pawn('w', 'c', 2)
        self.P4 = Pawn('w', 'd', 2)
        self.P5 = Pawn('w', 'e', 2)
        self.P6 = Pawn('w', 'f', 2)
        self.P7 = Pawn('w', 'g', 2)
        self.P8 = Pawn('w', 'h', 2)
        self.R1 = Rook('w', 'a', 1)
        self.R2 = Rook('w', 'h', 1)
        self.N1 = Knight('w', 'b', 1)
        self.N2 = Knight('w', 'g', 1)
        self.B1 = Bishop('w', 'c', 1)
        self.B2 = Bishop('w', 'f', 1)
        self.Q = Queen('w', 'd', 1)
        self.K = King('w', 'e', 1)
        
        self.p1 = Pawn('b', 'a', 7)
        self.p2 = Pawn('b', 'b', 7)
        self.p3 = Pawn('b', 'c', 7)
        self.p4 = Pawn('b', 'd', 7)
        self.p5 = Pawn('b', 'e', 7)
        self.p6 = Pawn('b', 'f', 7)
        self.p7 = Pawn('b', 'g', 7)
        self.p8 = Pawn('b', 'h', 7)
        self.r1 = Rook('b', 'a', 8)
        self.r2 = Rook('b', 'h', 8)
        self.n1 = Knight('b', 'b', 8)
        self.n2 = Knight('b', 'g', 8)
        self.b1 = Bishop('b', 'c', 8)
        self.b2 = Bishop('b', 'f', 8)
        self.q = Queen('b', 'd', 8)
        self.k = King('b', 'e', 8)
        
        self.pieces = [self.P1, self.P2, self.P3, self.P4, self.P5, self.P6, self.P7, self.P8, self.R1, self.R2, self.N1, self.N2, self.B1, self.B2, self.Q, self.K,
                  self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.r1, self.r2, self.n1, self.n2, self.b1, self.b2, self.q, self.k]
        
        self.columns = dict.fromkeys(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        
        self.turn = 'w'
    
    def updateBoard(self):
        self.columns.clear()
        self.columns = dict.fromkeys(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        for i in self.pieces:
            if self.columns[i.x]:
                self.columns[i.x].append(i)
            else:
                self.columns[i.x] = [i]
    
    def find(self, x, y):
        for i in self.pieces:
            if i.x == x:
                if i.y == y:
                    if i.alive == True:
                        return i
        return False
    
    def move(self, fromX, fromY, toX, toY):
        #validate in GUI that x coords are lowercase a-h and y coords are 1-8
        
        f = self.find(fromX, fromY)
        
        if f != False and self.turn == f.color:
            t = self.find(toX, toY)
            
            if t != False:
                if self.turn != t.color:
                    t.taken()
                else:
                    return False 
                
            f.move(toX, toY)
            self.next()
    
    def next(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    
    def printBoard(self):
        self.updateBoard()
        for i in range(8, 0, -1):
            print(i, '|', end=' ')
            for key in self.columns:
                for value in self.columns[key]:
                    if value.y == i and value.alive == True:
                        temp = value.symbol
                print(temp, '|', end=' ')
                temp = '-'
            print('')
        print('    a   b   c   d   e   f   g   h')    
        
            