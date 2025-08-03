from collections import Counter
import itertools

class ScoringSystem:
    def __init__(self):
        self.scoring_rules = {
            '6_sequential': 1500,  # Increased from 1000
            '5_sequential': 800,   # Increased from 500
            '4_sequential': 600,   # Increased from 400
            '3_sequential': 400,   # Increased from 300
            '2_sequential': 250,   # Increased from 200
            'six_of_kind': 1200,     # Increased from 600
            'five_of_kind': 1000,    # Increased from 500
            'four_of_kind': 800,     # Increased from 400
            'three_of_kind': 300,    # Increased from 200
            'pair': 150,             # Increased from 100
            'two_pair': 700,         # Increased from 500
            'full_house': 1000       # Increased from 600
        }
    
    def calculate_score(self, dice_values, wild_dice):
        """Calculate the best possible score for the given dice"""
        # Handle wild dice by trying all possible values
        best_score = 0
        best_hand = ""
        best_calculation = ""
        
        if wild_dice:
            # Try all possible values for wild dice
            for wild_values in itertools.product(range(1, 7), repeat=len(wild_dice)):
                test_values = dice_values.copy()
                for i, wild_index in enumerate(wild_dice):
                    test_values[wild_index] = wild_values[i]
                
                score, hand, calculation = self._calculate_single_score(test_values)
                if score > best_score:
                    best_score = score
                    best_hand = hand
                    best_calculation = calculation
        else:
            best_score, best_hand, best_calculation = self._calculate_single_score(dice_values)
        
        return best_score, best_hand, best_calculation
    
    def _calculate_single_score(self, dice_values):
        """Calculate score for a single set of dice values"""
        counter = Counter(dice_values)
        sorted_values = sorted(dice_values)
        
        # Check for different combinations
        combinations = []
        
        # Check for six of a kind
        if any(count >= 6 for count in counter.values()):
            value = max(k for k, v in counter.items() if v >= 6)
            combinations.append(('six_of_kind', value, 6))
        
        # Check for five of a kind
        if any(count >= 5 for count in counter.values()):
            value = max(k for k, v in counter.items() if v >= 5)
            combinations.append(('five_of_kind', value, 5))
        
        # Check for four of a kind
        if any(count >= 4 for count in counter.values()):
            value = max(k for k, v in counter.items() if v >= 4)
            combinations.append(('four_of_kind', value, 4))
        
        # Check for full house (three of a kind + pair)
        if any(count >= 3 for count in counter.values()) and any(count >= 2 for k, count in counter.items() if count < 3):
            three_value = max(k for k, v in counter.items() if v >= 3)
            pair_value = max(k for k, v in counter.items() if v >= 2 and k != three_value)
            combinations.append(('full_house', three_value, 5))
        
        # Check for three of a kind
        if any(count >= 3 for count in counter.values()):
            value = max(k for k, v in counter.items() if v >= 3)
            combinations.append(('three_of_kind', value, 3))
        
        # Check for two pair
        if sum(1 for count in counter.values() if count >= 2) >= 2:
            pairs = [k for k, v in counter.items() if v >= 2]
            pairs.sort(reverse=True)
            combinations.append(('two_pair', pairs[0], 4))
        
        # Check for pair
        if any(count >= 2 for count in counter.values()):
            value = max(k for k, v in counter.items() if v >= 2)
            combinations.append(('pair', value, 2))
        
        # Check for sequential combinations
        sequential_score, sequential_hand, sequential_values = self._check_sequential(sorted_values)
        if sequential_score > 0:
            combinations.append(('sequential', 0, len(sequential_values), sequential_values))
        
        # Find the best combination
        best_combination = None
        best_score = 0
        
        for combo in combinations:
            if combo[0] == 'sequential':
                length = combo[3]
                sequence_values = combo[3]  # Fixed: sequential_values is at index 3, not 4
                score = self.scoring_rules.get(f'{length}_sequential', 0)
                # Add bonus for numbers in the sequential combination (DOUBLED)
                for value in sequence_values:
                    score += value * 200  # Doubled from 100 to 200
            else:
                score = self.scoring_rules.get(combo[0], 0)
                # Add bonus for the value of the combination (DOUBLED)
                score += combo[1] * 200 * combo[2]  # Doubled from 100 to 200
            
            if score > best_score:
                best_score = score
                best_combination = combo
        
        # Generate description and calculation
        if best_combination:
            hand_name, calculation = self._generate_description(best_combination)
            return best_score, hand_name, calculation
        
        return 0, "No scoring combination", "0"
    
    def _check_sequential(self, sorted_values):
        """Check for sequential combinations"""
        best_score = 0
        best_hand = ""
        best_sequence = []
        
        # Check for different lengths of sequences
        for length in range(2, 7):
            for i in range(len(sorted_values) - length + 1):
                sequence = sorted_values[i:i+length]
                if self._is_sequential(sequence):
                    score = self.scoring_rules.get(f'{length}_sequential', 0)
                    if score > best_score:
                        best_score = score
                        best_hand = f"{length}-straight"
                        best_sequence = sequence
        
        return best_score, best_hand, best_sequence
    
    def _is_sequential(self, values):
        """Check if values form a sequential sequence"""
        for i in range(len(values) - 1):
            if values[i + 1] - values[i] != 1:
                return False
        return True
    
    def _generate_description(self, combination):
        """Generate a description and calculation for the combination"""
        combo_type, value, count = combination[:3]
        
        if combo_type == 'sequential':
            length = count
            hand_name = f"{length}-straight"
            base_score = self.scoring_rules.get(f'{length}_sequential', 0)
            bonus_score = sum(combination[3]) * 200  # Doubled from 100 to 200
            total_score = base_score + bonus_score
            calculation = f"{base_score} + {bonus_score} bonus = {total_score}"
        else:
            # Map combination types to readable names
            name_map = {
                'six_of_kind': 'Six of a Kind',
                'five_of_kind': 'Five of a Kind',
                'four_of_kind': 'Four of a Kind',
                'three_of_kind': 'Three of a Kind',
                'pair': 'Pair',
                'two_pair': 'Two Pair',
                'full_house': 'Full House'
            }
            
            hand_name = name_map.get(combo_type, combo_type)
            base_score = self.scoring_rules.get(combo_type, 0)
            bonus_score = value * 200 * count  # Doubled from 100 to 200
            total_score = base_score + bonus_score
            calculation = f"{base_score} + {bonus_score} bonus = {total_score}"
        
        return hand_name, calculation 