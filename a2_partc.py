from a1_partc import Stack #importing the stack class form the first assignmnet


# undo feature class
class UndoFeature:
    def __init__(self): 
        self.state_stack = Stack()  #start the stack to store the game play 

    def save_state(self, board_state):
        self.state_stack.push(board_state) #push the current board state to the stack 

    def undo_last_move(self, board):
        if not self.state_stack.is_empty():
            previous_state = self.state_stack.pop() #setting the current state of the stack one less as the privouse state 
            board.set(previous_state) #updating the board 
            return True # if undo was successful
        return False # if there was nothing to save
    
