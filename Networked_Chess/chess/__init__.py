from chess.board import *

if __name__ == "__main__":
    p = Board()
    
    p.printBoard()
    print()
    
    p.move('e', 2, 'e', 4)
    
    p.printBoard()
    print()
    
    p.move('d', 7, 'd', 5)
    
    p.printBoard()
    print()
    
    p.move('e', 4, 'd', 5)
    
    p.printBoard()