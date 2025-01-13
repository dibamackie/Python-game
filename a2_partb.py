from a1_partd import overflow
from a1_partc import Queue

# This function duplicates and returns the board. You may find this useful
def copy_board(board):
        current_board = []
        height = len(board)
        for i in range(height):
            current_board.append(board[i].copy())
        return current_board


# this function is your evaluation function for the board
def evaluate_board(board, player):
    """
    Figures out how good or bad the board is for a given player.
    
    Args:
        board (list[list[int]]): The game board.
        player (int): The player we're checking for (positive or negative number).
    
    Returns:
        float: Score of the board:
            - inf if the player wins
            - -inf if the opponent wins
            - A calculated score otherwise
    """
    if not board:
        return 0  # No board, no score
    
    rows, cols = len(board), len(board[0])
    score = 0
    unified = True
    first_piece = None

    # Check if one player controls the whole board
    for i in range(rows):
        for j in range(cols):
            if board[i][j] != 0:
                if first_piece is None:
                    first_piece = board[i][j] > 0
                elif (board[i][j] > 0) != first_piece:
                    unified = False
                    break
        if not unified:
            break

    if unified and first_piece is not None:
        return float('inf') if first_piece == (player > 0) else float('-inf')

    # Give weights to different positions and calculate score
    for i in range(rows):
        for j in range(cols):
            if board[i][j] != 0:
                weight = 1  # Default weight
                if (i in [0, rows - 1]) and (j in [0, cols - 1]):  # Corners are good
                    weight = 3
                elif i in [0, rows - 1] or j in [0, cols - 1]:  # Edges are okay too
                    weight = 2
                score += weight * abs(board[i][j]) * (1 if (board[i][j] > 0) == (player > 0) else -1)

    return score

class GameTree:
    """
    This class builds a tree of all possible moves and uses minimax to find the best one.
    """

    class Node:
        """
        Represents a spot in the tree. Holds the board and the score for that position.
        """
        def __init__(self, board, depth, player, tree_height=4):
            self.board = copy_board(board)  # Make a copy of the board for this node
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            self.children = []  # Nodes that come after this one
            self.score = None  # Will hold the minimax score later

    def __init__(self, board, player, tree_height=4):
        """
        Sets up the game tree and starts building it.
        
        Args:
            board (list[list[int]]): The starting board.
            player (int): The player we're finding moves for.
            tree_height (int): How far ahead to look in the tree.
        """
        self.player = player
        self.board = copy_board(board)
        self.tree_height = tree_height
        self.root = self.Node(self.board, 0, player, tree_height)
        self._build_tree(self.root)  # Build the tree starting from the root
        self._apply_minimax(self.root, True)  # Calculate the scores using minimax

    def _get_valid_moves(self, board, current_player):
        """
        Find all the places the current player can move.
        
        Args:
            board (list[list[int]]): The current board.
            current_player (int): The player making the move.
        
        Returns:
            list[tuple[int, int]]: List of (row, col) for valid moves.
        """
        moves = []
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == 0 or (cell > 0) == (current_player > 0):
                    moves.append((i, j))  # Can move here
        return moves

    def _make_move(self, board, move, player):
        """
        Simulates making a move on the board.
        
        Args:
            board (list[list[int]]): The current board.
            move (tuple[int, int]): Where to move (row, col).
            player (int): The player making the move.
        
        Returns:
            list[list[int]]: The board after the move.
        """
        new_board = copy_board(board)
        row, col = move
        if new_board[row][col] == 0:
            new_board[row][col] = player
        else:
            new_board[row][col] = player * (abs(new_board[row][col]) + 1)

        queue = Queue()
        overflow(new_board, queue)  # Handle overflow if necessary

        while not queue.is_empty():
            new_board = queue.dequeue()  # Keep processing until done

        return new_board

    def _build_tree(self, node):
        """
        Builds the game tree by adding all possible moves for this node.
        
        Args:
            node (Node): The current node we're building from.
        """
        if node.depth == node.tree_height:  # Stop if we've gone deep enough
            node.score = evaluate_board(node.board, self.player)
            return

        current_turn = self.player if node.depth % 2 == 0 else -self.player
        moves = self._get_valid_moves(node.board, current_turn)

        for move in moves:
            next_board = self._make_move(node.board, move, current_turn)
            child_node = self.Node(next_board, node.depth + 1, current_turn, node.tree_height)
            node.children.append(child_node)
            self._build_tree(child_node)

    def _apply_minimax(self, node, is_max_player):
        """
        Calculates the best score for each node using the minimax algorithm.
        
        Args:
            node (Node): The node to calculate scores for.
            is_max_player (bool): True if it's the maximizing player's turn.
        
        Returns:
            float: The score for this node.
        """
        if not node.children:  # If no children, it's a leaf
            node.score = evaluate_board(node.board, self.player)
            return node.score

        scores = [self._apply_minimax(child, not is_max_player) for child in node.children]
        node.score = max(scores) if is_max_player else min(scores)
        return node.score

    def get_move(self):
        """
        Finds the best move for the current player.
        
        Returns:
            tuple[int, int]: The coordinates of the best move.
        """
        if not self.root.children:  # No moves? Default to (0, 0)
            return (0, 0)

        valid_moves = self._get_valid_moves(self.board, self.player)
        best_move = max(zip(valid_moves, self.root.children), key=lambda x: x[1].score)[0]
        return best_move

    def clear_tree(self):
        """
        Clears the tree from memory.
        """
        def _clear(node):
            for child in node.children:
                _clear(child)
            node.children.clear()

        _clear(self.root)
        self.root = None
