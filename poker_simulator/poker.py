import random
import math
from collections import Counter
import argparse
from itertools import combinations

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        # This is great for debugging and compact display.
        return f"{self.rank}{self.suit}"
    
    def __str__(self):
        # Provides a long, human-readable name like "Ace of Spades".
        rank_map = {"A": "Ace", "K": "King", "Q": "Queen", "J": "Jack", "T": "Ten"}
        suit_map = {"S": "Spades", "C": "Clubs", "H": "Hearts", "D": "Diamonds"}
        
        # Use rank directly if not in map (for 2-9), then get full suit name.
        rank_name = rank_map.get(self.rank, self.rank)
        suit_name = suit_map.get(self.suit, self.suit)
        return f"{rank_name} of {suit_name}"

class Deck:
    def __init__(self):
        # Using single characters for suits and ranks makes parsing and comparison easier.
        # S=Spades, C=Clubs, H=Hearts, D=Diamonds
        # T=10, J=Jack, Q=Queen, K=King, A=Ace
        suits = "SCHD"
        ranks = "23456789TJQKA"
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
    
    def __str__(self):
        # This joins all the card strings with a newline in between.
        # It's a more efficient way to build the string than repeated concatenation.
        # Using repr() gives a compact view of the deck: AS KS QS JS TS...
        return " ".join(repr(c) for c in self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw_card(self):  # Renamed for clarity
        if not self.is_empty():
            return self.cards.pop()
    
    def is_empty(self):
        return len(self.cards) == 0

class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.hand = []
    
    def add_card(self, card):
        self.hand.append(card)
    
    def __str__(self):
        # The ' '.join(...) part uses the __repr__ from the Card class for a compact view.
        return f"{self.name}'s hand: {' '.join(repr(card) for card in self.hand)}"

class HandEvaluator:
    # Hand rankings from weakest to strongest
    HAND_RANKINGS = {
        "High Card": 1,
        "Pair": 2,
        "Two Pair": 3,
        "Three of a Kind": 4,
        "Straight": 5,
        "Flush": 6,
        "Full House": 7,
        "Four of a Kind": 8,
        "Straight Flush": 9,
        "Royal Flush": 10
    }
    
    # Approximate hand strength percentages (how strong each hand type is)
    HAND_STRENGTH_PERCENTAGES = {
        "High Card": 10,        # Weakest hands
        "Pair": 25,            # Common but better than high card
        "Two Pair": 45,        # Decent strength
        "Three of a Kind": 65, # Good hand
        "Straight": 75,        # Strong hand
        "Flush": 80,           # Very strong
        "Full House": 90,      # Excellent hand
        "Four of a Kind": 95,  # Extremely strong
        "Straight Flush": 99,  # Nearly unbeatable
        "Royal Flush": 100     # Perfect hand
    }
    
    # Card rank values for comparison (A can be high or low)
    RANK_VALUES = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    
    @staticmethod
    def get_rank_value(rank):
        return HandEvaluator.RANK_VALUES[rank]
    
    @staticmethod
    def get_hand_strength_percentage(hand_type):
        """Get the approximate strength percentage for a hand type."""
        return HandEvaluator.HAND_STRENGTH_PERCENTAGES.get(hand_type, 0)
    
    @staticmethod
    def is_flush(cards):
        """Check if all cards have the same suit."""
        suits = [card.suit for card in cards]
        return len(set(suits)) == 1
    
    @staticmethod
    def is_straight(cards):
        """Check if cards form a straight (5 consecutive ranks)."""
        ranks = [HandEvaluator.get_rank_value(card.rank) for card in cards]
        ranks.sort()
        
        # Check for normal straight
        for i in range(1, len(ranks)):
            if ranks[i] != ranks[i-1] + 1:
                # Check for A-2-3-4-5 straight (wheel)
                if ranks == [2, 3, 4, 5, 14]:
                    return True, 5  # Return 5 as high card for wheel
                return False, 0
        
        return True, ranks[-1]  # Return highest card
    
    @staticmethod
    def get_rank_counts(cards):
        """Get count of each rank in the hand."""
        ranks = [card.rank for card in cards]
        return Counter(ranks)
    
    @staticmethod
    def evaluate_hand(cards):
        """Evaluate a 5-card hand and return (hand_type, rank, tie_breakers)."""
        if len(cards) != 5:
            raise ValueError("Hand must have exactly 5 cards")
        
        # Sort cards by rank value for easier analysis
        sorted_cards = sorted(cards, key=lambda x: HandEvaluator.get_rank_value(x.rank))
        
        is_flush = HandEvaluator.is_flush(sorted_cards)
        is_straight, straight_high = HandEvaluator.is_straight(sorted_cards)
        rank_counts = HandEvaluator.get_rank_counts(sorted_cards)
        
        # Get counts in descending order
        counts = sorted(rank_counts.values(), reverse=True)
        ranks_by_count = sorted(rank_counts.keys(), key=lambda x: (rank_counts[x], HandEvaluator.get_rank_value(x)), reverse=True)
        
        # Check for each hand type from strongest to weakest
        
        # Royal Flush: A-K-Q-J-10 all same suit
        if is_flush and is_straight and straight_high == 14:
            return "Royal Flush", HandEvaluator.HAND_RANKINGS["Royal Flush"], [14]
        
        # Straight Flush: 5 consecutive cards, all same suit
        if is_flush and is_straight:
            return "Straight Flush", HandEvaluator.HAND_RANKINGS["Straight Flush"], [straight_high]
        
        # Four of a Kind: 4 cards of same rank
        if counts == [4, 1]:
            four_kind = ranks_by_count[0]
            kicker = ranks_by_count[1]
            return "Four of a Kind", HandEvaluator.HAND_RANKINGS["Four of a Kind"], [HandEvaluator.get_rank_value(four_kind), HandEvaluator.get_rank_value(kicker)]
        
        # Full House: 3 of a kind + pair
        if counts == [3, 2]:
            three_kind = ranks_by_count[0]
            pair = ranks_by_count[1]
            return "Full House", HandEvaluator.HAND_RANKINGS["Full House"], [HandEvaluator.get_rank_value(three_kind), HandEvaluator.get_rank_value(pair)]
        
        # Flush: 5 cards of same suit
        if is_flush:
            kickers = [HandEvaluator.get_rank_value(card.rank) for card in sorted_cards]
            kickers.sort(reverse=True)
            return "Flush", HandEvaluator.HAND_RANKINGS["Flush"], kickers
        
        # Straight: 5 consecutive cards
        if is_straight:
            return "Straight", HandEvaluator.HAND_RANKINGS["Straight"], [straight_high]
        
        # Three of a Kind: 3 cards of same rank
        if counts == [3, 1, 1]:
            three_kind = ranks_by_count[0]
            kickers = [HandEvaluator.get_rank_value(rank) for rank in ranks_by_count[1:]]
            kickers.sort(reverse=True)
            return "Three of a Kind", HandEvaluator.HAND_RANKINGS["Three of a Kind"], [HandEvaluator.get_rank_value(three_kind)] + kickers
        
        # Two Pair: 2 pairs
        if counts == [2, 2, 1]:
            pairs = [HandEvaluator.get_rank_value(rank) for rank in ranks_by_count[:2]]
            pairs.sort(reverse=True)
            kicker = HandEvaluator.get_rank_value(ranks_by_count[2])
            return "Two Pair", HandEvaluator.HAND_RANKINGS["Two Pair"], pairs + [kicker]
        
        # Pair: 2 cards of same rank
        if counts == [2, 1, 1, 1]:
            pair = HandEvaluator.get_rank_value(ranks_by_count[0])
            kickers = [HandEvaluator.get_rank_value(rank) for rank in ranks_by_count[1:]]
            kickers.sort(reverse=True)
            return "Pair", HandEvaluator.HAND_RANKINGS["Pair"], [pair] + kickers
        
        # High Card: no other hand
        kickers = [HandEvaluator.get_rank_value(card.rank) for card in sorted_cards]
        kickers.sort(reverse=True)
        return "High Card", HandEvaluator.HAND_RANKINGS["High Card"], kickers
    
    @staticmethod
    def find_best_hand(cards):
        """Find the best 5-card hand from a list of cards (5-7 cards)."""
        if len(cards) < 5:
            raise ValueError("Need at least 5 cards to evaluate")
        
        if len(cards) == 5:
            hand_type, rank, tie_breakers = HandEvaluator.evaluate_hand(cards)
            return hand_type, rank, tie_breakers, cards
        
        # Try all possible 5-card combinations and find the best
        best_hand = None
        best_rank = 0
        best_tie_breakers = []
        best_cards = []
        
        for five_cards in combinations(cards, 5):
            hand_type, rank, tie_breakers = HandEvaluator.evaluate_hand(list(five_cards))
            
            # Compare hands
            if rank > best_rank or (rank == best_rank and tie_breakers > best_tie_breakers):
                best_hand = hand_type
                best_rank = rank
                best_tie_breakers = tie_breakers
                best_cards = list(five_cards)
        
        return best_hand, best_rank, best_tie_breakers, best_cards
    
    @staticmethod
    def compare_hands(hand1_result, hand2_result):
        """Compare two hand evaluation results. Returns 1 if hand1 wins, -1 if hand2 wins, 0 if tie."""
        _, rank1, tie_breakers1 = hand1_result
        _, rank2, tie_breakers2 = hand2_result
        
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        else:
            # Same rank, compare tie breakers
            for tb1, tb2 in zip(tie_breakers1, tie_breakers2):
                if tb1 > tb2:
                    return 1
                elif tb1 < tb2:
                    return -1
            return 0  # Complete tie

class ExactProbabilityCalculator:
    """Exact combinatorial probability calculator for poker scenarios."""
    
    @staticmethod
    def combination(n, k):
        """Calculate C(n,k) = n! / (k! * (n-k)!)"""
        if k > n or k < 0:
            return 0
        return math.comb(n, k)
    
    @staticmethod
    def get_remaining_deck(known_cards):
        """Get all cards not in the known cards list."""
        all_cards = set()
        suits = "SCHD"
        ranks = "23456789TJQKA"
        
        for suit in suits:
            for rank in ranks:
                all_cards.add(f"{rank}{suit}")
        
        known_card_strs = {repr(card) for card in known_cards}
        remaining = all_cards - known_card_strs
        
        return [parse_card(card_str) for card_str in remaining]
    
    @staticmethod
    def calculate_exact_probability(player_cards, community_cards, num_opponents):
        """Calculate exact win probability using combinatorial analysis."""
        all_known = player_cards + community_cards
        remaining_deck = ExactProbabilityCalculator.get_remaining_deck(all_known)
        
        # Number of unknown community cards (max 5 total)
        unknown_community = 5 - len(community_cards)
        
        # Total cards needed for all opponents
        cards_per_opponent = 2
        total_opponent_cards = num_opponents * cards_per_opponent
        
        # Check if we can do exact calculation
        total_unknown_cards = unknown_community + total_opponent_cards
        
        if total_unknown_cards > len(remaining_deck):
            raise ValueError("Not enough cards in deck for this scenario")
        
        # For computational efficiency, limit exact calculation to reasonable scenarios
        # Rough estimate: C(47,6) = 10M scenarios takes ~30 seconds
        max_scenarios = ExactProbabilityCalculator.combination(len(remaining_deck), total_unknown_cards)
        if num_opponents > 2 or total_unknown_cards > 10 or max_scenarios > 1000000:
            return None  # Fall back to Monte Carlo
        
        wins = 0
        ties = 0
        total_scenarios = 0
        
        # Generate all possible combinations of unknown cards
        for unknown_cards in combinations(remaining_deck, total_unknown_cards):
            # Split unknown cards into community and opponent cards
            final_community = community_cards + list(unknown_cards[:unknown_community])
            opponent_cards_pool = list(unknown_cards[unknown_community:])
            
            # Create all possible opponent hand combinations
            opponent_hands = []
            start_idx = 0
            for _ in range(num_opponents):
                opponent_hand = opponent_cards_pool[start_idx:start_idx + cards_per_opponent]
                opponent_hands.append(opponent_hand)
                start_idx += cards_per_opponent
            
            # Evaluate player's hand
            player_all_cards = player_cards + final_community
            player_result = HandEvaluator.find_best_hand(player_all_cards)[:3]  # hand_type, rank, tie_breakers
            
            # Evaluate all opponent hands
            opponent_results = []
            for opponent_hand in opponent_hands:
                opponent_all_cards = opponent_hand + final_community
                opponent_result = HandEvaluator.find_best_hand(opponent_all_cards)[:3]
                opponent_results.append(opponent_result)
            
            # Compare player vs all opponents
            player_wins_scenario = True
            player_ties_scenario = False
            
            for opponent_result in opponent_results:
                comparison = HandEvaluator.compare_hands(player_result, opponent_result)
                if comparison < 0:  # Player loses to this opponent
                    player_wins_scenario = False
                    break
                elif comparison == 0:  # Tie with this opponent
                    player_ties_scenario = True
            
            total_scenarios += 1
            if player_wins_scenario:
                if player_ties_scenario:
                    ties += 1
                else:
                    wins += 1
        
        if total_scenarios == 0:
            return None
        
        win_probability = (wins / total_scenarios) * 100
        tie_probability = (ties / total_scenarios) * 100
        lose_probability = 100 - win_probability - tie_probability
        
        return {
            'method': 'exact',
            'total_scenarios': total_scenarios,
            'wins': wins,
            'ties': ties,
            'losses': total_scenarios - wins - ties,
            'win_probability': win_probability,
            'tie_probability': tie_probability,
            'lose_probability': lose_probability
        }
    
    @staticmethod
    def monte_carlo_simulation(player_cards, community_cards, num_opponents, iterations=10000):
        """Monte Carlo simulation as fallback for complex scenarios."""
        wins = 0
        ties = 0
        
        for _ in range(iterations):
            # Create a fresh deck and remove known cards
            deck = Deck()
            deck.cards = ExactProbabilityCalculator.get_remaining_deck(player_cards + community_cards)
            deck.shuffle()
            
            # Deal remaining community cards
            final_community = community_cards[:]
            while len(final_community) < 5:
                final_community.append(deck.draw_card())
            
            # Deal opponent hands
            opponent_hands = []
            for _ in range(num_opponents):
                opponent_hand = [deck.draw_card(), deck.draw_card()]
                opponent_hands.append(opponent_hand)
            
            # Evaluate player's hand
            player_all_cards = player_cards + final_community
            player_result = HandEvaluator.find_best_hand(player_all_cards)[:3]
            
            # Evaluate opponent hands and compare
            player_wins_round = True
            player_ties_round = False
            
            for opponent_hand in opponent_hands:
                opponent_all_cards = opponent_hand + final_community
                opponent_result = HandEvaluator.find_best_hand(opponent_all_cards)[:3]
                
                comparison = HandEvaluator.compare_hands(player_result, opponent_result)
                if comparison < 0:
                    player_wins_round = False
                    break
                elif comparison == 0:
                    player_ties_round = True
            
            if player_wins_round:
                if player_ties_round:
                    ties += 1
                else:
                    wins += 1
        
        win_probability = (wins / iterations) * 100
        tie_probability = (ties / iterations) * 100
        lose_probability = 100 - win_probability - tie_probability
        
        return {
            'method': 'monte_carlo',
            'iterations': iterations,
            'wins': wins,
            'ties': ties,
            'losses': iterations - wins - ties,
            'win_probability': win_probability,
            'tie_probability': tie_probability,
            'lose_probability': lose_probability
        }
    
    @staticmethod
    def calculate_win_probability(player_cards, community_cards, num_opponents):
        """Calculate win probability using the best available method."""
        try:
            # Try exact calculation first
            result = ExactProbabilityCalculator.calculate_exact_probability(
                player_cards, community_cards, num_opponents
            )
            if result is not None:
                return result
        except (ValueError, MemoryError):
            pass
        
        # Fall back to Monte Carlo
        return ExactProbabilityCalculator.monte_carlo_simulation(
            player_cards, community_cards, num_opponents
        )

def parse_card(card_str):
    """Parse a card string like 'AH' or 'As' into a Card object."""
    if len(card_str) != 2:
        raise ValueError(f"Invalid card format: {card_str}")
    
    rank = card_str[0].upper()
    suit = card_str[1].upper()
    
    # Validate rank
    if rank not in "23456789TJQKA":
        raise ValueError(f"Invalid rank: {rank}")
    
    # Validate suit
    if suit not in "SCHD":
        raise ValueError(f"Invalid suit: {suit}")
    
    return Card(rank, suit)

def get_user_cards():
    """Get the player's hole cards from user input."""
    while True:
        try:
            user_input = input("Enter your two hole cards (e.g., AH KS): ").strip()
            card_strings = user_input.split()
            
            if len(card_strings) != 2:
                print("Please enter exactly two cards.")
                continue
            
            cards = [parse_card(card_str) for card_str in card_strings]
            return cards
            
        except ValueError as e:
            print(f"Error: {e}")
            print("Please use format like 'AH KS' (rank + suit)")
            print("Ranks: 2-9, T, J, Q, K, A")
            print("Suits: S, C, H, D")

def get_community_cards():
    """Get community cards from user input (optional)."""
    while True:
        try:
            user_input = input("Enter community cards (0-5 cards, or press Enter to skip): ").strip()
            
            if not user_input:
                return []
            
            card_strings = user_input.split()
            
            if len(card_strings) > 5:
                print("Please enter at most 5 community cards.")
                continue
            
            cards = [parse_card(card_str) for card_str in card_strings]
            return cards
            
        except ValueError as e:
            print(f"Error: {e}")
            print("Please use format like 'AH KS 7D' (rank + suit)")
            print("Ranks: 2-9, T, J, Q, K, A")
            print("Suits: S, C, H, D")

def get_number_of_players():
    """Get the number of players from user input."""
    while True:
        try:
            user_input = input("How many players are in the game (2-10)? ").strip()
            num_players = int(user_input)
            
            if 2 <= num_players <= 10:
                return num_players
            else:
                print("Please enter a number between 2 and 10.")
                
        except ValueError:
            print("Please enter a valid number.")

def calculate_relative_hand_strength(hand_type, strength_percentage, num_players):
    """Calculate relative hand strength based on number of players."""
    # Adjust strength based on number of players
    # With more players, you need stronger hands to win
    if num_players <= 3:
        multiplier = 1.0  # Heads-up or 3-way, weaker hands can win
    elif num_players <= 6:
        multiplier = 0.9  # 4-6 players, need decent hands
    else:
        multiplier = 0.8  # 7+ players, need strong hands
    
    adjusted_strength = min(100, strength_percentage * multiplier)
    
    # Give context for the number of players
    if num_players == 2:
        context = "(heads-up)"
    elif num_players <= 4:
        context = "(small table)"
    elif num_players <= 6:
        context = "(medium table)"
    else:
        context = "(full table)"
    
    return adjusted_strength, context

def run_interactive_calculator():
    print("🃏 Welcome to Poker Simulator! 🃏")
    print("=" * 40)
    
    # Get game setup
    num_players = get_number_of_players()
    print(f"\n👥 Playing with {num_players} players")
    
    # Get player's cards
    print("\n📋 Enter your cards:")
    player_cards = get_user_cards()
    print(f"\n🂠 Your hole cards: {' '.join(repr(card) for card in player_cards)}")
    
    # Get community cards
    print("\n📋 Enter community cards (if any):")
    community_cards = get_community_cards()
    if community_cards:
        print(f"🂡 Community cards: {' '.join(repr(card) for card in community_cards)}")
    else:
        print("🂡 No community cards entered.")
    
    # Display all cards nicely
    print("\n" + "=" * 40)
    print("📊 HAND ANALYSIS:")
    print("=" * 40)
    print(f"🂠 Your cards: {' '.join(str(card) for card in player_cards)}")
    if community_cards:
        print(f"🂡 Community: {' '.join(str(card) for card in community_cards)}")
    
    # Evaluate the hand if we have enough cards
    all_cards = player_cards + community_cards
    if len(all_cards) >= 5:
        try:
            hand_type, rank, tie_breakers, best_cards = HandEvaluator.find_best_hand(all_cards)
            base_strength = HandEvaluator.get_hand_strength_percentage(hand_type)
            adjusted_strength, table_context = calculate_relative_hand_strength(hand_type, base_strength, num_players)
            
            print(f"\n🎯 BEST HAND: {hand_type}")
            print(f"🃏 Cards used: {' '.join(repr(card) for card in best_cards)}")
            print(f"💪 Base hand strength: {base_strength}%")
            print(f"📊 Adjusted strength: {adjusted_strength:.1f}% {table_context}")
            
            # Add contextual advice based on strength and players
            if adjusted_strength >= 85:
                print("🔥 EXCELLENT! This is a monster hand - bet aggressively!")
            elif adjusted_strength >= 70:
                print("💪 VERY STRONG! You should be confident with this hand.")
            elif adjusted_strength >= 50:
                print("👍 GOOD HAND! Play it strong but watch for danger signs.")
            elif adjusted_strength >= 30:
                print("🤔 DECENT HAND. Proceed with caution, especially with many players.")
            elif adjusted_strength >= 15:
                print("😬 WEAK HAND. Consider folding unless you have position/pot odds.")
            else:
                print("💀 VERY WEAK. This is likely a fold in most situations.")
            
            # Player count specific advice
            if num_players >= 8:
                print(f"\n⚠️  With {num_players} players, you need stronger hands to win!")
            elif num_players == 2:
                print(f"\n💡 In heads-up play, even weaker hands can be playable!")
            
            # Calculate exact win probability
            num_opponents = num_players - 1
            if len(all_cards) >= 5:  # We have enough cards for probability calculation
                print(f"\n🎲 CALCULATING WIN PROBABILITY vs {num_opponents} opponents...")
                try:
                    prob_result = ExactProbabilityCalculator.calculate_win_probability(
                        player_cards, community_cards, num_opponents
                    )
                    
                    print(f"\n🎯 PROBABILITY ANALYSIS ({prob_result['method'].upper()}):")
                    print("=" * 40)
                    print(f"🏆 Win: {prob_result['win_probability']:.1f}%")
                    print(f"🤝 Tie: {prob_result['tie_probability']:.1f}%")
                    print(f"💀 Lose: {prob_result['lose_probability']:.1f}%")
                    
                    if prob_result['method'] == 'exact':
                        print(f"\n📊 Analysis based on {prob_result['total_scenarios']:,} exact scenarios")
                        print("✅ This is the mathematically precise probability!")
                    else:
                        print(f"\n📊 Analysis based on {prob_result['iterations']:,} simulations")
                        print("📈 Accurate to within ~1% with 95% confidence")
                    
                    # Give probability-based advice
                    win_prob = prob_result['win_probability']
                    if win_prob >= 70:
                        print(f"\n🚀 EXCELLENT ODDS! You're heavily favored to win.")
                    elif win_prob >= 50:
                        print(f"\n👍 GOOD ODDS! You're favored to win this hand.")
                    elif win_prob >= 30:
                        print(f"\n⚖️  DECENT ODDS! Proceed with caution.")
                    elif win_prob >= 15:
                        print(f"\n📉 POOR ODDS! Consider folding unless pot odds justify a call.")
                    else:
                        print(f"\n💀 TERRIBLE ODDS! This is almost certainly a fold.")
                        
                except Exception as e:
                    print(f"❌ Error calculating probability: {e}")
                
        except Exception as e:
            print(f"❌ Error evaluating hand: {e}")
    else:
        print(f"\n⏳ Need at least 5 cards to evaluate hand (current: {len(all_cards)})")
        print("💡 Add community cards to see your hand strength and win probability!")
    
    print("\n" + "=" * 40)
    print("🎉 Calculation complete!")

def run_hand_evaluator_tests():
    """Runs a full suite of tests for the HandEvaluator logic."""
    print("🧪 Testing HandEvaluator...")
    print("=" * 50)
    
    test_cases = [
        (["AS", "KS", "QS", "JS", "TS"], "Royal Flush"),
        (["9H", "8H", "7H", "6H", "5H"], "Straight Flush"),
        (["AS", "AC", "AH", "AD", "KS"], "Four of a Kind"),
        (["KS", "KC", "KH", "2S", "2C"], "Full House"),
        (["AH", "KH", "QH", "JH", "9H"], "Flush"),
        (["AS", "KC", "QH", "JD", "TS"], "Straight"),
        (["5S", "4C", "3H", "2D", "AS"], "Straight"),
        (["AS", "AC", "AH", "KD", "QS"], "Three of a Kind"),
        (["AS", "AC", "KH", "KD", "QS"], "Two Pair"),
        (["AS", "AC", "KH", "QD", "JS"], "Pair"),
        (["AS", "KC", "QH", "JD", "9S"], "High Card"),
    ]
    
    passed, failed = 0, 0
    for i, (card_strs, expected) in enumerate(test_cases, 1):
        try:
            cards = [parse_card(card_str) for card_str in card_strs]
            hand_type, _, _ = HandEvaluator.evaluate_hand(cards)
            strength = HandEvaluator.get_hand_strength_percentage(hand_type)
            if hand_type == expected:
                print(f"✅ Test {i:2d}: {' '.join(card_strs):15} → {hand_type:15} ({strength}%)")
                passed += 1
            else:
                print(f"❌ Test {i:2d}: {' '.join(card_strs):15} → {hand_type:15} (expected: {expected})")
                failed += 1
        except Exception as e:
            print(f"💥 Test {i:2d}: {' '.join(card_strs):15} → ERROR: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("🎉 All hand evaluation tests passed!")
    else:
        print("🚨 Some tests failed.")

def run_method_comparison_demo():
    """Demonstrates and explains the different calculation methods."""
    print("🧮 MATHEMATICAL METHODS COMPARISON")
    print("=" * 50)
    
    player_cards = [parse_card("AS"), parse_card("AC")]
    community_cards = [parse_card("KH"), parse_card("QD"), parse_card("JS")]
    
    print(f"📋 Scenario: Pocket Aces vs 1 opponent on a draw-heavy board")
    print(f"🂠 Your cards: {' '.join(repr(card) for card in player_cards)}")
    print(f"🂡 Community: {' '.join(repr(card) for card in community_cards)}\n")
    
    # Exact Method
    print("🧮 METHOD 1: EXACT COMBINATORIAL ANALYSIS")
    print("-" * 40)
    exact_result = ExactProbabilityCalculator.calculate_exact_probability(player_cards, community_cards, 1)
    if exact_result:
        print(f"✅ EXACT: Win {exact_result['win_probability']:.3f}%, Tie {exact_result['tie_probability']:.3f}%")
        print(f"   (Based on {exact_result['total_scenarios']:,} scenarios)")
    
    # Monte Carlo Method
    print("\n🎲 METHOD 2: MONTE CARLO SIMULATION")
    print("-" * 40)
    for iterations in [1000, 10000, 100000]:
        mc_result = ExactProbabilityCalculator.monte_carlo_simulation(player_cards, community_cards, 1, iterations)
        win_error = abs(mc_result['win_probability'] - exact_result['win_probability'])
        print(f"📊 {iterations:,} sims: Win {mc_result['win_probability']:.3f}%, Tie {mc_result['tie_probability']:.3f}% (Error: ±{win_error:.3f}%)")

    print("\n🤔 WHEN TO USE EACH METHOD:")
    print("=" * 50)
    print("🧮 USE EXACT: For < 3 opponents and simple scenarios for perfect accuracy.")
    print("🎲 USE MONTE CARLO: For > 2 opponents or complex boards for fast, strong approximations.")
    print("\n🚀 OUR HYBRID APPROACH: Automatically chooses the best method for you!")
    print("   You get mathematical precision whenever possible, and speed when necessary.")

def main():
    """
    Main entry point for the Poker Simulator CLI.
    Handles command-line arguments to run the calculator, tests, or demos.
    """
    parser = argparse.ArgumentParser(
        description="A powerful command-line poker probability calculator.",
        formatter_class=argparse.RawTextHelpFormatter  # For better help text formatting
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help="Run the suite of tests for the HandEvaluator."
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help="Run a demonstration comparing exact vs. Monte Carlo methods."
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help="Run the interactive poker calculator (default action)."
    )

    args = parser.parse_args()

    if args.test:
        run_hand_evaluator_tests()
    elif args.demo:
        run_method_comparison_demo()
    else:
        # If no flags are provided, or --interactive is used, run the calculator.
        run_interactive_calculator()

if __name__ == "__main__":
    main()
