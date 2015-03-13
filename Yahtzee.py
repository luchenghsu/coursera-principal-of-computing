"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = {}
    
    for item in hand:
        if item not in scores:
            scores[item] = item
        else:
            scores[item] += item

    return max(scores.values())



def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    set_of_dices_after_rolled = gen_all_sequences(set(dummy_i for dummy_i in range(1, num_die_sides+1)), num_free_dice)
    
    total_value = 0
    
    for item in set_of_dices_after_rolled:
         total_value += score(held_dice + item)
    
    exptected_value = float(total_value) / (num_die_sides ** num_free_dice)
    
    return exptected_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    complete_set = list(hand)
    binary_counts =[bin(x)[2:].rjust(len(hand),'0') for x in range(2**len(hand))]        
         
    power_set = set([()])
    
    for count in binary_counts:
        power_set.add(tuple([complete_set[i] for i in range(len(count))
                         if count[i] == '1']))
    
        
    return power_set 

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    expected_values = {}
    for item in gen_all_holds(hand):      
        expected_values[item] = expected_value(item, num_die_sides, len(hand)-len(item)) 
    
    key = expected_values.keys()[expected_values.values().index(max(expected_values.values()))]
    return (max(expected_values.values()), key)


