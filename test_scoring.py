#!/usr/bin/env python3
"""
Test script for the Dicey Dilemma scoring system
"""

from scoring import ScoringSystem

def test_scoring():
    """Test various dice combinations"""
    scoring = ScoringSystem()
    
    test_cases = [
        # Test cases: (dice_values, expected_hand_type, description)
        ([1, 1, 1, 1, 1, 1], "Six of a Kind", "Six 1's"),
        ([2, 2, 2, 2, 2, 2], "Six of a Kind", "Six 2's"),
        ([1, 1, 1, 1, 1, 6], "Five of a Kind", "Five 1's"),
        ([1, 1, 1, 1, 2, 3], "Four of a Kind", "Four 1's"),
        ([1, 1, 1, 2, 2, 3], "Full House", "Three 1's + Two 2's"),
        ([1, 1, 2, 2, 3, 4], "Two Pair", "Two pairs"),
        ([1, 1, 1, 2, 3, 4], "Three of a Kind", "Three 1's"),
        ([1, 1, 2, 3, 4, 5], "Pair", "Pair of 1's"),
        ([1, 2, 3, 4, 5, 6], "6-straight", "Six sequential"),
        ([1, 2, 3, 4, 5, 1], "5-straight", "Five sequential"),
        ([1, 2, 3, 4, 1, 2], "4-straight", "Four sequential"),
        ([1, 2, 3, 1, 2, 3], "3-straight", "Three sequential"),
        ([1, 2, 1, 2, 3, 4], "2-straight", "Two sequential"),
        ([1, 3, 5, 2, 4, 6], "No scoring combination", "No combinations"),
    ]
    
    print("Testing Dicey Dilemma Scoring System")
    print("=" * 50)
    
    for i, (dice_values, expected_hand, description) in enumerate(test_cases, 1):
        score, hand, calculation = scoring.calculate_score(dice_values, [])
        print(f"Test {i}: {description}")
        print(f"  Dice: {dice_values}")
        print(f"  Result: {hand} - {calculation}")
        print(f"  Score: {score}")
        print(f"  Expected: {expected_hand}")
        print(f"  {'✓ PASS' if expected_hand in hand else '✗ FAIL'}")
        print()
    
    # Test wild card dice
    print("Testing Wild Card Dice")
    print("=" * 30)
    dice_with_wild = [1, 1, 1, 0, 0, 6]  # 0 represents wild cards
    wild_indices = [3, 4]  # Indices of wild cards
    score, hand, calculation = scoring.calculate_score(dice_with_wild, wild_indices)
    print(f"Dice with wild cards: {dice_with_wild}")
    print(f"Wild card indices: {wild_indices}")
    print(f"Result: {hand} - {calculation}")
    print(f"Score: {score}")
    print()

if __name__ == "__main__":
    test_scoring() 