"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 20        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player



def mc_trial(board, player):
    
    """
    This function takes a current board and the next player to move.
    """
    current_status = board.check_win()    
    while current_status == None:   
        
        empty_list = board.get_empty_squares()
        length = len(empty_list)
    
        will_move = empty_list[random.randrange(0, length)]
        board.move(will_move[0], will_move[1], player)
        
        # return when the game is over
        current = board.check_win()   
        if current == provided.PLAYERX or current == provided.PLAYERO or current == provided.DRAW:
            break  
        
        # Switch player
        player = provided.switch_player(player)


def mc_update_scores(scores, board, player):
    
    """
    The function should score the completed board and update the scores grid.
    """

    # get the winner
    winner = board.check_win()
   
    # get the human (O)
    human = provided.switch_player(player)
    
    mc_match = 0
    mc_other = 0
    
    if winner == player:
        # winner is machine
        mc_match = SCORE_CURRENT
        mc_other = SCORE_OTHER * -1
    elif winner == human:
        # winner is human
        mc_match = SCORE_CURRENT * -1
        mc_other = SCORE_OTHER
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                scores[row][col] += mc_match
            elif board.square(row, col) == human:               
                scores[row][col] += mc_other
            else:              
                scores[row][col] += 0
                            
               
def get_best_move(board, scores):
    
    """
    This function takes a current board and a grid of scores. 
    """
    
    empty_list = board.get_empty_squares()
    length = len(empty_list)
    score_dic = {}
    
    if length == 0:
        return
    
    for empty_item in empty_list:
        score_dic[empty_item] = scores[empty_item[0]][empty_item[1]]
    
    values = list(score_dic.values())
    max_score = max(values)
    max_list = []
 
    for (row, col) in empty_list:
        if scores[row][col] == max_score:
            max_list.append((row, col))
    
    length_max_list = len(max_list) 
    will_move = max_list[random.randrange(0, length_max_list)]
    
    return (will_move[0], will_move[1])
        
    
    
    
def mc_move(board, player, trials):
    
    """
    The function should use the Monte Carlo simulation described above to return a move
    """
    
    scores = [ [0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    
    for dummy_item in range(trials):
        new_board = board.clone()
        mc_trial(new_board, player)
        mc_update_scores(scores, new_board, player)
        
        
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
