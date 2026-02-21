'''
Created on 2025/02/11

@author: sin
'''

import psutil
import os

from mancala2p import Mancala    
from itertools import combinations_with_replacement, permutations

# def consistent_prev_move(board : Board2p, player_id : int, start : int, amount: int):
#     if board.data[start] != 0 :
#         return False
#     placed = [0] * len(board.data)
#     for ix in range(start+1, start+amount) :
#         placed[ix % len(board.data)] += 1
#         print(placed, ix, board.data[ix % len(board.data)])
#         if board.is_store(ix) :
#             print('yes')
#         if board.is_store(ix) or board.data[ix % len(board.data)] >= placed[ix] :
#             continue
#         return False
#     return True


# def find_combinations_simple(n=13, target_sum=25):
#     """
#     Find all combinations of n non-negative integers that sum to target_sum.
#
#     Time Complexity: O(C(n+target_sum-1, n))
#     Space Complexity: O(number of valid combinations)
#     """
#     combinations = []
#
#     # Generate combinations with replacement from range up to target_sum
#     for combo in combinations_with_replacement(range(target_sum + 1), n):
#         if sum(combo) == target_sum:
#             combinations.append(combo)
#
#     return combinations
    
def find_combinations_dp(n=13, target_sum=25):
    """
    Use recursion with memoization to find combinations efficiently.
    
    Time Complexity: O(C(n+target_sum-1, n))
    Space Complexity: O(n * target_sum) for memoization
    """
    combinations = set()
    
    def backtrack(remaining_count, current_sum, current_combo, start_value):
        # Base cases
        if remaining_count == 0:
            if current_sum == 0:
                combinations.add(tuple(current_combo))
            return
        
        if current_sum < 0:
            return
        
        # Pruning: if we need remaining_count more integers and each is at least start_value
        # if current_sum < start_value * remaining_count:
        #     return
        
        if sum(current_combo[:(n>>1)-1]) > 0 and sum(current_combo[(n>>1):n-1]) > 0 :
            return
                            
        # Try all possible values for the next position
        for value in range(start_value, current_sum + 1):
            current_combo.append(value)
            backtrack(remaining_count - 1, current_sum - value, current_combo, 0) #value)
            current_combo.pop()
    
    backtrack(n, target_sum, [], 0)
    return combinations


if __name__ == '__main__':
    # Usage
    import time

    print("=" * 50)
    
    # Test Approach 2 (Most practical)
    start = time.time()
    result = find_combinations_dp(10, 24)
    elapsed = time.time() - start
    print(f"\nApproach 2 (DP Backtracking):")
    print(f"  Found: {len(result)} combinations")
    print(f"  Time: {elapsed:.4f} seconds")
    
    settled = set()
    for boardt in sorted(result):
        n = len(boardt)
        print(boardt)
        if sum(boardt[:(n>>1) -1]) == 0 :
            settled.add(boardt + (0, ))
        if sum(boardt[(n>>1):2*n - 1]) == 0 :
            settled.add(boardt + (1, ))
    
    for e in sorted(settled)[80000:80000+500]:
        print(e)
    print(f"  Settled: {len(settled)} boards")
